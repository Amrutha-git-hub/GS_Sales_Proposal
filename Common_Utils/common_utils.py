import os 
import streamlit as st

import streamlit as st
import pandas as pd
from typing import List
import os
from datetime import datetime

from Search.WebsiteUrl_Agent.agent_runner import get_urls
import asyncio 
from Common_Utils.pain_points_extractor import *

def check_field_validation(field_name: str, field_value: str, is_mandatory: bool = False) -> bool:
    """Check if field validation should show warning"""
    if is_mandatory and not field_value.strip():
        return True
    return False

def show_field_warning(field_name: str):
    """Show warning message for mandatory fields"""
    st.markdown(f'<div class="field-warning">⚠️ {field_name} is mandatory and cannot be empty!</div>', unsafe_allow_html=True)

import re

def normalize_url(url):
    """
    Ensure the URL has a valid scheme (http/https).
    """
    if not url:
        return ""
    
    # If it already starts with http:// or https:// — keep it
    if re.match(r"^https?://", url.strip(), re.IGNORECASE):
        return url.strip()
    
    # Otherwise, prepend https://
    return f"https://{url.strip()}"


def save_uploaded_file_and_get_path(uploaded_file, logger, client_enterprise_name):
    """Save uploaded file to a temporary directory and return the file path"""
    logger.info(f"Starting file upload process for file: {uploaded_file.name if uploaded_file else 'None'}")
    
    try:
        if uploaded_file is not None:
            logger.debug(f"File details - Name: {uploaded_file.name}, Size: {uploaded_file.size} bytes")

            # Base upload directory from environment
            base_upload_dir = os.getenv("FILE_SAVE_PATH")
            logger.debug(f"Base upload directory path: {base_upload_dir}")
            
            # Full path including enterprise name
            enterprise_upload_dir = os.path.join(base_upload_dir, client_enterprise_name)
            logger.debug(f"Enterprise-specific upload path: {enterprise_upload_dir}")
            
            # Create the directory if it doesn't exist
            if not os.path.exists(enterprise_upload_dir):
                try:
                    os.makedirs(enterprise_upload_dir)
                    logger.info(f"Created directory: {enterprise_upload_dir}")
                except OSError as e:
                    logger.error(f"Failed to create directory {enterprise_upload_dir}: {str(e)}")
                    raise
            
            # Full file path
            file_path = os.path.join(enterprise_upload_dir, uploaded_file.name)
            logger.debug(f"Full file path: {file_path}")
            
            # Save the file
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                logger.info(f"Successfully saved file to: {file_path}")
                return file_path
            except IOError as e:
                logger.error(f"Failed to save file {file_path}: {str(e)}")
                raise
                
        else:
            logger.warning("No file provided for upload")
            return None
            
    except Exception as e:
        st.error(str(e))
        logger.error(f"Unexpected error in save_uploaded_file_and_get_path: {str(e)}")
        raise


def save_uploaded_file_and_get_path(uploaded_file):
    """Save uploaded file to a temporary directory and return the file path"""
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Create file path
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None


# Function to get URLs (placeholder function)

def get_urls_list(company_name) -> List[str]:
    """
    Placeholder function that returns a list of URLs
    Replace this with your actual function that fetches URLs
    """
    return asyncio.run(get_urls(company_name))

# Function to get LinkedIn profiles (NEW)


# Function to get roles list
def get_roles_list() -> List[str]:
    """
    Function that returns a list of executive roles
    """
    return [
        "CEO (Chief Executive Officer)",
        "CMO (Chief Marketing Officer)",
        "CTO (Chief Technology Officer)",
        "CFO (Chief Financial Officer)",
        "COO (Chief Operating Officer)",
        "CHRO (Chief Human Resources Officer)",
        "CDO (Chief Data Officer)",
        "CPO (Chief Product Officer)",
        "CRO (Chief Revenue Officer)",
        "CIO (Chief Information Officer)"
    ]


from WebScraper.scrape_agent import get_data

def get_url_details(url:str):
    """Use this if you want to run async function synchronously"""
    try:
        # Run the async function synchronously
        website_details = asyncio.run(get_data(url))
        return website_details
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_priority_suggestions() -> List[dict]:
    """
    Function that returns a list of priority suggestions with titles and descriptions
    Replace this with your actual function that fetches priority suggestions
    """
    return [
        {
            "title": "Digital Transformation Initiative",
            "description": "Modernize systems and processes for improved efficiency",
            "icon": "🚀"
        },
        {
            "title": "Data Analytics & Business Intelligence",
            "description": "Implement advanced analytics for better decision making",
            "icon": "📊"
        },
        {
            "title": "Process Optimization & Automation",
            "description": "Streamline workflows and reduce manual tasks",
            "icon": "🔧"
        }
    ]

def get_editable_content() -> str:
    """
    Placeholder function that returns editable content
    Replace this with your actual function that fetches editable content
    """
    return """This is editable content from the function:

- Project requirements and specifications
- Current implementation status
- Key stakeholder feedback
- Next steps and action items
- Additional notes and observations

You can modify this content as needed."""


# Function to get summary items (NEW)
# from Rag.rag import get_pain_points




def get_pain_items(file,company_name):
    print("-----------------------------------------------------------")
    return get_pain_points(file,company_name)




def check_field_validation(field_name: str, field_value: str, is_mandatory: bool = False) -> bool:
    """Check if field validation should show warning"""
    if is_mandatory and not field_value.strip():
        return True
    return False

def show_field_warning(field_name: str):
    """Show warning message for mandatory fields"""
    st.markdown(f'<div class="field-warning">⚠️ {field_name} is mandatory and cannot be empty!</div>', unsafe_allow_html=True)


def save_uploaded_file(uploaded_file, save_dir="uploaded_rf_is"):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, uploaded_file.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path

def save_uploaded_file_and_get_path(uploaded_file):
    """Save uploaded file to a temporary directory and return the file path"""
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Create file path
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

def set_global_message(message, message_type="info", duration=10):
    """
    Set a global message to be displayed
    
    Args:
        message (str): The message text to display
        message_type (str): Type of message - "error", "warning", "info", "success"
        duration (int): Duration in seconds before auto-dismiss (default: 10)
    """
    st.session_state.global_message = {
        'message': message,
        'type': message_type,
        'timestamp': datetime.now(),
        'duration': duration
    }
