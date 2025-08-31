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


# from WebScraper.scrape_agent import get_data

# def get_url_details(url:str):
#     """Use this if you want to run async function synchronously"""
#     try:
#         # Run the async function synchronously
#         website_details = asyncio.run(get_data(url))
#         return website_details
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
    

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

def clear_global_error():
    """Clear the global error message"""
    if 'global_message' in st.session_state:
        del st.session_state.global_message

def is_message_expired():
    """Check if the current message has expired"""
    if 'global_message' not in st.session_state:
        return True
    
    message_data = st.session_state.global_message
    elapsed_time = (datetime.now() - message_data['timestamp']).total_seconds()
    return elapsed_time > message_data['duration']

@st.dialog("‼️ Error")
def show_error_dialog(message_text, fun1=None, fun2=None, fun3=None, btn1_text="Close", btn2_text="OK", btn3_text="Cancel", show_third_button=False, single_button=False):
    """Error message dialog with icon and multiple action buttons"""
    st.error(message_text)
    
    # Single button layout - centered with good width
    if single_button:
        col1, col2, col3 = st.columns([1, 2, 1])  # Side margins with wider center
        with col2:
            if st.button(btn1_text, key="error_btn1", type="primary", use_container_width=True):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
    # Two or three buttons layout based on show_third_button parameter
    elif show_third_button:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button(btn1_text, key="error_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="error_btn2"):
                if fun2:
                    fun2()
                    st.rerun()
        with col3:
            if st.button(btn3_text, key="error_btn3"):
                if fun3:
                    fun3()
                    st.rerun()
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(btn1_text, key="error_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="error_btn2"):
                if fun2:
                    fun2()
                    st.rerun()


@st.dialog("⚠️ Warning")
def show_warning_dialog(message_text, fun1=None, fun2=None, fun3=None, btn1_text="Close", btn2_text="OK", btn3_text="Cancel", show_third_button=False, single_button=False):
    """Warning message dialog with icon and multiple action buttons"""
    st.warning(message_text)
    
    # Single button layout - centered with good width
    if single_button:
        col1, col2, col3 = st.columns([1, 2, 1])  # Side margins with wider center
        with col2:
            if st.button(btn1_text, key="warning_btn1", type="primary", use_container_width=True):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
    # Two or three buttons layout based on show_third_button parameter
    elif show_third_button:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button(btn1_text, key="warning_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="warning_btn2"):
                if fun2:
                    fun2()
                    st.rerun()
        with col3:
            if st.button(btn3_text, key="warning_btn3"):
                if fun3:
                    fun3()
                    st.rerun()
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(btn1_text, key="warning_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="warning_btn2"):
                if fun2:
                    fun2()
                    st.rerun()


@st.dialog("✅ Success")
def show_success_dialog(message_text, fun1=None, fun2=None, fun3=None, btn1_text="Close", btn2_text="OK", btn3_text="Cancel", show_third_button=False, single_button=False):
    """Success message dialog with icon and multiple action buttons"""
    st.success(message_text)
    
    # Single button layout - centered with good width
    if single_button:
        col1, col2, col3 = st.columns([1, 2, 1])  # Side margins with wider center
        with col2:
            if st.button(btn1_text, key="success_btn1", type="primary", use_container_width=True):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
    # Two or three buttons layout based on show_third_button parameter
    elif show_third_button:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button(btn1_text, key="success_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="success_btn2"):
                if fun2:
                    fun2()
                    st.rerun()
        with col3:
            if st.button(btn3_text, key="success_btn3"):
                if fun3:
                    fun3()
                    st.rerun()
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(btn1_text, key="success_btn1", type="primary"):
                if fun1:
                    fun1()
                    st.rerun()
                else:
                    clear_global_error()
                    st.rerun()
        with col2:
            if st.button(btn2_text, key="success_btn2"):
                if fun2:
                    fun2()
                    st.rerun()
                    
def clear_global_error():
    """Clear the global message from session state"""
    if 'global_message' in st.session_state:
        del st.session_state.global_message
    if 'showing_dialog' in st.session_state:
        del st.session_state.showing_dialog

def is_message_expired():
    """Check if the current message has expired"""
    if 'global_message' not in st.session_state:
        return True
    
    message_data = st.session_state.global_message
    elapsed_time = (datetime.now() - message_data['timestamp']).total_seconds()
    return elapsed_time > message_data['duration']

def set_global_message(message_text, message_type='error', fun1=None, fun2=None, fun3=None, 
                      btn1_text="Close", btn2_text="OK", btn3_text="Cancel", show_third_button=False,single_button = True):
    """Helper function to set and immediately display global message"""
    # Check if we should show the dialog (only if not already showing)
    if 'showing_dialog' not in st.session_state or not st.session_state.showing_dialog:
        st.session_state.showing_dialog = True
        
        # Direct orchestration - show the appropriate dialog immediately
        if message_type == "error":
            show_error_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button,single_button=True)
        elif message_type == "warning":
            show_warning_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button,single_button=True)
        elif message_type == "success":
            show_success_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button,single_button=True)
        else:
            # Fallback for other message types
            st.info(message_text)
    clear_global_error()

def display_global_message():
    """Display the global message using appropriate dialog based on message type."""
    if 'global_message' not in st.session_state:
        return
    
    message_data = st.session_state.global_message
    message_type = message_data['type']
    message_text = message_data['message']
    
    # Get optional parameters
    fun1 = message_data.get('fun1', None)
    fun2 = message_data.get('fun2', None)
    fun3 = message_data.get('fun3', None)
    btn1_text = message_data.get('btn1_text', "Close")
    btn2_text = message_data.get('btn2_text', "OK")
    btn3_text = message_data.get('btn3_text', "Cancel")
    show_third_button = message_data.get('show_third_button', False)
    
    # Direct orchestration - show the appropriate dialog
    if message_type == "error":
        show_error_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button)
    elif message_type == "warning":
        show_warning_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button)
    elif message_type == "success":
        show_success_dialog(message_text, fun1, fun2, fun3, btn1_text, btn2_text, btn3_text, show_third_button)
    else:
        # Fallback for other message types
        st.info(message_text)



from WebScraper.webscraper_beautifulsoup import get_url_details_with_bs4
from WebScraper.scrape_agent import get_url_detail_using_googleai


def get_scraped_data(url:str , scrape_technique= "bs4"):
    if scrape_technique=='bs4':
        return get_url_details_with_bs4(url)
    else:
        return  asyncio.run(get_url_detail_using_googleai(url))
