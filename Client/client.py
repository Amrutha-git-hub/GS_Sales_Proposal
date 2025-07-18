
import streamlit as st
import pandas as pd
import os
import logging
from typing import List
from .client_utils import *
import threading
import time
from Search.Linkedin.linkedin_serp import *
from Search.Linkedin.linkedin_agent_runner_unused import *
from Recommendation.recommendation_utils import *
from .client_css import client_css
from .client_dataclass import *
from datetime import datetime 
# Configure logging
from WebScraper.webscraper_without_ai import get_url_details_without_ai
from Common_Utils.common_utils import set_global_message

def normalize_url(url: str) -> str:
    url = url.strip()

    # Add scheme if missing
    if not re.match(r'^https?://', url):
        url = 'https://' + url

    # Extract the domain part (remove scheme temporarily for easier check)
    domain_part = re.sub(r'^https?://', '', url).split('/')[0]

    # If no known domain suffix present, append '.com'
    if not re.search(r'\.(com|in|org|net|co|io|edu|gov)(/|$)', domain_part):
        url = url.rstrip('/') + '.com'

    return url

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
        set_global_message(str(e))
        logger.error(f"Unexpected error in save_uploaded_file_and_get_path: {str(e)}")
        raise

def validate_client_mandatory_fields():
    """Validate client mandatory fields using dataclass"""
    
    
    try:
        client_data = client_state_manager.get_client_data()
        #logger.debug("Retrieved client data for validation")
        
        # Temporarily return True - validation disabled
        #st.info("Validation bypassed - returning True")
        #return True
        
        # Uncomment below for actual validation
        result = client_data.validate_mandatory_fields()
        return result
        
    except Exception as e:
        set_global_message(f"Error in validate_client_mandatory_fields: {str(e)}")
        return False
@st.fragment
def render_client_name_section(logger, client_data, is_locked):
    """Render the client enterprise name section"""
    try:
        logger.debug("Processing client enterprise name section")
        
        st.markdown("""
            <div class="tooltip-label">
                Client Enterprise Name <span style="color:red;">*</span>
                <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client in all documentation and communications. This field is mandatory for creating the client profile.">ⓘ</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create a sub-column layout for name input and find URLs button
        name_col, button_col = st.columns([3, 1])
        
        with name_col:
            client_enterprise_name = st.text_input(
                on_change=lambda: None,
                label="Client Enterprise Name",
                placeholder="Enter client enterprise name...",
                key="client_enterprise_name_input",
                label_visibility="collapsed",
                disabled=is_locked,
                value=client_data.enterprise_name
            )
            
            # Update dataclass when input changes
            if client_enterprise_name != client_data.enterprise_name:
                try:
                    client_state_manager.update_field('enterprise_name', client_enterprise_name)
                    logger.info(f"Updated enterprise name: {client_enterprise_name}")
                    
                    # Force rerun to synchronize other fragments
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error updating enterprise name: {str(e)}")
                    set_global_message("Unable to save enterprise name. Please try again.", 'error')
                    st.rerun()
        
        with button_col:
            try:
                # Find URLs button - only enabled when client name has more than 2 characters
                find_urls_disabled = not (client_enterprise_name and len(client_enterprise_name.strip()) > 2)
                logger.debug(f"Find URLs button disabled: {find_urls_disabled}")
                
                find_urls_clicked = st.button("🔍 Find Website",
                            disabled=find_urls_disabled,
                            help="Find website URLs for this company",
                            key="find_urls_button",
                            type="secondary")
            
            except Exception as e:
                logger.error(f"Error in Find URLs button section: {str(e)}")
                find_urls_clicked = False
                set_global_message("Unable to initialize website search. Please refresh the page.", 'error')
                st.rerun()
        
        # Handle the Find URLs button click
        if find_urls_clicked:
            logger.info(f"Find URLs button clicked for: {client_enterprise_name.strip()}")
            
            # Show processing message instead of spinner
            set_global_message(f"Finding websites for '{client_enterprise_name.strip()}'...", 'info')
            
            try:
                urls_list = get_urls_list(client_enterprise_name.strip())
                logger.info(f"Found {len(urls_list)} URLs for {client_enterprise_name.strip()}")
                
                # Update multiple fields at once
                client_state_manager.update_multiple_fields(
                    website_urls_list=urls_list,
                    enterprise_name=client_enterprise_name,
                    last_company_name=client_enterprise_name.strip()
                )
                logger.debug("Updated client data with URLs list")
                
                if urls_list:
                    set_global_message(f"Successfully found {len(urls_list)} website URLs for {client_enterprise_name.strip()}", 'success')
                else:
                    set_global_message(f"No website URLs found for {client_enterprise_name.strip()}", "error")
                st.rerun()
                
            except Exception as e:
                logger.error(f"Error finding URLs for {client_enterprise_name.strip()}: {str(e)}")
                client_state_manager.update_field('website_urls_list', [])
                set_global_message("The requested websites couldn't be found. Please try again later.", "error")
                st.rerun()
        
        # Clear URLs if company name is cleared
        try:
            if not client_enterprise_name and client_data.enterprise_name:
                logger.info("Company name cleared, clearing URLs list")
                client_state_manager.update_multiple_fields(
                    website_urls_list=[],
                    enterprise_name="",
                    last_company_name=""
                )
                set_global_message("Company name cleared, website URLs reset", 'info')
                st.rerun()
        except Exception as e:
            logger.error(f"Error clearing URLs when company name cleared: {str(e)}")
            set_global_message("Unable to clear website data. Please refresh the page.", 'error')
            st.rerun()
        
        # Show validation warning if triggered and field is empty
        try:
            if client_data.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
                show_field_warning("Client Enterprise Name")
                logger.debug("Showed validation warning for Client Enterprise Name")
        except Exception as e:
            logger.error(f"Error showing validation warning: {str(e)}")
            set_global_message("Validation check failed. Please verify your input.", "error")
            st.rerun()
    
    except Exception as e:
        logger.error(f"Error in client enterprise name column: {str(e)}")
        set_global_message("Something went wrong with the client name section. Please refresh the page.", 'error')
        st.rerun()
    
    return client_enterprise_name
@st.fragment
def render_client_website_section(logger, client_data, is_locked):
    """Render the client website URL section"""
    try:
        logger.debug("Processing client website URL section")
        
        # Get the current enterprise name from the client data
        client_enterprise_name = client_data.enterprise_name
        
        # Label row with inline emoji and tooltip
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Client Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the client's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create columns for dropdown and buttons
        url_col, btn1_col, btn2_col = st.columns([7, 1, 2])
        
        with url_col:
            try:
                # URL selection logic
                client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
                logger.debug(f"Client name provided: {client_name_provided}")
                
                if not client_data.website_urls_list:
                    url_options = ["Select client website URL"]
                else:
                    url_options = ["Select client website URL"] + client_data.website_urls_list
                
                logger.debug(f"URL options count: {len(url_options)}")
                
                # Set default selection
                default_index = 0
                if client_data.website_url and client_data.website_url in url_options:
                    default_index = url_options.index(client_data.website_url)
                
                client_website_url = st.selectbox(
                    label="Client Website URL",
                    options=url_options,
                    index=default_index,
                    key="client_website_url_selector",
                    label_visibility="collapsed",
                    disabled=not client_name_provided or is_locked,
                    accept_new_options=True,
                )
                
                # Reset to empty string if default option is selected
                if client_website_url == "Select client website URL":
                    client_website_url = ""
                
                # Update dataclass when URL changes
                if client_website_url != client_data.website_url:
                    client_website_url = normalize_url(client_website_url)
                    try:
                        client_state_manager.update_field('website_url', client_website_url)
                        logger.info(f"Updated website URL: {client_website_url}")
                    except Exception as e:
                        logger.error(f"Error updating website URL: {str(e)}")
                        set_global_message("Unable to save website URL. Please try again.", 'error')
                        st.rerun()
                        
            except Exception as e:
                logger.error(f"Error in URL selection: {str(e)}")
                set_global_message("Unable to load website options. Please refresh the page.", 'error')
                st.rerun()
                client_website_url = ""
        
        # Buttons for website actions
        with btn1_col:
            try:
                refresh_clicked = st.button("🔄", help="Refresh website URLs list", key="refresh_urls_btn", 
                                        use_container_width=True, disabled=not client_name_provided)
            except Exception as e:
                logger.error(f"Error creating refresh button: {str(e)}")
                set_global_message("Unable to initialize refresh button. Please reload the page.", 'error')
                st.rerun()
                refresh_clicked = False
        
        with btn2_col:
            try:
                scrape_clicked = st.button("📑 Get Details", help="Get enterprise details", key="scrape_website_btn", 
                                        use_container_width=True, disabled=not client_website_url)
                
                if scrape_clicked and client_website_url:
                    logger.info(f"Scrape button clicked for URL: {client_website_url}")
                    client_state_manager.update_multiple_fields(
                        pending_scrape_url=client_website_url,
                        scraping_in_progress=True
                    )
                    set_global_message(f"Starting website analysis for {client_website_url}", 'info')
                    st.rerun()
            except Exception as e:
                logger.error(f"Error creating scrape button: {str(e)}")
                set_global_message("Error creating scrape button", 'error')
                st.rerun()
                scrape_clicked = False

        # Show redirect link when website is selected
        if client_website_url:
            client_website_url = normalize_url(client_website_url)
            with st.container():
                st.markdown(f'''
            <style>
                .plain-link {{
                    margin-top: -120px;  /* Increased from -90px to push it higher */
                    margin-left: 10px;
                    display: inline-block;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                }}
                
                .plain-link a {{
                    color: #0c5460;
                    text-decoration: none;
                }}
                
                .plain-link a:hover {{
                    text-decoration: underline;
                }}
            </style>
            <div class="plain-link">
                🌐 <a href="{client_website_url}" target="_blank">Visit Website</a>
            </div>
        ''', unsafe_allow_html=True)

        # Handle refresh action
        if refresh_clicked and client_name_provided:
            try:
                logger.info(f"Refreshing URLs for: {client_enterprise_name}")
                set_global_message("Refreshing website URLs...", 'info')
                
                urls_list = get_urls_list(client_enterprise_name)
                client_state_manager.update_multiple_fields(
                    website_urls_list=urls_list,
                    last_company_name=client_enterprise_name
                )
                logger.info(f"Successfully refreshed URLs, found {len(urls_list)} URLs")
                
                if urls_list:
                    set_global_message(f"Successfully refreshed! Found {len(urls_list)} website URLs", 'success')
                else:
                    set_global_message("No website URLs found during refresh", "error")
                st.rerun()
            except Exception as e:
                logger.error(f"Error refreshing URLs: {str(e)}")
                set_global_message(f"Failed to refresh URLs: {str(e)}", 'error')
                st.rerun()

        # Handle pending scraping operation
        if client_data.scraping_in_progress and client_data.pending_scrape_url:
            try:
                logger.info(f"Starting website scraping for: {client_data.pending_scrape_url}")
                set_global_message(f"Scraping website details from {client_data.pending_scrape_url}...", 'info')
                
                try:
                    # Get website details from the URL
                    scrape_result = get_url_details_without_ai(client_data.pending_scrape_url)
                    
                    # Extract data from the User object
                    website_name = scrape_result.name
                    logo_url = scrape_result.logo
                    description = scrape_result.description
                    services = scrape_result.services
                    
                    # Format the website details with description and services in bullet points
                    website_details = f"Company: {website_name}\n\n"
                    
                    if description:
                        website_details += f"Description:\n{description}\n\n"
                    
                    if services:
                        website_details += "Services:\n"
                        for service in services:
                            website_details += f"• {service}\n"
                    
                    # Check if scraping returned empty or no data
                    if not website_details or len(website_details.strip()) < 10:
                        logger.warning(f"Website scraping returned empty data for: {client_data.pending_scrape_url}")
                        client_state_manager.update_multiple_fields(
                            scraping_in_progress=False,
                            pending_scrape_url=None
                        )
                        set_global_message("Website scraping failed - No content could be extracted from the website. Please check if the URL is accessible and contains readable content.", "error")
                        st.rerun()
                    else:
                        logger.info(f"Successfully scraped website details, length: {len(website_details)}")
                        
                        # Prepare update parameters
                        update_params = {
                            'enterprise_details_content': website_details,
                            'last_analyzed_url': client_data.pending_scrape_url,
                            'scraping_in_progress': False,
                            'pending_scrape_url': None
                        }
                        
                        # Add logo to update parameters if available (storing in enterprise_logo)
                        if logo_url:
                            update_params['enterprise_logo'] = logo_url
                        
                        client_state_manager.update_multiple_fields(**update_params)
                        
                        # Show success message with logo info
                        if logo_url:
                            set_global_message("Website details and logo extracted successfully!", 'success')
                        else:
                            set_global_message("Website details extracted successfully!", 'success')
                        
                        st.rerun()
                        
                except Exception as scrape_error:
                    logger.error(f"Error during website scraping for {client_data.pending_scrape_url}: {str(scrape_error)}", exc_info=True)
                    client_state_manager.update_multiple_fields(
                        scraping_in_progress=False,
                        pending_scrape_url=None
                    )
                    set_global_message("Error scraping website", 'error')
                    logger.error(f"Error scraping: {str(scrape_error)}")
                    st.rerun()
                    
            except Exception as e:
                logger.error(f"Critical error in website scraping process: {str(e)}", exc_info=True)
                # Ensure scraping state is cleared even on critical errors
                try:
                    client_state_manager.update_multiple_fields(
                        scraping_in_progress=False,
                        pending_scrape_url=None
                    )
                except Exception as cleanup_error:
                    logger.error(f"Error during cleanup: {str(cleanup_error)}")
                
                set_global_message("A critical error occurred during website scraping. Please try again.", 'error')
                st.rerun()
                                    
    except Exception as e:
        logger.error(f"Error in scraping operation: {str(e)}")
        set_global_message(f"Error in website scraping operation: {str(e)}", 'error')
        st.rerun()


@st.fragment
def render_first_section(logger, client_data, is_locked):
    """Main function to render the first section with two columns"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        client_enterprise_name = render_client_name_section(logger, client_data, is_locked)
    
    with col2:
        render_client_website_section(logger, client_data, is_locked)
    
    return client_enterprise_name
# @st.fragment
# def doc_upload_section(logger,client_enterprise_name,client_data,is_locked,col3):
@st.fragment
def enterprise_content(logger, client_data, is_locked):
    """Render the enterprise details section"""
    try:
        logger.debug("Processing enterprise details section")
        
        st.markdown('''
        <div class="tooltip-label">
            Client Enterprise Details
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get the current enterprise name from the shared data
        client_enterprise_name = client_data.enterprise_name
        client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
        
        try:
            enterprise_details = st.text_area(
                label="Client Enterprise Details", 
                value=client_data.enterprise_details_content if client_name_provided else "",
                placeholder="Enter client name first to enable this field" if not client_name_provided else "Select/Enter the client website URL to fetch enterprise details", 
                height=150, 
                key="enterprise_details_textarea",
                label_visibility="collapsed",
                disabled=not client_name_provided or is_locked
            )
            
            # Update dataclass when text area changes
            if client_name_provided and enterprise_details != client_data.enterprise_details_content:
                try:
                    client_state_manager.update_client_data(enterprise_details_content=enterprise_details)
                    logger.debug("Updated enterprise details content")
                except Exception as e:
                    logger.error(f"Error updating enterprise details: {str(e)}")
                    set_global_message("Save failed - Your enterprise details couldn't be saved. Please try again", 'error')
                    
        except Exception as e:
            logger.error(f"Error creating enterprise details textarea: {str(e)}")
            set_global_message("Text editor unavailable - Please refresh the page to restore functionality", 'error')
            
    except Exception as e:
        logger.error(f"Error in enterprise details column: {str(e)}")
        set_global_message("Enterprise details section temporarily unavailable - Please refresh the page to continue", 'error')
    
    return client_name_provided


@st.fragment
def doc_upload_section(logger, client_data, is_locked):
    """Render the document upload section"""
    try:
        logger.debug("Processing file upload section")
        
        # Get the current enterprise name from the shared data
        client_enterprise_name = client_data.enterprise_name
        
        st.markdown('''
        <div class="tooltip-label">
            Upload RFI Document
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add custom CSS for file uploader
        st.markdown("""
        <style>
        .stFileUploader > div > div > div {
            padding: 0.5rem !important;
            min-height: 2rem !important;
        }
        
        /* Move entire file uploader upwards */
        .stFileUploader {
            margin-top: -40px !important;
        }
        
        /* File Uploader */
        .stFileUploader > div > div {
            background-color: #f0f5f5 !important;
            color: black !important;
            border: 2px solid #ececec !important;
            border-radius: 8px !important;
        }
        
        /* REDUCED HEIGHT FOR UPLOADED FILE DISPLAY */
        /* Target the uploaded file container */
        .stFileUploader div[data-testid="stFileUploaderFileName"] {
            min-height: 40px !important;
            height: 40px !important;
            padding: 8px 12px !important;
            margin: 4px 0 !important;
            display: flex !important;
            align-items: center !important;
            color: black !important;
            font-size: 12px !important;
            line-height: 1.2 !important;
            background-color: #f0f5f5 !important;
        }
        
        /* Reduce height of the file uploader section after upload */
        .stFileUploader section[data-testid="stFileUploaderDropzone"] {
            min-height: 50px !important;
            height: auto !important;
            padding: 12px !important;
            margin: 6px 0 !important;
            background-color: #f0f5f5 !important;
        }
        
        /* Target any uploaded file display elements */
        .stFileUploader [data-testid="fileUploaderFileName"],
        .stFileUploader [data-testid="stFileUploaderFileName"] > div,
        .stFileUploader div[role="button"] {
            min-height: 40px !important;
            height: 40px !important;
            padding: 8px 12px !important;
            margin: 4px 0 !important;
            line-height: 1.2 !important;
            font-size: 12px !important;
            background-color: #f0f5f5 !important;
        }
        
        /* Compact the entire file uploader when files are uploaded */
        .stFileUploader:has([data-testid="stFileUploaderFileName"]) {
            min-height: 40px !important;
        }
        
        .stFileUploader:has([data-testid="stFileUploaderFileName"]) > div {
            min-height: 40px !important;
            padding: 4px !important;
        }
        
        /* File Uploader - Uploaded file display text (light grey) */
        .stFileUploader div[data-testid="stFileUploaderFileName"],
        .stFileUploader div[data-testid="fileUploaderDropzone"] span,
        .stFileUploader div[data-testid="fileUploaderDropzone"] p,
        .stFileUploader section span,
        .stFileUploader section p,
        .stFileUploader [data-testid="fileUploaderFileName"],
        .stFileUploader small {
            color: black !important; /* Light grey for uploaded file names and text */
            font-size: 12px !important;
            line-height: 1.2 !important;
        }
        
        /* File uploader drag and drop area */
        .stFileUploader section {
            background-color: #f0f5f5 !important;
            border: 2px dashed #ececec !important;
            border-radius: 8px !important;
        }
        
        /* File uploader text content - making it light grey */
        .stFileUploader section div,
        .stFileUploader section span,
        .stFileUploader section small {
            color: black !important; /* Light grey for all file uploader text */
            font-size: 12px !important;
            line-height: 1.2 !important;
        }
        
        /* Fix for uploaded file dark background */
        .stFileUploader div[data-testid="stFileUploaderFileName"],
        .stFileUploader div[data-testid="stFileUploaderFileName"] > div,
        .stFileUploader .uploadedFile,
        .stFileUploader [data-baseweb="file-uploader"] div {
            background-color: #f0f5f5 !important;
            color: black !important;
        }
        
        /* Override any dark backgrounds in file uploader */
        .stFileUploader * {
            background-color: #f0f5f5 !important;
        }
        
        /* Make sure the file name text is visible */
        .stFileUploader span, .stFileUploader small {
            color: black!important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # FILE UPLOAD
        try:
            rfi_document_upload = st.file_uploader(
                label="Upload RFI Document", 
                type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
                key="rfi_document_uploader",
                label_visibility="hidden"
            )
            
            if rfi_document_upload is not None:
                logger.info(f"File uploaded: {rfi_document_upload.name}")
                
        except Exception as e:
            logger.error(f"Error creating file uploader: {str(e)}")
            set_global_message("Upload service temporarily unavailable - Please refresh the page and try again", 'error')
            rfi_document_upload = None
        
        # Show file info and analyze button
        if rfi_document_upload is not None:
            try:
                file_size_kb = round(rfi_document_upload.size / 1024, 1)
                file_size_display = f"{file_size_kb}KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)}MB"
                logger.debug(f"File size: {file_size_display}")
                
                # Single compact row
                col_info, col_btn = st.columns([2.5, 1])
                
                with col_info:
                    st.markdown(f"<span style='font-size:0.8em; color:#ffffff'>📄 {rfi_document_upload.name[:25]}{'...' if len(rfi_document_upload.name) > 25 else ''} ({file_size_display})</span>", 
                                unsafe_allow_html=True)
                
                with col_btn:
                    try:
                        st.markdown(f"""
                        <style>
                        div.stButton > button:first-child {{
                            background-color: #4CAF50;
                            color: #f0f5f5;
                            border: none;
                        }}
                        </style>
                        """, unsafe_allow_html=True)

                        analyze_clicked = st.button(
                            "Get pain points",
                            key="analyze_rfi_document_btn",
                            help="Process RFI document",
                            type="secondary",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        logger.error(f"Error creating analyze button: {str(e)}")
                        set_global_message("Button display issue - Please refresh the page to restore full functionality", 'error')
                        analyze_clicked = False
                
                # Handle analyze button click
                if analyze_clicked:
                    try:
                        if not client_enterprise_name:
                            logger.warning("Analyze clicked but no client enterprise name provided")
                            set_global_message("Client name required - Please enter your client's enterprise name to continue", 'error')
                        else:
                            logger.info("Starting RFI analysis process")
                            set_global_message("Analyzing RFI document... 🔄", "info")
                            
                            # Perform the actual processing
                            try:
                                logger.info("Starting RFI document processing")
                                file_path = save_uploaded_file_and_get_path(rfi_document_upload, logger, client_enterprise_name)
                                
                                if file_path and client_enterprise_name:
                                    logger.info(f"Processing RFI file: {file_path}")
                                    pain_points_data = get_pain_points(file_path, client_enterprise_name)
                                    logger.info(f"Successfully extracted pain points, count: {len(pain_points_data) if pain_points_data else 0}")
                                    
                                    client_state_manager.update_client_data(
                                        uploaded_file_path=file_path,
                                        rfi_pain_points_items=pain_points_data,
                                        document_analyzed=True,
                                        processing_rfi=False
                                    )
                                    set_global_message("✅ RFI document analyzed successfully!", "success")
                                else:
                                    logger.error("Error saving the uploaded file or missing client name")
                                    set_global_message("Upload failed - We couldn't process your file. Please try again or contact support if the issue persists", 'error')
                                    
                            except Exception as e:
                                logger.error(f"Error analyzing RFI document: {str(e)}")
                                set_global_message("Analysis unavailable - We're having trouble analyzing your document right now. Please try uploading again", 'error')
                                client_state_manager.update_client_data(
                                    rfi_pain_points_items={},
                                    document_analyzed=False,
                                    processing_rfi=False
                                )
                                
                    except Exception as e:
                        logger.error(f"Error handling analyze button click: {str(e)}")
                        set_global_message("Analysis initialization failed - Please try again", 'error')
                        
            except Exception as e:
                logger.error(f"Error in file info section: {str(e)}")
                set_global_message("File information display issue - Please refresh the page to restore functionality", 'error')
                
    except Exception as e:
        logger.error(f"Error in file upload section: {str(e)}")
        set_global_message("File upload section temporarily unavailable - Please refresh the page to continue", 'error')


@st.fragment
def render_second_section(logger, client_data, is_locked):
    """Main function to render the second section with two columns"""
    col3, col4 = st.columns([1, 1])
        
    with col3:
        doc_upload_section(logger, client_data, is_locked)
    
    with col4:
        client_name_provided = enterprise_content(logger, client_data, is_locked)
    
    return client_name_provided

@st.fragment
def render_client_requirements_section(logger, client_data, is_locked):
    """Render the client requirements section (left column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    try:
        logger.debug("Processing client requirements section")
        
        st.markdown('''
        <div class="tooltip-label">
            Client Requirements <span style="color:red;">*</span>
            <div class="tooltip-icon" data-tooltip="Define the core client requirements, technical specifications, project scope, deliverables, and expected outcomes. This forms the foundation of your proposal and helps ensure all client needs are addressed.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        try:
            client_requirements = st.text_area(
                label="Client Requirements", 
                value=client_data.client_requirements_content if client_name_provided else "", 
                height=200, 
                key="client_requirements_textarea",
                label_visibility="collapsed",
                disabled=not client_name_provided or is_locked,
                placeholder="Enter client name first to enable this field" if not client_name_provided else "Add your client requirements here you may take suggestions from AI in the right as well"
            )
            
            # Update the client data when the text area changes (only if enabled)
            if client_name_provided:
                try:
                    client_state_manager.update_client_data(client_requirements_content=client_requirements)
                    logger.debug("Updated client requirements content")
                except Exception as e:
                    logger.error(f"Error updating client requirements: {str(e)}")
                    set_global_message("Save failed - Your client requirements couldn't be saved. Please try again")
            
            client_requirements_provided = bool(client_name_provided and client_requirements.strip())
            logger.debug(f"Client requirements provided: {client_requirements_provided}")
            
        except Exception as e:
            logger.error(f"Error creating client requirements textarea: {str(e)}")
            set_global_message("Requirements editor unavailable - Please refresh the page to restore functionality")
            client_requirements = ""
            client_requirements_provided = False
            
    except Exception as e:
        logger.error(f"Error in client requirements section: {str(e)}")
        set_global_message("Requirements section temporarily unavailable - Please refresh the page to continue")


@st.fragment
def render_client_pain_points_section(logger, client_data, is_locked):
    """Render the client pain points section (right column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    try:
        logger.info("Starting client pain points section rendering")
        
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Client Pain Points
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        try:
            # Get RFI pain points items from client data or use dummy data
            if client_name_provided and client_data.rfi_pain_points_items:
                rfi_pain_points_items = client_data.rfi_pain_points_items
                logger.info(f"Using client RFI pain points data with {len(rfi_pain_points_items)} items")
            else:
                # Dummy data when no client name or no file uploaded
                rfi_pain_points_items = {
                    "Revenue Challenges": "**Revenue Challenges** • Sales declined by XX year-over-year despite market growth\n• Missed quarterly revenue targets by XX for three consecutive quarters\n• Average deal size decreased by XX due to increased price competition\n• Customer churn rate increased to XX, up from XX previous year\n• Revenue per customer dropped XX as clients downgraded service tiers\n• New product launches generated only XX of projected revenue\n• Seasonal revenue fluctuations creating XX variance between peak and low periods\n• Pipeline conversion rates fell from XX to XX over past XX months\n\n",

                    "Cost and Margin Pressure": "**Cost and Margin Pressure** • Cost of Goods Sold increased by XX due to supply chain disruptions\n• Labor costs rose XX while productivity remained flat\n• Raw material prices up XX with limited ability to pass costs to customers\n• Operational efficiency decreased by XX due to outdated processes\n• Procurement costs increased XX from supplier consolidation issues\n• Technology infrastructure costs grew XX without proportional business benefits\n• Regulatory compliance expenses added XX in unexpected annual costs\n• Facility and overhead costs up XX while revenue remained stagnant\n\n",

                    "Market Expansion and Customer Acquisition": "**Market Expansion and Customer Acquisition**\n\n • Win rate on new business opportunities dropped from XX to XX\n• Customer acquisition cost increased XX while customer lifetime value declined\n• Expansion into new geographic markets yielding only XX of projected results\n• Lack of local market knowledge resulting in XX longer sales cycles\n• Digital marketing campaigns generating XX fewer qualified leads\n• Competition from new market entrants capturing XX of target customer segment\n• Limited brand recognition in new markets requiring XX marketing investment\n• Difficulty penetrating enterprise accounts with average sales cycle extending to XX months\n\n"
                }
                logger.info("Using dummy pain points data as fallback")

        except Exception as e:
            logger.error(f"Error retrieving pain points data: {str(e)}")
            set_global_message("Data loading issue - We're having trouble loading your pain points. Please refresh the page")
            rfi_pain_points_items = {}

        # Use a single container for all pain points items
        try:
            with st.container():
                logger.debug(f"Rendering {len(rfi_pain_points_items)} pain point items")
                
                # Display pain points items with add/remove buttons
                for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                    try:
                        logger.debug(f"Processing pain point item {i}: {key}")
                        
                        # Check if this item is selected
                        try:
                            is_selected = key in client_data.selected_pain_points
                            logger.debug(f"Pain point '{key}' selection status: {is_selected}")
                        except Exception as e:
                            logger.error(f"Error checking selection status for '{key}': {str(e)}")
                            set_global_message("Selection status check failed - Please refresh the page")
                            is_selected = False
                        
                        # Create a box container with +/- button and content on same horizontal level
                        col_add, col_content = st.columns([0.5, 9], gap="medium")
                        
                        with col_add:
                            try:
                                # Style the button to align vertically with the content box
                                st.markdown("""
        <style>
        /* Force override all button styling */
        button[kind="secondary"] {
            height: 48px !important;
            border: 2.2px solid #ececec !important;
            border-radius: 4px !important;
            margin-top: -5px !important;  /* Move button up */
            transform: translateY(-3px) !important;  /* Additional upward adjustment */
            background-color: #d3d3d3 !important;  
            color: black !important;  /* black text */
        }
            
        button[kind="secondary"]:hover {
            border: 2.2px solid #ececec !important;
            transform: translateY(-3px) !important;  /* Keep position on hover */
            background-color: #d3d3d3 !important;  /* Slightly lighter on hover */
            color: black !important;  /* Keep black text on hover */
        }
            
        button[kind="secondary"]:focus {
            border: 2.2px solid #ececec !important;
            outline: 2px solid #ececec !important;
            transform: translateY(-3px) !important;  /* Keep position on focus */
            background-color: #d3d3d3 !important;  /* Keep dark background on focus */
            color: black !important;  /* Keep black text on focus */
        }
            
        /* Try targeting by data attributes */
        [data-testid] button {
            border: 2.2px solid #ececec !important;
            height: 48px !important;
            margin-top: -5px !important;  /* Move button up */
            transform: translateY(-2.5px) !important;  /* Additional upward adjustment */
            background-color: #d3d3d3 !important;  /* Dark greyish background */
            color: black !important;  /* black text */
        }
        
        /* Additional targeting for button text specifically */
        button[kind="secondary"] p,
        button[kind="secondary"] span,
        button[kind="secondary"] div {
            color: black !important;
        }
        
        [data-testid] button p,
        [data-testid] button span,
        [data-testid] button div {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)  
                                button_text = "❌" if is_selected else "➕"
                                button_help = f"Remove '{key}' from client requirements" if is_selected else f"Add '{key}' to client requirements section"
                                button_type = "secondary" 
                                
                                if st.button(button_text, 
                                        key=f"toggle_rfi_pain_point_item_{i}", 
                                        help=button_help,
                                        type=button_type,
                                        disabled=not client_name_provided or is_locked):
                                    
                                    logger.info(f"Pain point button clicked for '{key}', current selection: {is_selected}")
                                    
                                    try:
                                        if is_selected:
                                            # REMOVE FUNCTIONALITY
                                            logger.info(f"Removing pain point '{key}' from requirements")
                                            
                                            try:
                                                # Get current content from the client data
                                                current_content = client_data.client_requirements_content
                                                logger.debug(f"Current content length: {len(current_content) if current_content else 0}")
                                                
                                                # Get the original content that was added for this key
                                                original_content = client_data.pain_point_content_map.get(key, value)
                                                logger.debug(f"Original content to remove length: {len(original_content)}")
                                                
                                                # Remove this specific pain point section from content
                                                patterns_to_remove = [
                                                    f"\n\n{original_content}",
                                                    f"{original_content}\n\n",
                                                    original_content
                                                ]
                                                
                                                updated_content = current_content
                                                for pattern in patterns_to_remove:
                                                    if pattern in updated_content:
                                                        updated_content = updated_content.replace(pattern, "")
                                                        logger.debug(f"Removed pattern from content")
                                                        break
                                                
                                                # Clean up any excessive newlines
                                                updated_content = '\n\n'.join([section.strip() for section in updated_content.split('\n\n') if section.strip()])
                                                
                                                # Update client data
                                                client_data.selected_pain_points.discard(key)
                                                if key in client_data.pain_point_content_map:
                                                    del client_data.pain_point_content_map[key]
                                                
                                                client_state_manager.update_client_data(
                                                    client_requirements_content=updated_content,
                                                    selected_pain_points=client_data.selected_pain_points,
                                                    pain_point_content_map=client_data.pain_point_content_map
                                                )
                                                
                                                logger.info(f"Successfully removed pain point '{key}'")
                                                
                                            except Exception as e:
                                                logger.error(f"Error in remove functionality for '{key}': {str(e)}")
                                                set_global_message("Item removal failed - Couldn't remove the selected item. Please try again")
                                            
                                        else:
                                            # ADD FUNCTIONALITY
                                            logger.info(f"Adding pain point '{key}' to requirements")
                                            
                                            try:
                                                # Get current content from client data
                                                current_content = client_data.client_requirements_content
                                                logger.debug(f"Current content length before add: {len(current_content) if current_content else 0}")
                                                
                                                # Append the value to the content
                                                new_content = current_content + f"\n\n{value}" if current_content else value
                                                logger.debug(f"New content length after add: {len(new_content)}")
                                                
                                                # Update client data
                                                client_data.selected_pain_points.add(key)
                                                client_data.pain_point_content_map[key] = value
                                                
                                                client_state_manager.update_client_data(
                                                    client_requirements_content=new_content,
                                                    selected_pain_points=client_data.selected_pain_points,
                                                    pain_point_content_map=client_data.pain_point_content_map
                                                )
                                                
                                                logger.info(f"Successfully added pain point '{key}'")
                                                
                                            except Exception as e:
                                                logger.error(f"Error in add functionality for '{key}': {str(e)}")
                                                set_global_message("Item addition failed - Couldn't add the selected item. Please try again")
                                        
                                        st.rerun()
                                        
                                    except Exception as e:
                                        logger.error(f"Error handling button click for '{key}': {str(e)}")
                                        set_global_message("Selection update failed - Please try your selection again")
                                        
                            except Exception as e:
                                logger.error(f"Error rendering button for pain point '{key}': {str(e)}")
                                set_global_message("Button display issue - Please refresh the page to restore full functionality")

                        with col_content:
                            try:
                                # Style the content box based on selection state
                                if is_selected:
                                    background_color = "#DCEBD6"
                                    border_color = "#ececec"
                                    text_color = "#000000"
                                    icon = "✅"
                                    box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                                else:
                                    background_color = "#f5f5f5"
                                    border_color = "#ececec"
                                    text_color = "#000000"
                                    icon = "📋"
                                    box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
                                
                                st.markdown(f"""
                                <div style="
                                    padding: 12px;
                                    border-radius: 6px;
                                    margin: 5px 0;
                                    background-color: {background_color};
                                    border: 2px solid {border_color};
                                    color: {text_color};
                                    font-weight: 500;
                                    box-shadow: {box_shadow};
                                    min-height: 24px;
                                    display: flex;
                                    align-items: center;
                                    transition: all 0.3s ease;
                                ">
                                    {icon} {key}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                logger.debug(f"Successfully rendered content box for '{key}'")
                                
                            except Exception as e:
                                logger.error(f"Error rendering content box for '{key}': {str(e)}")
                                set_global_message("Content display issue - Please refresh the page to restore full functionality")
                                
                    except Exception as e:
                        logger.error(f"Error processing pain point item {i} ('{key}'): {str(e)}")
                        set_global_message("Processing error - We couldn't process your selection. Please try again")
                        
        except Exception as e:
            logger.error(f"Error rendering pain points container: {str(e)}")
            set_global_message("Pain points section unavailable - Please refresh the page to restore functionality")
            
    except Exception as e:
        logger.error(f"Critical error in pain points section rendering: {str(e)}")
        set_global_message("Service interruption - We're experiencing technical difficulties. Please refresh the page or contact support")


@st.fragment
def render_third_section(logger, client_data, is_locked):
    """Main function to render both client requirements and pain points sections"""
    col5, col6 = st.columns([1, 1])

    with col5:
        render_client_requirements_section(logger, client_data, is_locked)
    
    with col6:
        render_client_pain_points_section(logger, client_data, is_locked)

@st.fragment
def render_spoc_name_section(logger, client_data, is_locked):
    """Render the SPOC name input section (left column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    try:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Name
            <div class="tooltip-icon" data-tooltip="Enter the Single Point of Contact (SPOC) name - the primary person responsible for communication and decision-making on the client side. This person will be your main contact throughout the project lifecycle.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        spoc_name = st.text_input(
            on_change=lambda : None,
            label="SPOC Name", 
            value=client_data.spoc_name,
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input",
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked
        )
        
        # Update client data when SPOC name changes
        if spoc_name != client_data.spoc_name:
            try:
                client_state_manager.update_client_data(spoc_name=spoc_name)
                logger.debug(f"Updated SPOC name to: {spoc_name}")
            except Exception as e:
                logger.error(f"Error updating SPOC name: {str(e)}")
                set_global_message("Failed to save SPOC name - Please try again")
        
        # Automatically search for LinkedIn profiles when SPOC name changes
        if spoc_name and spoc_name.strip() and spoc_name != client_data.last_searched_spoc and client_name_provided:
            try:
                set_global_message(f"Searching LinkedIn profiles for {spoc_name}...")
                logger.info(f"Searching LinkedIn profiles for SPOC: {spoc_name}")
                
                # Search for LinkedIn profiles
                linkedin_profiles_raw = get_linkedin(spoc_name.strip())
                
                # Process LinkedIn profiles - handle both list and dict formats
                processed_profiles = {}
                if linkedin_profiles_raw:
                    if isinstance(linkedin_profiles_raw, list):
                        # Handle list format - merge all dictionaries
                        for profile_dict in linkedin_profiles_raw:
                            if isinstance(profile_dict, dict):
                                processed_profiles.update(profile_dict)
                    elif isinstance(linkedin_profiles_raw, dict):
                        # Handle direct dictionary format
                        processed_profiles = linkedin_profiles_raw
                    
                    logger.info(f"Found {len(processed_profiles)} LinkedIn profiles")
                else:
                    set_global_message("No LinkedIn profiles found", "info")
                    logger.info("No LinkedIn profiles found for SPOC")
                
                try:
                    client_state_manager.update_client_data(
                        linkedin_profiles=processed_profiles,
                        last_searched_spoc=spoc_name
                    )
                    logger.debug("Updated client data with LinkedIn profiles")
                except Exception as e:
                    logger.error(f"Error updating LinkedIn profiles: {str(e)}")
                    set_global_message("Failed to save LinkedIn profiles - Please try searching again")
                
                st.rerun()
                
            except Exception as e:
                logger.error(f"Error searching LinkedIn profiles: {str(e)}")
                set_global_message("LinkedIn search failed - Please try again or check your connection")
                
    except Exception as e:
        logger.error(f"Error in SPOC name section: {str(e)}")
        set_global_message("SPOC name section unavailable - Please refresh the page")
    
    return spoc_name


@st.fragment
def render_linkedin_profile_section(logger, client_data, is_locked, spoc_name):
    """Render the LinkedIn profile selection section (right column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    spoc_name_provided = bool(spoc_name and spoc_name.strip()) and client_name_provided
    
    try:
        st.markdown('''
        <div class="tooltip-label">
            Select SPOC LinkedIn Profile
            <div class="tooltip-icon" data-tooltip="Enter or select the LinkedIn profile URL of the SPOC. This helps in understanding their professional background, expertise, and communication style for better relationship building.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        spoc_linkedin_profile = None
        
        # Prepare LinkedIn profile options
        if spoc_name_provided and client_data.linkedin_profiles:
            try:
                # Create options with profile titles for better selection
                linkedin_options = ["Select a LinkedIn profile..."]
                linkedin_url_mapping = {}  # To map display text to actual URL
                
                for url, profile_data in client_data.linkedin_profiles.items():
                    # Handle both old and new profile data formats
                    if isinstance(profile_data, dict):
                        name = profile_data.get('name', 'Unknown')
                        role = profile_data.get('role', 'Unknown Role')
                        display_text = f"{name} - {role}"
                    else:
                        # Fallback for unexpected format
                        display_text = f"Profile: {str(profile_data)}"
                    
                    linkedin_options.append(display_text)
                    linkedin_url_mapping[display_text] = url
                
                selected_linkedin_display = st.selectbox(
                    label="SPOC LinkedIn Profile",
                    options=linkedin_options,
                    key="spoc_linkedin_profile_selector",
                    label_visibility="collapsed",
                    disabled=not client_name_provided or is_locked,
                    accept_new_options=True,
                )
                
                # Extract the actual URL from the selected option
                if selected_linkedin_display != "Select a LinkedIn profile...":
                    spoc_linkedin_profile = linkedin_url_mapping.get(selected_linkedin_display)
                    if spoc_linkedin_profile:
                        try:
                            client_state_manager.update_client_data(spoc_linkedin_profile=spoc_linkedin_profile)
                            logger.debug(f"Updated SPOC LinkedIn profile: {spoc_linkedin_profile}")
                        except Exception as e:
                            logger.error(f"Error updating SPOC LinkedIn profile: {str(e)}")
                            set_global_message("Failed to save LinkedIn profile selection - Please try again")
                else:
                    spoc_linkedin_profile = None
                    
            except Exception as e:
                logger.error(f"Error processing LinkedIn profile options: {str(e)}")
                set_global_message("LinkedIn profile options unavailable - Please refresh the page")
                
        elif spoc_name_provided and not client_data.linkedin_profiles:
            # Show message when no profiles found
            st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["No LinkedIn profiles found. Try a different name."],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=is_locked,
                accept_new_options=True
            )
            spoc_linkedin_profile = None
        else:
            # Default disabled state
            spoc_linkedin_profile = st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["Enter SPOC name to get LinkedIn profiles"],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=is_locked or not spoc_name_provided,
                accept_new_options=True
            )
            
    except Exception as e:
        logger.error(f"Error in LinkedIn profile section: {str(e)}")
        set_global_message("LinkedIn profile section unavailable - Please refresh the page")
    
    return spoc_linkedin_profile


@st.fragment
def render_selected_profile_info(logger, client_data, spoc_name_provided, spoc_linkedin_profile):
    """Render the selected profile information and handle dynamic updates"""
    try:
        # Display selected profile information and handle dynamic updates
        if spoc_name_provided and client_data.linkedin_profiles:
            # Check if LinkedIn profile selection has changed
            profile_changed = False
            if spoc_linkedin_profile:
                if client_data.current_selected_profile_url != spoc_linkedin_profile:
                    try:
                        client_state_manager.update_client_data(current_selected_profile_url=spoc_linkedin_profile)
                        profile_changed = True
                        logger.info(f"Profile changed to: {spoc_linkedin_profile}")
                    except Exception as e:
                        logger.error(f"Error updating current selected profile URL: {str(e)}")
                        set_global_message("Failed to update profile selection - Please try again")
                        
                selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
                if selected_profile_data and isinstance(selected_profile_data, dict):
                    try:
                        name = selected_profile_data.get('name', 'Unknown')
                        role = selected_profile_data.get('role', 'Unknown Role')
                        st.markdown(f'''
<div style="text-align: center; margin-top: 10px;">
    <a href="{spoc_linkedin_profile}" target="_blank" style="color: #0077b5; font-weight: 500; text-decoration: none;">
        Visit LinkedIn
    </a>
</div>
''', unsafe_allow_html=True)

                        
                        logger.debug(f"Displayed profile info for: {name}")
                        
                    except Exception as e:
                        logger.error(f"Error displaying profile info: {str(e)}")
                        set_global_message("Profile display error - Please refresh the page")
                
                # Update roles and priorities when profile changes
                if profile_changed:
                    try:
                        # Remove previously auto-populated LinkedIn role if it exists
                        linkedin_roles_to_remove = []
                        if hasattr(client_data, 'selected_target_roles') and isinstance(client_data.selected_target_roles, list):
                            for i, existing_role in enumerate(client_data.selected_target_roles):
                                # Check if this role was from a previous LinkedIn profile
                                for url, profile in client_data.linkedin_profiles.items():
                                    if (url != spoc_linkedin_profile and 
                                        isinstance(profile, dict) and 
                                        profile.get('role') == existing_role):
                                        linkedin_roles_to_remove.append(i)
                                        break
                        
                            # Remove old LinkedIn roles
                            for idx in reversed(linkedin_roles_to_remove):
                                client_data.selected_target_roles.pop(idx)
                        
                        # Add new LinkedIn role
                        linkedin_role = selected_profile_data.get('role')
                        if linkedin_role:
                            if not hasattr(client_data, 'selected_target_roles'):
                                client_data.selected_target_roles = []
                            if linkedin_role not in client_data.selected_target_roles:
                                client_data.selected_target_roles.append(linkedin_role)
                        
                        # Remove old LinkedIn priorities and add new ones
                        if hasattr(client_data, 'selected_business_priorities') and isinstance(client_data.selected_business_priorities, list):
                            linkedin_priorities_to_remove = []
                            for priority in client_data.selected_business_priorities:
                                # Check if this priority was from a previous LinkedIn profile
                                for url, profile in client_data.linkedin_profiles.items():
                                    if (url != spoc_linkedin_profile and 
                                        isinstance(profile, dict) and 
                                        priority in profile.get('top_3_priorities', [])):
                                        linkedin_priorities_to_remove.append(priority)
                                        break
                            
                            # Remove old LinkedIn priorities
                            for priority in linkedin_priorities_to_remove:
                                if priority in client_data.selected_business_priorities:
                                    client_data.selected_business_priorities.remove(priority)
                        
                        # Add new LinkedIn priorities
                        inferred_priorities = selected_profile_data.get('top_3_priorities', [])
                        if not hasattr(client_data, 'selected_business_priorities'):
                            client_data.selected_business_priorities = []
                        
                        for priority in inferred_priorities:
                            if priority not in client_data.selected_business_priorities:
                                client_data.selected_business_priorities.append(priority)
                        
                        # Update client data
                        client_state_manager.update_client_data(
                            selected_target_roles=getattr(client_data, 'selected_target_roles', []),
                            selected_business_priorities=getattr(client_data, 'selected_business_priorities', [])
                        )
                        
                        logger.info("Updated target roles and business priorities based on LinkedIn profile")
                        
                        # Force rerun to update the display
                        st.rerun()
                        
                    except Exception as e:
                        logger.error(f"Error updating roles and priorities: {str(e)}")
                        set_global_message("Failed to update roles and priorities - Please try again")
                        
            elif hasattr(client_data, 'current_selected_profile_url') and client_data.current_selected_profile_url is not None:
                # Profile was deselected
                try:
                    client_state_manager.update_client_data(current_selected_profile_url=None)
                    profile_changed = True
                    logger.info("Profile deselected")
                except Exception as e:
                    logger.error(f"Error clearing selected profile: {str(e)}")
                    set_global_message("Failed to clear profile selection - Please try again")
                    
    except Exception as e:
        logger.error(f"Error in selected profile info section: {str(e)}")
        set_global_message("Profile information section unavailable - Please refresh the page")
@st.fragment
def render_spoc_name_section(logger, client_data, is_locked):
    """Render the SPOC name input section (left column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    try:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Name
            <div class="tooltip-icon" data-tooltip="Enter the Single Point of Contact (SPOC) name - the primary person responsible for communication and decision-making on the client side. This person will be your main contact throughout the project lifecycle.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create two columns for SPOC name input and LinkedIn button
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            spoc_name = st.text_input(
                on_change=lambda : None,
                label="SPOC Name", 
                value=client_data.spoc_name,
                placeholder="Enter SPOC full name...", 
                key="spoc_name_input",
                label_visibility="collapsed",
                disabled=not client_name_provided or is_locked
            )
        
        with col2:
            # LinkedIn search button - only enabled when SPOC name is provided
            linkedin_button_disabled = (not spoc_name or not spoc_name.strip() or 
                                       not client_name_provided or is_locked)
            
            if st.button(
                "Get LinkedIn",
                key="get_linkedin_button",
                disabled=linkedin_button_disabled,
                help="Search for LinkedIn profiles of the SPOC"
            ):
                # Handle LinkedIn profile search when button is clicked
                try:
                    set_global_message(f"Searching LinkedIn profiles for {spoc_name}...")
                    logger.info(f"Searching LinkedIn profiles for SPOC: {spoc_name}")
                    
                    # Search for LinkedIn profiles
                    linkedin_profiles_raw = get_linkedin(spoc_name.strip())
                    
                    # Process LinkedIn profiles - handle both list and dict formats
                    processed_profiles = {}
                    if linkedin_profiles_raw:
                        if isinstance(linkedin_profiles_raw, list):
                            # Handle list format - merge all dictionaries
                            for profile_dict in linkedin_profiles_raw:
                                if isinstance(profile_dict, dict):
                                    processed_profiles.update(profile_dict)
                        elif isinstance(linkedin_profiles_raw, dict):
                            # Handle direct dictionary format
                            processed_profiles = linkedin_profiles_raw
                        
                        logger.info(f"Found {len(processed_profiles)} LinkedIn profiles")
                    else:
                        set_global_message("No LinkedIn profiles found", "info")
                        logger.info("No LinkedIn profiles found for SPOC")
                    
                    try:
                        client_state_manager.update_client_data(
                            linkedin_profiles=processed_profiles,
                            last_searched_spoc=spoc_name
                        )
                        logger.debug("Updated client data with LinkedIn profiles")
                    except Exception as e:
                        logger.error(f"Error updating LinkedIn profiles: {str(e)}")
                        set_global_message("Failed to save LinkedIn profiles - Please try searching again")
                    
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error searching LinkedIn profiles: {str(e)}")
                    set_global_message("LinkedIn search failed - Please try again or check your connection")
        
        # Update client data when SPOC name changes
        if spoc_name != client_data.spoc_name:
            try:
                client_state_manager.update_client_data(spoc_name=spoc_name)
                logger.debug(f"Updated SPOC name to: {spoc_name}")
            except Exception as e:
                logger.error(f"Error updating SPOC name: {str(e)}")
                set_global_message("Failed to save SPOC name - Please try again")
    
    except Exception as e:
        logger.error(f"Error in SPOC name section: {str(e)}")
        set_global_message("SPOC name section unavailable - Please refresh the page")
    
    return spoc_name


@st.fragment
def render_linkedin_profile_section(logger, client_data, is_locked, spoc_name):
    """Render the LinkedIn profile selection section (right column)"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    spoc_name_provided = bool(spoc_name and spoc_name.strip()) and client_name_provided
    
    try:
        st.markdown('''
        <div class="tooltip-label">
            Select SPOC LinkedIn Profile
            <div class="tooltip-icon" data-tooltip="Enter or select the LinkedIn profile URL of the SPOC. This helps in understanding their professional background, expertise, and communication style for better relationship building.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        spoc_linkedin_profile = None
        
        # Prepare LinkedIn profile options
        if spoc_name_provided and client_data.linkedin_profiles:
            try:
                # Create options with profile titles for better selection
                linkedin_options = ["Select a LinkedIn profile..."]
                linkedin_url_mapping = {}  # To map display text to actual URL
                
                for url, profile_data in client_data.linkedin_profiles.items():
                    # Handle both old and new profile data formats
                    if isinstance(profile_data, dict):
                        name = profile_data.get('name', 'Unknown')
                        role = profile_data.get('role', 'Unknown Role')
                        display_text = f"{name} - {role}"
                    else:
                        # Fallback for unexpected format
                        display_text = f"Profile: {str(profile_data)}"
                    
                    linkedin_options.append(display_text)
                    linkedin_url_mapping[display_text] = url
                
                selected_linkedin_display = st.selectbox(
                    label="SPOC LinkedIn Profile",
                    options=linkedin_options,
                    key="spoc_linkedin_profile_selector",
                    label_visibility="collapsed",
                    disabled= not client_name_provided or is_locked,
                    accept_new_options=True,
                )
                



                # Extract the actual URL from the selected option
                if selected_linkedin_display != "Select a LinkedIn profile...":
                    spoc_linkedin_profile = linkedin_url_mapping.get(selected_linkedin_display)
                    if spoc_linkedin_profile:
                        try:
                            client_state_manager.update_client_data(spoc_linkedin_profile=spoc_linkedin_profile)
                            logger.debug(f"Updated SPOC LinkedIn profile: {spoc_linkedin_profile}")
                        except Exception as e:
                            logger.error(f"Error updating SPOC LinkedIn profile: {str(e)}")
                            set_global_message("Failed to save LinkedIn profile selection - Please try again")
                else:
                    spoc_linkedin_profile = None
                    
            except Exception as e:
                logger.error(f"Error processing LinkedIn profile options: {str(e)}")
                set_global_message("LinkedIn profile options unavailable - Please refresh the page")
                
        elif spoc_name_provided and not client_data.linkedin_profiles:
            # Show message when no profiles found
            st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["No LinkedIn profiles found. Try a different name."],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=is_locked,
                accept_new_options=True
            )
            spoc_linkedin_profile = None
        else:
            # Default disabled state
            spoc_linkedin_profile = st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["Enter SPOC name to get LinkedIn profiles"],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=is_locked or not spoc_name_provided,
                accept_new_options=True
            )
            
    except Exception as e:
        logger.error(f"Error in LinkedIn profile section: {str(e)}")
        set_global_message("LinkedIn profile section unavailable - Please refresh the page")
    
    return spoc_linkedin_profile


@st.fragment
def render_selected_profile_info(logger, client_data, spoc_name_provided, spoc_linkedin_profile):
    """Render the selected profile information and handle dynamic updates"""
    try:
        # Display selected profile information and handle dynamic updates
        if spoc_name_provided and client_data.linkedin_profiles:
            # Check if LinkedIn profile selection has changed
            profile_changed = False
            if spoc_linkedin_profile:
                if client_data.current_selected_profile_url != spoc_linkedin_profile:
                    try:
                        client_state_manager.update_client_data(current_selected_profile_url=spoc_linkedin_profile)
                        profile_changed = True
                        logger.info(f"Profile changed to: {spoc_linkedin_profile}")
                    except Exception as e:
                        logger.error(f"Error updating current selected profile URL: {str(e)}")
                        set_global_message("Failed to update profile selection - Please try again")
                        
                selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
                if selected_profile_data and isinstance(selected_profile_data, dict):
                    try:
                        name = selected_profile_data.get('name', 'Unknown')
                        role = selected_profile_data.get('role', 'Unknown Role')
                        st.markdown(f'<div style="text-align: right;"><a href="{spoc_linkedin_profile}" target="_blank">Visit LinkedIn profile</a></div>', unsafe_allow_html=True)
                        logger.debug(f"Displayed profile info for: {name}")
                        
                    except Exception as e:
                        logger.error(f"Error displaying profile info: {str(e)}")
                        set_global_message("Profile display error - Please refresh the page")
                
                # Update roles and priorities when profile changes
                if profile_changed:
                    try:
                        # Remove previously auto-populated LinkedIn role if it exists
                        linkedin_roles_to_remove = []
                        if hasattr(client_data, 'selected_target_roles') and isinstance(client_data.selected_target_roles, list):
                            for i, existing_role in enumerate(client_data.selected_target_roles):
                                # Check if this role was from a previous LinkedIn profile
                                for url, profile in client_data.linkedin_profiles.items():
                                    if (url != spoc_linkedin_profile and 
                                        isinstance(profile, dict) and 
                                        profile.get('role') == existing_role):
                                        linkedin_roles_to_remove.append(i)
                                        break
                        
                            # Remove old LinkedIn roles
                            for idx in reversed(linkedin_roles_to_remove):
                                client_data.selected_target_roles.pop(idx)
                        
                        # Add new LinkedIn role
                        linkedin_role = selected_profile_data.get('role')
                        if linkedin_role:
                            if not hasattr(client_data, 'selected_target_roles'):
                                client_data.selected_target_roles = []
                            if linkedin_role not in client_data.selected_target_roles:
                                client_data.selected_target_roles.append(linkedin_role)
                        
                        # Remove old LinkedIn priorities and add new ones
                        if hasattr(client_data, 'selected_business_priorities') and isinstance(client_data.selected_business_priorities, list):
                            linkedin_priorities_to_remove = []
                            for priority in client_data.selected_business_priorities:
                                # Check if this priority was from a previous LinkedIn profile
                                for url, profile in client_data.linkedin_profiles.items():
                                    if (url != spoc_linkedin_profile and 
                                        isinstance(profile, dict) and 
                                        priority in profile.get('top_3_priorities', [])):
                                        linkedin_priorities_to_remove.append(priority)
                                        break
                            
                            # Remove old LinkedIn priorities
                            for priority in linkedin_priorities_to_remove:
                                if priority in client_data.selected_business_priorities:
                                    client_data.selected_business_priorities.remove(priority)
                        
                        # Add new LinkedIn priorities
                        inferred_priorities = selected_profile_data.get('top_3_priorities', [])
                        if not hasattr(client_data, 'selected_business_priorities'):
                            client_data.selected_business_priorities = []
                        
                        for priority in inferred_priorities:
                            if priority not in client_data.selected_business_priorities:
                                client_data.selected_business_priorities.append(priority)
                        
                        # Update client data
                        client_state_manager.update_client_data(
                            selected_target_roles=getattr(client_data, 'selected_target_roles', []),
                            selected_business_priorities=getattr(client_data, 'selected_business_priorities', [])
                        )
                        
                        logger.info("Updated target roles and business priorities based on LinkedIn profile")
                        
                        # Force rerun to update the display
                        st.rerun()
                        
                    except Exception as e:
                        logger.error(f"Error updating roles and priorities: {str(e)}")
                        set_global_message("Failed to update roles and priorities - Please try again")
                        
            elif hasattr(client_data, 'current_selected_profile_url') and client_data.current_selected_profile_url is not None:
                # Profile was deselected
                try:
                    client_state_manager.update_client_data(current_selected_profile_url=None)
                    profile_changed = True
                    logger.info("Profile deselected")
                except Exception as e:
                    logger.error(f"Error clearing selected profile: {str(e)}")
                    set_global_message("Failed to clear profile selection - Please try again")
                    
    except Exception as e:
        logger.error(f"Error in selected profile info section: {str(e)}")
        set_global_message("Profile information section unavailable - Please refresh the page")


@st.fragment
def render_fourth_section(logger, is_locked, client_data):
    """Main function to render both SPOC name and LinkedIn profile sections"""
    try:
        col_spoc1, col_spoc2 = st.columns([1, 1])

        with col_spoc1:
            spoc_name = render_spoc_name_section(logger, client_data, is_locked)

        with col_spoc2:
            spoc_linkedin_profile = render_linkedin_profile_section(logger, client_data, is_locked, spoc_name)

        # Render selected profile information below the columns
        spoc_name_provided = bool(spoc_name and spoc_name.strip()) and bool(client_data.enterprise_name and client_data.enterprise_name.strip())
        render_selected_profile_info(logger, client_data, spoc_name_provided, spoc_linkedin_profile)

        return spoc_name_provided, spoc_linkedin_profile
        
    except Exception as e:
        logger.error(f"Critical error in fourth section rendering: {str(e)}")
        set_global_message("Service interruption - We're experiencing technical difficulties. Please refresh the page or contact support")
        return False, None
    
@st.fragment
def render_spoc_role_section(spoc_name_provided, spoc_linkedin_profile, client_data, logger, is_locked):
    """Render the SPOC Role selection section"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    st.markdown("""
    <style>
    .push-down {
        transform: translateY(10px);
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown('''
    <div class="tooltip-label">
        SPOC Role 
        <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ⓘ</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .push-down {
        transform: translateY(0.3px);
    }
    </style>
""", unsafe_allow_html=True)
    # Prepare role options for dropdown based on LinkedIn profile selection
    role_options = ["Select a role..."]
    
    # Get default roles from function (assuming this function exists)
    target_roles_list = get_roles_list() or []
    
    # Check if a LinkedIn profile is selected
    selected_linkedin_role = None
    if (spoc_name_provided and 
        client_data.linkedin_profiles and 
        'spoc_linkedin_profile' in locals() and 
        spoc_linkedin_profile):
        
        # Get the selected LinkedIn profile data
        selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
        if selected_profile_data and isinstance(selected_profile_data, dict):
            selected_linkedin_role = selected_profile_data.get('role')
            if selected_linkedin_role:
                # Show LinkedIn profile role + default roles from get_roles_list()
                role_options = ["Select a role...", selected_linkedin_role]
                # Add default roles, avoiding duplicates
                for role in target_roles_list:
                    if role not in role_options:
                        role_options.append(role)
    
    # If no LinkedIn profile selected, show all available roles
    if not selected_linkedin_role:
        # Add standard roles from get_roles_list()
        role_options.extend(target_roles_list)
        
        # Add LinkedIn roles if available (but no specific profile selected)
        if spoc_name_provided and client_data.linkedin_profiles:
            for url, profile_data in client_data.linkedin_profiles.items():
                if isinstance(profile_data, dict):
                    linkedin_role = profile_data.get('role')
                    if linkedin_role and linkedin_role not in role_options:
                        role_options.append(linkedin_role)

    # Determine the default/current value for the selectbox
    current_selection = "Select a role..."
    if selected_linkedin_role and selected_linkedin_role in role_options:
        # Auto-select the LinkedIn role
        current_selection = selected_linkedin_role
    elif "target_role_selector_dropdown" in st.session_state:
        # Keep the current selection if it exists in options
        current_value = st.session_state["target_role_selector_dropdown"]
        if current_value in role_options:
            current_selection = current_value

    # ROLES DROPDOWN - Only one role can be selected
    selected_target_role = st.selectbox(
        label="Target Role Selector", 
        options=role_options,
        index=role_options.index(current_selection) if current_selection in role_options else 0,
        key="target_role_selector_dropdown",
        label_visibility="collapsed",
        disabled=not (client_name_provided and spoc_name_provided) or is_locked,
        accept_new_options=True
    )

    # Update client_data with the single selected role
    if selected_target_role and selected_target_role != "Select a role...":
        # Store as a single role, not a list
        client_data.selected_target_role = selected_target_role
        client_state_manager.update_client_data(selected_target_role=selected_target_role)
    else:
        client_data.selected_target_role = None
        client_state_manager.update_client_data(selected_target_role=None)


@st.fragment
def render_spoc_business_priorities_section(spoc_name_provided, client_data, logger, is_locked):
    """Render the SPOC Business priorities section"""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    # Enhanced CSS for styling
    st.markdown("""
    <style>
    .tooltip-label {
        position: relative;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
    }
    
    .tooltip-icon {
        cursor: help;
        color: #666;
        font-size: 14px;
        position: relative;
    }
    
    .tooltip-icon:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .tooltip-icon:hover::before {
        content: '';
        position: absolute;
        bottom: 115%;
        left: 50%;
        transform: translateX(-50%);
        border: 5px solid transparent;
        border-top-color: #333;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Label with tooltip
    st.markdown('''
    <div class="tooltip-label">
        SPOC Business priorities
        <div class="tooltip-icon" data-tooltip="Select Business priorities of the SPOC based on their role.">ⓘ</div>
    </div>
    ''', unsafe_allow_html=True)

    # Default priorities (used if role is not selected or error occurs)
    default_priorities = [
        {'title': 'Revenue Growth and Market Share Expansion', 'icon': '📈'}, 
        {'title': 'Profitability and Cost Optimization', 'icon': '💰'}, 
        {'title': 'Digital Transformation and Innovation', 'icon': '🤖'}
    ]

    # Initialize selected_business_priorities if missing
    if not hasattr(client_data, 'selected_business_priorities'):
        client_data.selected_business_priorities = []

    # Track the current role to detect role changes
    current_role = getattr(client_data, 'selected_target_role', None)
    session_key = "last_role_for_priorities"
    priorities_session_key = "current_business_priorities_list"
    loading_session_key = "priorities_loading"

    # Initialize session state tracking for last role
    if session_key not in st.session_state:
        st.session_state[session_key] = None
    if priorities_session_key not in st.session_state:
        st.session_state[priorities_session_key] = default_priorities
    if loading_session_key not in st.session_state:
        st.session_state[loading_session_key] = False

    # Load role-based priorities only when role changes or is first loaded
    if current_role and current_role != "Select a role..." and current_role != st.session_state[session_key]:
        # Show loading message using set_global_message
        set_global_message("Getting AI suggestions", "info")
        
        try:
            role_priorities = get_ai_business_priorities(current_role)
            if role_priorities:
                business_priorities_list = role_priorities
                client_state_manager.update_client_data(current_role_priorities=role_priorities)
            else:
                business_priorities_list = default_priorities
                client_state_manager.update_client_data(current_role_priorities=default_priorities)
            
            # Store in session state
            st.session_state[priorities_session_key] = business_priorities_list
            st.session_state[session_key] = current_role
            
            # Clear previous selections when role changes
            client_state_manager.update_client_data(selected_business_priorities=[])
            
            # Clear checkbox initialization flags when role changes
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith("business_priority_checkbox_")]
            for key in keys_to_remove:
                del st.session_state[key]
                
        except Exception as e:
            business_priorities_list = default_priorities
            st.session_state[priorities_session_key] = default_priorities
            client_state_manager.update_client_data(current_role_priorities=default_priorities)
            st.session_state[session_key] = current_role
        
        finally:
            # Clear the loading message
            set_global_message("", "clear")
    # Use cached priorities from session state
    business_priorities_list = st.session_state.get(priorities_session_key, default_priorities)
    
    # Show priorities with add/remove buttons (similar to pain points)
    for i, priority in enumerate(business_priorities_list):
        priority_title = priority.get('title') if isinstance(priority, dict) else str(priority)
        priority_icon = priority.get('icon', '📋') if isinstance(priority, dict) else '📋'
        
        # Check if this priority is selected
        is_selected = priority_title in client_data.selected_business_priorities
        
        # Create a box container with +/- button and content on same horizontal level
        col_add, col_content = st.columns([0.5, 9], gap="medium")
        
        with col_add:
            # Style the button to align vertically with the content box
            st.markdown("""
        <style>
        /* Force override all button styling */
        button[kind="secondary"] {
            height: 48px !important;
            border: 2.2px solid #ececec !important;
            border-radius: 4px !important;
            margin-top: -5px !important;  /* Move button up */
            transform: translateY(-5px) !important;  /* Additional upward adjustment */
            background-color: #d3d3d3 !important;  
            color: black !important;  /* black text */
        }
            
        button[kind="secondary"]:hover {
            border: 2.2px solid #ececec !important;
            transform: translateY(-5px) !important;  /* Keep position on hover */
            background-color: #d3d3d3 !important;  /* Slightly lighter on hover */
            color: black !important;  /* Keep black text on hover */
        }
            
        button[kind="secondary"]:focus {
            border: 2.2px solid #ececec !important;
            outline: 2px solid #ececec !important;
            transform: translateY(-5px) !important;  /* Keep position on focus */
            background-color: #d3d3d3 !important;  /* Keep dark background on focus */
            color: black !important;  /* Keep black text on focus */
        }
            
        /* Try targeting by data attributes */
        [data-testid] button {
            border: 2.2px solid #ececec !important;
            height: 48px !important;
            margin-top: -5px !important;  /* Move button up */
            transform: translateY(-5px) !important;  /* Additional upward adjustment */
            background-color: #d3d3d3 !important;  /* Dark greyish background */
            color: black !important;  /* black text */
        }
        
        /* Additional targeting for button text specifically */
        button[kind="secondary"] p,
        button[kind="secondary"] span,
        button[kind="secondary"] div {
            color: black !important;
        }
        
        [data-testid] button p,
        [data-testid] button span,
        [data-testid] button div {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True) 
            
            button_text = "❌" if is_selected else "➕"
            button_help = f"Remove '{priority_title}' from SPOC priorities" if is_selected else f"Add '{priority_title}' to SPOC priorities"
            button_type = "secondary"
            
            is_enabled = (
                spoc_name_provided and 
                current_role and 
                current_role != "Select a role..."
            )
            
            if st.button(button_text, 
                        key=f"toggle_business_priority_{i}_{hash(current_role or 'none')}", 
                        help=button_help,
                        type=button_type,
                        disabled=not is_enabled or is_locked):
                
                try:
                    if is_selected:
                        # REMOVE FUNCTIONALITY
                        logger.info(f"Removing priority '{priority_title}' from SPOC priorities")
                        
                        # Remove from selected priorities
                        updated_priorities = [p for p in client_data.selected_business_priorities if p != priority_title]
                        
                        client_state_manager.update_client_data(selected_business_priorities=updated_priorities)
                        logger.info(f"Successfully removed priority '{priority_title}'")
                        
                    else:
                        # ADD FUNCTIONALITY
                        logger.info(f"Adding priority '{priority_title}' to SPOC priorities")
                        
                        # Add to selected priorities
                        updated_priorities = list(client_data.selected_business_priorities) + [priority_title]
                        
                        client_state_manager.update_client_data(selected_business_priorities=updated_priorities)
                        logger.info(f"Successfully added priority '{priority_title}'")
                    
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error handling priority button click for '{priority_title}': {str(e)}")
                    set_global_message("Priority update failed - Please try your selection again", "error")

        with col_content:
            # Style the content box based on selection state
            if is_selected:
                background_color = "#DCEBD6"
                border_color = "#ececec"
                text_color = "#000000"
                display_icon = "✅"
                box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
            else:
                background_color = "#f5f5f5"
                border_color = "#ececec"
                text_color = "#000000"
                display_icon = priority_icon
                box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
            
            st.markdown(f"""
            <div style="
                padding: 12px;
                border-radius: 6px;
                margin: 5px 0;
                background-color: {background_color};
                border: 2px solid {border_color};
                color: {text_color};
                font-weight: 500;
                box-shadow: {box_shadow};
                min-height: 24px;
                display: flex;
                align-items: center;
                transition: all 0.3s ease;
            ">
                {display_icon} {priority_title}
            </div>
            """, unsafe_allow_html=True)


@st.fragment
def render_fifth_section(spoc_name_provided, spoc_linkedin_profile, client_data, logger, is_locked):
    """Main function to render the fifth section with two columns"""
    col7, col8 = st.columns([1, 1])

    with col7:
        render_spoc_role_section(spoc_name_provided, spoc_linkedin_profile, client_data, logger, is_locked)

    with col8:
        render_spoc_business_priorities_section(spoc_name_provided, client_data, logger, is_locked)
@st.fragment
def render_sixth_section(logger, is_locked, client_data):
    # Get current client state
    
    client_enterprise_name = client_data.enterprise_name
    client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
    
    col9, col10 = st.columns([1, 1])
    logger.info("Created additional requirements columns")

    # COL9 - Additional Client Requirements
    with col9:
        st.markdown('''
        <div class="tooltip-label">
            Additional Client Requirements
            <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        logger.info("Rendered additional client requirements tooltip")
        
        # TEXT AREA - DISABLED if no client name
        client_additional_requirements = st.text_area(
            label="Additional Client Requirements", 
            value=client_data.client_additional_requirements_content if client_name_provided else "",
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...",
            height=200,
            key="client_additional_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked,
        )
        logger.info(f"Additional requirements text area rendered with {len(client_additional_requirements)} characters")
        
        # Update the state when the text area changes (only if enabled)
        if client_name_provided and client_additional_requirements != client_data.client_additional_requirements_content:
            client_state_manager.update_field('client_additional_requirements_content', client_additional_requirements)
            client_data = client_state_manager.get_state()  # Refresh reference
            logger.info("Updated additional client requirements content")
        
        client_additional_requirements_provided = bool(client_name_provided and client_additional_requirements.strip())
        logger.info(f"Additional requirements provided status: {client_additional_requirements_provided}")

    # COL10 - Additional Specifications
    with col10:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Additional Specifications to be considered
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        logger.info("Rendered additional specifications tooltip")
        
        # Get additional specs items from client data or use dummy data
        if client_name_provided and client_data.additional_specs_items:
            additional_specs_items = client_data.additional_specs_items
            logger.info(f"Using {len(additional_specs_items)} client-specific additional specs")
        else:
            # Dummy data when no client name or no specific data
            additional_specs_items = {
                "Technical Infrastructure Requirements": "**Technical Infrastructure Requirements**\n• Cloud hosting with 99.9% uptime SLA and auto-scaling capabilities\n• Multi-region deployment for disaster recovery and performance optimization\n• Integration with existing ERP, CRM, and financial management systems\n• API-first architecture with RESTful services and webhook support\n• Database performance optimization with sub-second query response times\n• Security compliance with SOC2, ISO 27001, and industry-specific regulations\n• Load balancing and CDN implementation for global content delivery\n• Automated backup and recovery systems with point-in-time restoration\n\n",
                
                "Compliance and Security Standards": "**Compliance and Security Standards**\n• GDPR, CCPA, and regional data privacy regulation compliance\n• End-to-end encryption for data in transit and at rest\n• Multi-factor authentication and role-based access controls\n• Regular security audits and penetration testing protocols\n• Data retention and deletion policies per regulatory requirements\n• Audit trail logging for all system interactions and data changes\n• Incident response plan with 4-hour notification requirements\n• Employee background checks and security clearance verification\n\n",
                
                "Performance and Scalability Metrics": "**Performance and Scalability Metrics**\n• System response time under 2 seconds for 95% of user interactions\n• Concurrent user capacity of 10,000+ with linear scaling capability\n• Database query optimization with indexing and caching strategies\n• Mobile application performance with offline synchronization\n• Bandwidth optimization for low-connectivity environments\n• Real-time analytics and reporting with sub-minute data refresh\n• Automated performance monitoring with threshold-based alerting\n• Capacity planning with predictive scaling based on usage patterns\n\n"
            }
            logger.info("Using default additional specs items")

        # Use a single container for all additional specs items
        with st.container():
            # Display additional specs items with add/remove buttons
            for i, (key, value) in enumerate(additional_specs_items.items()):
                # Check if this item is selected
                is_selected = key in client_data.selected_additional_specs
                
                # Create a box container with +/- button and content on same horizontal level
                col_add, col_content = st.columns([0.5, 9], gap="medium")
                
                with col_add:
                    # Style the button to align vertically with the content box
                    st.markdown("""
                    <style>
                    div[data-testid="column"] > div > div > button {
                        height: 48px !important;
                        margin-top: 5px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Change button appearance based on selection state
                    button_text = "❌" if is_selected else "➕"
                    button_help = f"Remove '{key}' from additional requirements" if is_selected else f"Add '{key}' to additional requirements section"
                    button_type = "secondary" 
                    
                    if st.button(button_text, 
                            key=f"toggle_additional_spec_item_{i}", 
                            help=button_help,
                            type=button_type,
                            disabled=not client_name_provided or is_locked):
                        
                        if is_selected:
                            # REMOVE FUNCTIONALITY
                            # Get current content from the state
                            current_content = client_data.client_additional_requirements_content
                            
                            # Get the original content that was added for this key
                            original_content = client_data.additional_specs_content_map.get(key, value)
                            
                            # Remove this specific additional spec section from content
                            # Try multiple removal patterns to be more robust
                            patterns_to_remove = [
                                f"\n\n{original_content}",
                                f"{original_content}\n\n",
                                original_content
                            ]
                            
                            updated_content = current_content
                            for pattern in patterns_to_remove:
                                updated_content = updated_content.replace(pattern, "")
                            
                            # Clean up any excessive newlines
                            updated_content = '\n\n'.join([section.strip() for section in updated_content.split('\n\n') if section.strip()])
                            
                            # Update the state using the new manager methods
                            client_state_manager.update_multiple_fields(
                                client_additional_requirements_content=updated_content,
                                selected_additional_specs=client_data.selected_additional_specs - {key},
                                additional_specs_content_map={k: v for k, v in client_data.additional_specs_content_map.items() if k != key}
                            )
                            
                            logger.info(f"Removed additional spec: {key}")
                            
                        else:
                            # ADD FUNCTIONALITY
                            # Get current content from the state
                            current_content = client_data.client_additional_requirements_content
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update the state using the new manager methods
                            new_selected_specs = client_data.selected_additional_specs.copy()
                            new_selected_specs.add(key)
                            
                            new_content_map = client_data.additional_specs_content_map.copy()
                            new_content_map[key] = value
                            
                            client_state_manager.update_multiple_fields(
                                client_additional_requirements_content=new_content,
                                selected_additional_specs=new_selected_specs,
                                additional_specs_content_map=new_content_map
                            )
                            
                            logger.info(f"Added additional spec: {key}")
                        
                        st.rerun()

                with col_content:
                    # Style the content box based on selection state
                    if is_selected:
                        background_color = "#DCEBD6"
                        border_color = "#ececec"
                        text_color = "#000000"
                        icon = "✅"
                        box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                    else:
                        background_color = "#f5f5f5"
                        border_color = "#ececec"
                        text_color = "#000000"
                        icon = "📋"
                        box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
                    
                    st.markdown(f"""
                    <div style="
                        padding: 12px;
                        border-radius: 6px;
                        margin: 5px 0;
                        background-color: {background_color};
                        border: 2px solid {border_color};
                        color: {text_color};
                        font-weight: 500;
                        box-shadow: {box_shadow};
                        min-height: 24px;
                        display: flex;
                        align-items: center;
                        transition: all 0.3s ease;
                    ">
                        {icon} {key}
                    </div>
                    """, unsafe_allow_html=True)
                    

def client_tab(st, logger, is_locked):
    """Main client tab function using ClientTabStateManager for state management."""
    logger.info("Starting client_tab function")
    
    try:
        # Get client state from the state manager
        client_state = client_state_manager.get_state()
        logger.debug("Retrieved client state from state manager")
        
        # Apply CSS for styling
        try:
            # Re-apply CSS after every rerun to ensure persistence
            content_area_css = """
            <style>
            /* Primary targeting for block container - 70% width grey background */
            [data-testid="block-container"] {
                background-color: #fafafa !important;
                width: 70% !important;
                max-width: 70% !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            
            /* Alternative targeting for older Streamlit versions */
            .block-container {
                background-color: #fafafa !important;
                width: 70% !important;
                max-width: 70% !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            
            /* Target the element that contains your tab content */
            .stApp .main .block-container {
                background-color: #fafafa !important;
                width: 70% !important;
                max-width: 70% !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            </style>
            """
            st.markdown(content_area_css, unsafe_allow_html=True)
            
            # Apply additional client-specific CSS if available
            if 'client_css' in globals():
                st.markdown(client_css, unsafe_allow_html=True)
            
            # Update CSS applied flag
            if not client_state.css_applied:
                client_state_manager.update_field('css_applied', True)
            
            logger.debug("CSS applied successfully")
            
        except Exception as e:
            logger.error(f"Error applying CSS: {str(e)}")
            set_global_message("Error loading page styles", "error")
        
        # Render all sections using the client state
        logger.debug("Creating sections with client state data")
        
        # Section 1: Enterprise name and basic info
        client_enterprise_name = render_first_section(
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Section 2: Website URL and analysis
        render_second_section(
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Section 3: Enterprise details and requirements
        render_third_section(
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Section 4: SPOC information
        spoc_name_provided, spoc_linkedin_profile = render_fourth_section(
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Section 5: LinkedIn profile handling
        render_fifth_section(
            spoc_name_provided,
            spoc_linkedin_profile,
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Section 6: Pain points and additional specifications
        render_sixth_section(
            logger=logger, 
            client_data=client_state, 
            is_locked=is_locked
        )
        
        # Display validation and completion status if in debug mode
        if client_state.debug_mode:
            logger.debug("Displaying debug information")
            
            # Show validation results
            mandatory_validation = client_state.validate_mandatory_fields()
            optional_validation = client_state.validate_optional_fields()
            completion_percentage = client_state.get_completion_percentage()
            
            with st.expander("Debug Information", expanded=False):
                st.write("**Mandatory Fields Validation:**")
                st.json(mandatory_validation)
                st.write("**Optional Fields Validation:**")
                st.json(optional_validation)
                st.write(f"**Completion Percentage:** {completion_percentage}%")
                
                # Export summary
                summary = client_state.export_summary()
                st.write("**State Summary:**")
                st.json(summary)
        
        # Display global messages if any
        if 'global_message' in st.session_state and st.session_state.global_message:
            message_type = st.session_state.get('global_message_type', 'info')
            
            if message_type == 'error':
                st.error(st.session_state.global_message)
            elif message_type == 'warning':
                st.warning(st.session_state.global_message)
            elif message_type == 'success':
                st.success(st.session_state.global_message)
            else:
                st.info(st.session_state.global_message)
            
            # Clear the message after displaying
            st.session_state.global_message = ""
            st.session_state.global_message_type = "info"
        
        logger.info("Client tab rendered successfully")
        return client_state
        
    except Exception as e:
        logger.error(f"Critical error in client_tab function: {str(e)}")
        set_global_message("Critical error loading client tab. Please refresh the page.", "error")
        
        # Return a default client state in case of error
        try:
            return client_state_manager.get_state()
        except:
            return ClientTabState()


# Additional utility functions for better integration

def handle_client_tab_navigation():
    """Handle any navigation-specific logic for the client tab."""
    try:
        # Reset processing states when navigating to client tab
        client_state_manager.reset_processing_states()
        
        # Clear any temporary UI states
        if 'temp_ui_state' in st.session_state:
            del st.session_state['temp_ui_state']
            
    except Exception as e:
        logger.error(f"Error handling client tab navigation: {str(e)}")


def validate_client_tab_data():
    """Validate client tab data and return validation status."""
    try:
        state = client_state_manager.get_state()
        
        # Check mandatory fields
        if not state.is_mandatory_data_complete():
            return False, "Please complete all mandatory fields (Enterprise Name and Client Requirements)"
        
        # Additional validation logic can be added here
        return True, "All mandatory data is complete"
        
    except Exception as e:
        logger.error(f"Error validating client tab data: {str(e)}")
        return False, "Error validating client data"


def get_client_tab_summary():
    """Get a summary of the current client tab state."""
    try:
        return client_state_manager.export_summary()
    except Exception as e:
        logger.error(f"Error getting client tab summary: {str(e)}")
        return {}


def clear_client_tab_data():
    """Clear all client tab data with confirmation."""
    try:
        client_state_manager.clear_all_data()
        set_global_message("All client data has been cleared", "success")
        return True
    except Exception as e:
        logger.error(f"Error clearing client tab data: {str(e)}")
        set_global_message("Error clearing client data", "error")
        return False
             
