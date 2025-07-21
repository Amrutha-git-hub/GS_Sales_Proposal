#!/usr/bin/env python3
"""
ngrok_manager.py - Python script to manage ngrok restarts every 8 hours
"""

import subprocess
import time
import requests
import json
import logging
import signal
import sys
from datetime import datetime
import os
import psutil
import re

# Configuration
STREAMLIT_APP_PATH = "app.py"  # Path to your Streamlit app
STREAMLIT_PORT = 8501
RESTART_INTERVAL = 8 * 60 * 60  # 8 hours in seconds
LOG_FILE = "/tmp/ngrok_manager.log"
URL_FILE = "/tmp/ngrok_url.txt"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class NgrokManager:
    def __init__(self):
        self.ngrok_process = None
        self.streamlit_process = None
        self.running = True
        self.detected_port = None
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logging.info(f"Received signal {signum}, shutting down...")
        self.running = False
        self.kill_ngrok()
        if self.streamlit_process:
            self.streamlit_process.terminate()
        sys.exit(0)
    
    def find_streamlit_port(self):
        """Find the port where Streamlit is running"""
        try:
            # Method 1: Check if Streamlit is already running and find its port
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'connections']):
                try:
                    if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if 'streamlit' in cmdline and 'run' in cmdline:
                            # Found Streamlit process, check its connections
                            connections = proc.info['connections']
                            for conn in connections:
                                if conn.status == 'LISTEN' and conn.laddr.ip in ['127.0.0.1', '0.0.0.0']:
                                    port = conn.laddr.port
                                    if port >= 8500 and port <= 8510:  # Typical Streamlit port range
                                        logging.info(f"Found Streamlit running on port {port}")
                                        return port
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Method 2: Check if default port is in use
            if self.is_port_in_use(STREAMLIT_PORT):
                logging.info(f"Port {STREAMLIT_PORT} is in use, assuming Streamlit")
                return STREAMLIT_PORT
            
            return None
            
        except Exception as e:
            logging.error(f"Error finding Streamlit port: {e}")
            return None
    
    def is_port_in_use(self, port):
        """Check if a port is in use"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def start_streamlit(self):
        """Start Streamlit if not already running"""
        try:
            # First check if Streamlit is already running
            current_port = self.find_streamlit_port()
            if current_port:
                logging.info(f"Streamlit already running on port {current_port}")
                self.detected_port = current_port
                return True
            
            # Start Streamlit
            logging.info(f"Starting Streamlit on port {STREAMLIT_PORT}...")
            self.streamlit_process = subprocess.Popen(
                ["streamlit", "run", STREAMLIT_APP_PATH, "--server.port", str(STREAMLIT_PORT)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for Streamlit to start
            max_wait = 30
            for i in range(max_wait):
                if self.is_port_in_use(STREAMLIT_PORT):
                    logging.info(f"Streamlit started successfully on port {STREAMLIT_PORT}")
                    self.detected_port = STREAMLIT_PORT
                    return True
                time.sleep(1)
            
            logging.error("Streamlit failed to start within 30 seconds")
            return False
            
        except Exception as e:
            logging.error(f"Error starting Streamlit: {e}")
            return False
    
    def kill_ngrok(self):
        """Kill existing ngrok processes"""
        try:
            logging.info("Killing existing ngrok processes...")
            subprocess.run(["pkill", "-f", "ngrok"], check=False)
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error killing ngrok: {e}")
    
    def start_ngrok(self):
        """Start ngrok tunnel"""
        try:
            # Ensure we have the correct port
            if not self.detected_port:
                port = self.find_streamlit_port()
                if not port:
                    logging.error("Cannot find Streamlit port")
                    return False
                self.detected_port = port
            
            logging.info(f"Starting ngrok tunnel for port {self.detected_port}...")
            self.ngrok_process = subprocess.Popen(
                ["ngrok", "http", str(self.detected_port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # Wait for ngrok to start
            
            # Get the public URL
            url = self.get_ngrok_url()
            if url:
                logging.info(f"Ngrok tunnel started successfully: {url}")
                self.save_url(url)
                return True
            else:
                logging.error("Failed to get ngrok URL")
                return False
                
        except Exception as e:
            logging.error(f"Error starting ngrok: {e}")
            return False
    
    def get_ngrok_url(self):
        """Get the public ngrok URL"""
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
            if response.status_code == 200:
                tunnels = response.json()
                for tunnel in tunnels.get("tunnels", []):
                    if tunnel.get("proto") == "https":
                        return tunnel.get("public_url")
        except Exception as e:
            logging.error(f"Error getting ngrok URL: {e}")
        return None
    
    def save_url(self, url):
        """Save the ngrok URL to a file"""
        try:
            with open(URL_FILE, 'w') as f:
                f.write(url)
        except Exception as e:
            logging.error(f"Error saving URL: {e}")
    
    def check_streamlit(self):
        """Check if Streamlit is running and get its port"""
        try:
            port = self.find_streamlit_port()
            if port:
                logging.info(f"Streamlit is running on port {port}")
                self.detected_port = port
                return True
            else:
                logging.warning("Streamlit is not running")
                return False
        except Exception as e:
            logging.error(f"Error checking Streamlit: {e}")
            return False
    
    def restart_ngrok(self):
        """Restart ngrok tunnel"""
        logging.info("Starting ngrok restart cycle...")
        
        # Check if Streamlit is running, if not try to start it
        if not self.check_streamlit():
            logging.info("Streamlit not running, attempting to start...")
            if not self.start_streamlit():
                logging.error("Failed to start Streamlit")
                return False
        
        # Kill existing ngrok and start new one
        self.kill_ngrok()
        success = self.start_ngrok()
        
        if success:
            logging.info("Ngrok restart completed successfully")
        else:
            logging.error("Ngrok restart failed")
        
        return success
    
    def run(self):
        """Main loop to restart ngrok every 8 hours"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logging.info("Starting ngrok manager...")
        
        # Initial start
        if not self.restart_ngrok():
            logging.error("Failed to start ngrok initially")
            return
        
        # Main loop
        while self.running:
            try:
                logging.info(f"Waiting {RESTART_INTERVAL} seconds until next restart...")
                time.sleep(RESTART_INTERVAL)
                
                if self.running:  # Check if we haven't been signaled to stop
                    self.restart_ngrok()
                    
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait a minute before retrying
        
        self.kill_ngrok()
        if self.streamlit_process:
            self.streamlit_process.terminate()
        logging.info("Ngrok manager stopped")

if __name__ == "__main__":
    manager = NgrokManager()
    manager.run()