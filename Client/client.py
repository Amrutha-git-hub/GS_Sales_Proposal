
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
from .client_dataclass import ClientData, ClientDataManager
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
        client_data = ClientDataManager.get_client_data()
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


def client_tab(st,logger,is_locked):
    logger.info("Starting client_tab function")
    
    try:

        # Get client data from dataclass manager
        client_data = ClientDataManager.get_client_data()
        logger.debug("Retrieved client data from dataclass manager")
        
        # Apply CSS only once
        try:
            # if not client_data.css_applied:
            #     logger.debug("Applying CSS for the first time")
            #     st.markdown(client_css, unsafe_allow_html=True)
            #     ClientDataManager.update_client_data(css_applied=True)
            #     logger.info("CSS applied and updated in client data")
            
            # Re-apply CSS after every rerun to ensure persistence
            content_area_css = """
            <style>
            /* More aggressive targeting for Streamlit's structure */
            .stApp > div:first-child > div:first-child > div:first-child {
                background-color: #f7f7f7 !important;
            }

            /* Target the main content area */
            .main {
                background-color: #f7f7f7 !important;
            }

            /* Primary targeting for block container with full height and width control */
            [data-testid="block-container"] {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 140vh !important;
                height: auto !important;
                padding-bottom: 5rem !important; /* Extra padding at bottom */
            }

            /* Alternative targeting for older Streamlit versions */
            .block-container {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 140vh !important;
                height: auto !important;
                padding-bottom: 5rem !important;
            }

            /* Target the element that contains your tab content */
            .stApp .main .block-container {
                background-color: #f7f7f7 !important;
                padding: 2rem !important;
                border-radius: 8px !important;
                margin-top: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 80% !important;
                max-width: 80% !important;
                min-height: 140vh !important;
                height: auto !important;
                padding-bottom: 5rem !important;
            }

            /* Ensure the main container expands to content */
            .main > div {
                min-height: 140vh !important;
                height: auto !important;
            }

            /* Target specific Streamlit containers that might override height */
            div[data-testid="stVerticalBlock"] {
                min-height: inherit !important;
                height: auto !important;
            }

            /* Ensure tabs container has proper height */
            .stTabs [data-baseweb="tab-panel"] {
                min-height: 80vh !important;
                height: auto !important;
                padding-bottom: 3rem !important;
            }

            /* Style form elements to stand out on the background */
            .stSelectbox > div,
            .stTextInput > div,
            .stTextArea > div,
            .stNumberInput > div,
            .stDateInput > div,
            .stTimeInput > div {
                background-color: white !important;
                border-radius: 4px !important;
            }

            /* Style expander containers */
            .streamlit-expanderHeader,
            .streamlit-expanderContent {
                background-color: rgba(255, 255, 255, 0.9) !important;
                border-radius: 4px !important;
            }

            /* Style metric containers */
            [data-testid="metric-container"] {
                background-color: rgba(255, 255, 255, 0.9) !important;
                border-radius: 4px !important;
                padding: 8px !important;
            }

            /* Additional fallback for main content area */
            section[data-testid="stSidebar"] ~ div {
                background-color: #f7f7f7 !important;
                width: 80% !important;
                margin-left: auto !important;
                margin-right: auto !important;
                min-height: 140vh !important;
                height: auto !important;
            }

            /* Ensure columns maintain proper height */
            div[data-testid="column"] {
                min-height: inherit !important;
                height: auto !important;
            }

            /* Additional height coverage for dynamic content */
            .stApp {
                min-height: 140vh !important;
                height: auto !important;
            }

            /* Fallback for very long content */
            @media screen and (min-height: 800px) {
                [data-testid="block-container"] {
                    min-height: 140vh !important;
                }
                
                .block-container {
                    min-height: 140vh !important;
                }
                
                .stApp .main .block-container {
                    min-height: 140vh !important;
                }
            }

            /* For extra long content (like many form fields) */
            @media screen and (min-height: 1200px) {
                [data-testid="block-container"] {
                    min-height: 150vh !important;
                }
                
                .block-container {
                    min-height: 150vh !important;
                }
                
                .stApp .main .block-container {
                    min-height: 150vh !important;
                }
            }
            </style>
            """

            st.markdown(content_area_css, unsafe_allow_html=True)
            st.markdown(client_css, unsafe_allow_html=True)

            
            print("content scc applied")
            logger.debug("CSS re-applied for persistence")
            
        except Exception as e:

            logger.error(f"Error applying CSS: {str(e)}")
            set_global_message("Error loading page styles")
        
        # Top section with client name and URLs
        logger.debug("Creating top section with client name and URLs")
        col1, col2 = st.columns([1, 1])
        
        with col1:
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
                        label="Client Enterprise Name", 
                        value=client_data.enterprise_name,
                        placeholder="Enter client enterprise name...", 
                        key="client_enterprise_name_input",
                        label_visibility="collapsed",
                        disabled=is_locked,
                    )
                    
                    # Update dataclass when input changes
                    if client_enterprise_name != client_data.enterprise_name:
                        try:
                            ClientDataManager.update_client_data(enterprise_name=client_enterprise_name)
                            logger.info(f"Updated enterprise name: {client_enterprise_name}")
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
                        
                
                # Handle the Find URLs button click with spinner under the whole first column
                if find_urls_clicked:
                    logger.info(f"Find URLs button clicked for: {client_enterprise_name.strip()}")
                    
                    # Add spinner under the whole first column
                    with st.spinner(f"Finding Websites for '{client_enterprise_name.strip()}'..."):
                        try:
                            urls_list = get_urls_list(client_enterprise_name.strip())
                            logger.info(f"Found {len(urls_list)} URLs for {client_enterprise_name.strip()}")
                            
                            ClientDataManager.update_client_data(
                                website_urls_list=urls_list,
                                enterprise_name=client_enterprise_name
                            )
                            logger.debug("Updated client data with URLs list")
                            
                            if urls_list:
                                pass
                                #set_global_message(f"Successfully found {len(urls_list)} website URLs for {client_enterprise_name.strip()}", 'success')
                            else:
                                set_global_message(f"No website URLs found for {client_enterprise_name.strip()}", "error")
                            st.rerun()
                            
                        except Exception as e:
                            logger.error(f"Error finding URLs for {client_enterprise_name.strip()}: {str(e)}")
                            ClientDataManager.update_client_data(website_urls_list=[])
                            set_global_message("The requested websites couldn't be found. Please try again later.", "error")
                            st.rerun()
                
                # Clear URLs if company name is cleared
                try:
                    if not client_enterprise_name and client_data.enterprise_name:
                        logger.info("Company name cleared, clearing URLs list")
                        ClientDataManager.update_client_data(
                            website_urls_list=[],
                            enterprise_name=""
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
        
        with col2:
            try:
                logger.debug("Processing client website URL section")
                
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
                                ClientDataManager.update_client_data(website_url=client_website_url)
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
                            ClientDataManager.update_client_data(
                                pending_scrape_url=client_website_url,
                                scraping_in_progress=True
                            )
                            #set_global_message(f"Starting website analysis for {client_website_url}", 'info')
                            #st.rerun()
                    except Exception as e:
                        logger.error(f"Error creating scrape button: {str(e)}")
                        set_global_message(f"Error creating scrape button:", 'error')
                        st.rerun()
                        scrape_clicked = False

                # Show redirect link when website is selected
                if client_website_url:
                    client_website_url = normalize_url(client_website_url)
                    with st.container():
                        st.markdown(f'''
                    <style>
                        .website-link-box {{
                            max-width: auto;
                            margin: -5px auto auto -5px;
                            border: 1px solid #bee5eb;
                            border-radius: 4px;
                            padding: 8px 12px;
                            background-color: #d1ecf1;
                            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                            font-family: Arial, sans-serif;
                        }}
                        
                        .website-link-box a {{
                            color: #0c5460;
                            text-decoration: none;
                            font-weight: 500;
                            display: inline-block;
                        }}
                        
                        .website-link-box a:hover {{
                            text-decoration: underline;
                        }}
                    </style>
                    <div class="website-link-box">
                        🌐 <a href="{client_website_url}" target="_blank">Visit Website</a>
                    </div>
                ''', unsafe_allow_html=True)

                # Handle refresh action
                if refresh_clicked and client_name_provided:
                    try:
                        logger.info(f"Refreshing URLs for: {client_enterprise_name}")
                        with st.spinner("Refreshing website URLs..."):
                            urls_list = get_urls_list(client_enterprise_name)
                            ClientDataManager.update_client_data(website_urls_list=urls_list)
                            logger.info(f"Successfully refreshed URLs, found {len(urls_list)} URLs")
                            
                            if urls_list:
                                pass
                                #set_global_message(f"Successfully refreshed! Found {len(urls_list)} website URLs", 'success')
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
                        with st.spinner(f"Scraping website details from {client_data.pending_scrape_url}..."):
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
                                    ClientDataManager.update_client_data(
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
                                    
                                    ClientDataManager.update_client_data(**update_params)
                                    
                                    # Show success message with logo info
                                    if logo_url:
                                        pass#set_global_message("Website details and logo extracted successfully!", 'success')
                                    else:
                                        pass #set_global_message("Website details extracted successfully!", 'success')
                                    
                                    st.rerun()
                                    
                            except Exception as scrape_error:
                                logger.error(f"Error during website scraping for {client_data.pending_scrape_url}: {str(scrape_error)}", exc_info=True)
                                ClientDataManager.update_client_data(
                                    scraping_in_progress=False,
                                    pending_scrape_url=None
                                )
                                set_global_message(f"Error scraping website:", 'error')
                                logger.error(f"Error sraping :{str(e)}")
                                st.rerun()
                                
                    except Exception as e:
                        logger.error(f"Critical error in website scraping process: {str(e)}", exc_info=True)
                        # Ensure scraping state is cleared even on critical errors
                        try:
                            ClientDataManager.update_client_data(
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


        col3, col4 = st.columns([1, 1])
        
        with col3:
            try:
                logger.debug("Processing file upload section")
                
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
                .processing-file {
                    animation: pulse 1.5s ease-in-out infinite;
                    background: linear-gradient(90deg, #e3f2fd, #bbdefb, #e3f2fd);
                    background-size: 200% 100%;
                    animation: shimmer 2s linear infinite;
                    border-radius: 4px;
                }
                @keyframes pulse {
                    0% { opacity: 0.6; }
                    50% { opacity: 1; }
                    100% { opacity: 0.6; }
                }
                @keyframes shimmer {
                    0% { background-position: -200% 0; }
                    100% { background-position: 200% 0; }
                }
                .analyzing-text {
                    color: #1976d2;
                    font-weight: 500;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # FILE UPLOAD
                try:
                    rfi_document_upload = st.file_uploader(
                        label="Upload RFI Document", 
                        type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
                        key="rfi_document_uploader",
                        label_visibility="collapsed",
                        
                    )
                    
                    if rfi_document_upload is not None:
                        logger.info(f"File uploaded: {rfi_document_upload.name}")
                        
                except Exception as e:
                    logger.error(f"Error creating file uploader: {str(e)}")
                    set_global_message("📤 Upload service temporarily unavailable - Please refresh the page and try again")
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
                            if client_data.processing_rfi:
                                st.markdown(f"""
                                <div class="processing-file">
                                    <span style='font-size:0.8em' class="analyzing-text">
                                        🔄 {rfi_document_upload.name[:20]}{'...' if len(rfi_document_upload.name) > 20 else ''} (Analyzing...)
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"<span style='font-size:0.8em'>📄 {rfi_document_upload.name[:25]}{'...' if len(rfi_document_upload.name) > 25 else ''} ({file_size_display})</span>", 
                                           unsafe_allow_html=True)
                        
                        with col_btn:
                            try:
                                button_color = "#FF6B6B" if client_data.processing_rfi else "#4CAF50"
                                st.markdown(f"""
                                <style>
                                div.stButton > button:first-child {{
                                    background-color: {button_color};
                                    color: white;
                                    border: none;
                                }}
                                </style>
                                """, unsafe_allow_html=True)

                                analyze_clicked = st.button(
                                    "Analyzing..." if client_data.processing_rfi else "Get pain points",
                                    key="analyze_rfi_document_btn",
                                    help="Process RFI document" if not client_data.processing_rfi else "Processing in progress...",
                                    type="secondary",
                                    disabled=client_data.processing_rfi,
                                    use_container_width=True
                                )
                                
                            except Exception as e:
                                logger.error(f"Error creating analyze button: {str(e)}")
                                set_global_message("🎨 Button display issue - Please refresh the page to restore full functionality")
                                analyze_clicked = False
                        
                        # Handle analyze button click
                        if analyze_clicked and not client_data.processing_rfi:
                            try:
                                if not client_enterprise_name:
                                    logger.warning("Analyze clicked but no client enterprise name provided")
                                    set_global_message("📝 Client name required - Please enter your client's enterprise name to continue")
                                else:
                                    logger.info("Starting RFI analysis process")
                                    ClientDataManager.update_client_data(processing_rfi=True)
                                    st.rerun()
                            except Exception as e:
                                logger.error(f"Error handling analyze button click: {str(e)}")
                                set_global_message("🔄 Analysis initialization failed - Please try again")
                        
                        # Show processing indicator
                        if client_data.processing_rfi:
                            try:
                                with st.container():
                                    col_spinner, col_text = st.columns([0.5, 4])
                                    with col_spinner:
                                        with st.spinner(''):
                                            pass
                                    with col_text:
                                        st.markdown("**🔍 Analyzing RFI document and extracting key insights...**")
                                
                                # Perform the actual processing
                                try:
                                    logger.info("Starting RFI document processing")
                                    file_path = save_uploaded_file_and_get_path(rfi_document_upload,logger,client_enterprise_name)
                                    
                                    if file_path and client_enterprise_name:
                                        logger.info(f"Processing RFI file: {file_path}")
                                        pain_points_data = get_pain_points(file_path, client_enterprise_name)
                                        logger.info(f"Successfully extracted pain points, count: {len(pain_points_data) if pain_points_data else 0}")
                                        
                                        ClientDataManager.update_client_data(
                                            uploaded_file_path=file_path,
                                            rfi_pain_points_items=pain_points_data,
                                            document_analyzed=True,
                                            processing_rfi=False
                                        )
                                        st.success("✅ RFI document analyzed successfully!")
                                        st.rerun()
                                    else:
                                        logger.error("Error saving the uploaded file or missing client name")
                                        set_global_message("⚠️ Upload failed - We couldn't process your file. Please try again or contact support if the issue persists")
                                        ClientDataManager.update_client_data(processing_rfi=False)
                                        
                                except Exception as e:
                                    logger.error(f"Error analyzing RFI document: {str(e)}")
                                    set_global_message("🔍 Analysis unavailable - We're having trouble analyzing your document right now. Please try uploading again")
                                    ClientDataManager.update_client_data(
                                        rfi_pain_points_items={},
                                        document_analyzed=False,
                                        processing_rfi=False
                                    )
                                    
                            except Exception as e:
                                logger.error(f"Error in processing indicator section: {str(e)}")
                                set_global_message("⚙️ Processing display issue - Please refresh the page to continue")
                                
                    except Exception as e:
                        logger.error(f"Error in file info section: {str(e)}")
                        set_global_message("📊 File information display issue - Please refresh the page to restore functionality")
                        
            except Exception as e:
                logger.error(f"Error in file upload column: {str(e)}")
                set_global_message("📤 Upload service temporarily unavailable - Please refresh the page and try again")

        with col4:
            try:
                logger.debug("Processing enterprise details section")
                
                st.markdown('''
                <div class="tooltip-label">
                    Client Enterprise Details
                    <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
                </div>
                ''', unsafe_allow_html=True)
                
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
                            ClientDataManager.update_client_data(enterprise_details_content=enterprise_details)
                            logger.debug("Updated enterprise details content")
                        except Exception as e:
                            logger.error(f"Error updating enterprise details: {str(e)}")
                            set_global_message("💾 Save failed - Your enterprise details couldn't be saved. Please try again")
                            
                except Exception as e:
                    logger.error(f"Error creating enterprise details textarea: {str(e)}")
                    set_global_message("📝 Text editor unavailable - Please refresh the page to restore functionality")
                    
            except Exception as e:
                logger.error(f"Error in enterprise details column: {str(e)}")
                set_global_message("⚙️ Enterprise details section temporarily unavailable - Please refresh the page to continue")

        # Client Requirements and Pain Points Row
        logger.debug("Creating client requirements and pain points section")
        col5, col6 = st.columns([1, 1])

        with col5:
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
                        placeholder="Enter client name first to enable this field" if not client_name_provided else "Add your client requirements here youmay take suggestions from AI in the right as well"
                    )
                    
                    # Update the client data when the text area changes (only if enabled)
                    if client_name_provided:
                        try:
                            ClientDataManager.update_client_data(client_requirements_content=client_requirements)
                            logger.debug("Updated client requirements content")
                        except Exception as e:
                            logger.error(f"Error updating client requirements: {str(e)}")
                            set_global_message("💾 Save failed - Your client requirements couldn't be saved. Please try again")
                    
                    client_requirements_provided = bool(client_name_provided and client_requirements.strip())
                    logger.debug(f"Client requirements provided: {client_requirements_provided}")
                    
                except Exception as e:
                    logger.error(f"Error creating client requirements textarea: {str(e)}")
                    set_global_message("📝 Requirements editor unavailable - Please refresh the page to restore functionality")
                    client_requirements = ""
                    client_requirements_provided = False
                    
            except Exception as e:
                logger.error(f"Error in client requirements column: {str(e)}")
                set_global_message("⚙️ Requirements section temporarily unavailable - Please refresh the page to continue")
                
        
            # Continue from COL6 with enhanced logging and error handling
            with col6:
                try:
                    logger.info("Starting COL6 - Client Pain Points section rendering")
                    
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
                        set_global_message("📊 Data loading issue - We're having trouble loading your pain points. Please refresh the page")
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
                                        set_global_message("🔍 Selection status check failed - Please refresh the page")
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
                        border: 2.2px solid #618f8f !important;
                        border-radius: 4px !important;
                        margin-top: -5px !important;  /* Move button up */
                        transform: translateY(-3px) !important;  /* Additional upward adjustment */
                        background-color: #4a4a4a !important;  /* Dark greyish background */
                        color: white !important;  /* White text */
                    }
                     
                    button[kind="secondary"]:hover {
                        border: 2.2px solid #618f8f !important;
                        transform: translateY(-3px) !important;  /* Keep position on hover */
                        background-color: #5a5a5a !important;  /* Slightly lighter on hover */
                        color: white !important;  /* Keep white text on hover */
                    }
                     
                    button[kind="secondary"]:focus {
                        border: 2.2px solid #618f8f !important;
                        outline: 2px solid #618f8f !important;
                        transform: translateY(-3px) !important;  /* Keep position on focus */
                        background-color: #4a4a4a !important;  /* Keep dark background on focus */
                        color: white !important;  /* Keep white text on focus */
                    }
                     
                    /* Try targeting by data attributes */
                    [data-testid] button {
                        border: 2.2px solid #618f8f !important;
                        height: 48px !important;
                        margin-top: -5px !important;  /* Move button up */
                        transform: translateY(-2.5px) !important;  /* Additional upward adjustment */
                        background-color: #4a4a4a !important;  /* Dark greyish background */
                        color: white !important;  /* White text */
                    }
                    
                    /* Additional targeting for button text specifically */
                    button[kind="secondary"] p,
                    button[kind="secondary"] span,
                    button[kind="secondary"] div {
                        color: white !important;
                    }
                    
                    [data-testid] button p,
                    [data-testid] button span,
                    [data-testid] button div {
                        color: white !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)  
                                            icon_url = (
                                                    "https://cdn-icons-png.flaticon.com/512/5974/5974627.png"  # ❌ (close)
                                                    if is_selected else
                                                    "home/shreyank/GS/GS_Sales_Proposal/Images/remove.png"         # ➕ (add)
                                                )      
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
                                                            
                                                            ClientDataManager.update_client_data(
                                                                client_requirements_content=updated_content,
                                                                selected_pain_points=client_data.selected_pain_points,
                                                                pain_point_content_map=client_data.pain_point_content_map
                                                            )
                                                            
                                                            logger.info(f"Successfully removed pain point '{key}'")
                                                            
                                                        except Exception as e:
                                                            logger.error(f"Error in remove functionality for '{key}': {str(e)}")
                                                            set_global_message("🔄 Item removal failed - Couldn't remove the selected item. Please try again")
                                                        
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
                                                            
                                                            ClientDataManager.update_client_data(
                                                                client_requirements_content=new_content,
                                                                selected_pain_points=client_data.selected_pain_points,
                                                                pain_point_content_map=client_data.pain_point_content_map
                                                            )
                                                            
                                                            logger.info(f"Successfully added pain point '{key}'")
                                                            
                                                        except Exception as e:
                                                            logger.error(f"Error in add functionality for '{key}': {str(e)}")
                                                            set_global_message("➕ Item addition failed - Couldn't add the selected item. Please try again")
                                                    
                                                    st.rerun()
                                                    
                                                except Exception as e:
                                                    logger.error(f"Error handling button click for '{key}': {str(e)}")
                                                    set_global_message("🔄 Selection update failed - Please try your selection again")
                                                    
                                        except Exception as e:
                                            logger.error(f"Error rendering button for pain point '{key}': {str(e)}")
                                            set_global_message("🎨 Button display issue - Please refresh the page to restore full functionality")

                                    with col_content:
                                        try:
                                            # Style the content box based on selection state
                                            if is_selected:
                                                background_color = "#DCEBD6"
                                                border_color = "#5a9f9f"
                                                text_color = "#000000"
                                                icon = "✅"
                                                box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                                            else:
                                                background_color = "#f5f5f5"
                                                border_color = "#5a9f9f"
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
                                            set_global_message("🎨 Content display issue - Please refresh the page to restore full functionality")
                                            
                                except Exception as e:
                                    logger.error(f"Error processing pain point item {i} ('{key}'): {str(e)}")
                                    set_global_message("⚠️ Processing error - We couldn't process your selection. Please try again")
                                    
                    except Exception as e:
                        logger.error(f"Error rendering pain points container: {str(e)}")
                        set_global_message("📊 Pain points section unavailable - Please refresh the page to restore functionality")
                        
                except Exception as e:
                    logger.error(f"Critical error in COL6 rendering: {str(e)}")
                    set_global_message("🚨 Service interruption - We're experiencing technical difficulties. Please refresh the page or contact support")
            # SPOC Row


        #____________________________________________________________________

        col_spoc1, col_spoc2 = st.columns([1, 1])

        with col_spoc1:
            st.markdown('''
            <div class="tooltip-label">
                SPOC Name
                <div class="tooltip-icon" data-tooltip="Enter the Single Point of Contact (SPOC) name - the primary person responsible for communication and decision-making on the client side. This person will be your main contact throughout the project lifecycle.">ⓘ</div>
            </div>
            ''', unsafe_allow_html=True)
            
            spoc_name = st.text_input(
                label="SPOC Name", 
                value=client_data.spoc_name,
                placeholder="Enter SPOC full name...", 
                key="spoc_name_input",
                label_visibility="collapsed",
                disabled=not client_name_provided or is_locked
            )
            
            # Update client data when SPOC name changes
            if spoc_name != client_data.spoc_name:
                ClientDataManager.update_client_data(spoc_name=spoc_name)
            
            # Automatically search for LinkedIn profiles when SPOC name changes
            if spoc_name and spoc_name.strip() and spoc_name != client_data.last_searched_spoc and client_name_provided:
                with st.spinner(f"Searching LinkedIn profiles for {spoc_name}..."):
                    # Assuming search_linkedin_serpapi is available
                    print(f"Searching for {spoc_name}")
                    #linkedin_profiles_raw = get_linkedin(spoc_name.strip()+" "+client_enterprise_name.strip())
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
                    else:
                        set_global_message("No such linkedin profiles found","info")
                    ClientDataManager.update_client_data(
                        linkedin_profiles=processed_profiles,
                        last_searched_spoc=spoc_name
                    )
                    st.rerun()

        with col_spoc2:
            # Check if SPOC name is provided (for disabling LinkedIn field)
            spoc_name_provided = bool(spoc_name and spoc_name.strip()) and client_name_provided
            
            st.markdown('''
            <div class="tooltip-label">
                Select SPOC LinkedIn Profile
                <div class="tooltip-icon" data-tooltip="Enter or select the LinkedIn profile URL of the SPOC. This helps in understanding their professional background, expertise, and communication style for better relationship building.">ⓘ</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Prepare LinkedIn profile options
            if spoc_name_provided and client_data.linkedin_profiles:
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
                        ClientDataManager.update_client_data(spoc_linkedin_profile=spoc_linkedin_profile)
                else:
                    spoc_linkedin_profile = None
                    
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

        # Display selected profile information and handle dynamic updates
        if spoc_name_provided and client_data.linkedin_profiles:
            # Check if LinkedIn profile selection has changed
            profile_changed = False
            if 'spoc_linkedin_profile' in locals() and spoc_linkedin_profile:
                if client_data.current_selected_profile_url != spoc_linkedin_profile:
                    ClientDataManager.update_client_data(current_selected_profile_url=spoc_linkedin_profile)
                    profile_changed = True
                    
                selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
                if selected_profile_data and isinstance(selected_profile_data, dict):
                    name = selected_profile_data.get('name', 'Unknown')
                    role = selected_profile_data.get('role', 'Unknown Role')
                    st.markdown(f'''
    <style>
        .selected-profile-box {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 100%;
            margin: 10px 0;
            border: 1px solid #c3e6cb;
            border-radius: 6px;
            padding: 10px 16px;
            background-color: #d4edda;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            color: #4791bf;
        }}

        .selected-profile-box .left {{
            width: 50%;
            word-wrap: break-word;
        }}

        .selected-profile-box .right {{
            width: 50%;
            padding-left: 20px; /* Shift right */
            word-wrap: break-word;
        }}

        .selected-profile-box a {{
            color: #4791bf;
            font-weight: bold;
            text-decoration: none;
        }}

        .selected-profile-box a:hover {{
            text-decoration: underline;
        }}
    </style>

    <div class="selected-profile-box">
        <div class="left">
            👤 <strong>Selected Profile:</strong> {name} – {role}
        </div>
        <div class="right">
            🔗 <a href="{spoc_linkedin_profile}" target="_blank">Visit the LinkedIn profile</a>
        </div>
    </div>
''', unsafe_allow_html=True)


                    
                    # Update roles and priorities when profile changes
                    if profile_changed:
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
                        ClientDataManager.update_client_data(
                            selected_target_roles=getattr(client_data, 'selected_target_roles', []),
                            selected_business_priorities=getattr(client_data, 'selected_business_priorities', [])
                        )
                        
                        # Force rerun to update the display
                        st.rerun()
            elif hasattr(client_data, 'current_selected_profile_url') and client_data.current_selected_profile_url is not None:
                # Profile was deselected
                ClientDataManager.update_client_data(current_selected_profile_url=None)
                profile_changed = True

        # Roles and Priorities Row
        col7, col8 = st.columns([1, 1])

        with col7:
            st.markdown('''
            <div class="tooltip-label">
                SPOC Role 
                <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ⓘ</div>
            </div>
            ''', unsafe_allow_html=True)

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
                ClientDataManager.update_client_data(selected_target_role=selected_target_role)
            else:
                client_data.selected_target_role = None
                ClientDataManager.update_client_data(selected_target_role=None)

        with col8:
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
                # Show loading state
                st.session_state[loading_session_key] = True
                
                # Display loading message
                loading_placeholder = st.empty()
                with loading_placeholder.container():
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin: 10px 0;">
                        <div style="
                            width: 20px; 
                            height: 20px; 
                            border: 2px solid #f3f3f3; 
                            border-top: 2px solid #1f77b4; 
                            border-radius: 50%; 
                            animation: spin 1s linear infinite;
                        "></div>
                        <span style="color: #1f77b4; font-weight: 500;">🤖 Generating personalized business priorities for {role}...</span>
                    </div>
                    <style>
                        @keyframes spin {{
                            0% {{ transform: rotate(0deg); }}
                            100% {{ transform: rotate(360deg); }}
                        }}
                    </style>
                    """.format(role=current_role), unsafe_allow_html=True)
                
                try:
                    role_priorities = get_ai_business_priorities(current_role)
                    if role_priorities:
                        business_priorities_list = role_priorities
                        ClientDataManager.update_client_data(current_role_priorities=role_priorities)
                    else:
                        business_priorities_list = default_priorities
                        ClientDataManager.update_client_data(current_role_priorities=default_priorities)
                    
                    # Store in session state
                    st.session_state[priorities_session_key] = business_priorities_list
                    st.session_state[session_key] = current_role
                    
                    # Clear previous selections when role changes
                    ClientDataManager.update_client_data(selected_business_priorities=[])
                    
                    # Clear checkbox initialization flags when role changes
                    keys_to_remove = [key for key in st.session_state.keys() if key.startswith("business_priority_checkbox_")]
                    for key in keys_to_remove:
                        del st.session_state[key]
                        
                except Exception as e:
        
                    business_priorities_list = default_priorities
                    st.session_state[priorities_session_key] = default_priorities
                    ClientDataManager.update_client_data(current_role_priorities=default_priorities)
                    st.session_state[session_key] = current_role
                
                finally:
                    # Hide loading state
                    st.session_state[loading_session_key] = False
                    loading_placeholder.empty()
            else:
                # Use cached priorities from session state
                business_priorities_list = st.session_state.get(priorities_session_key, default_priorities)

            # Only show checkboxes if not loading
            if not st.session_state[loading_session_key]:
                # Collect checkbox states without immediate updates
                checkbox_states = {}
                selected_priorities = []
                
                # Show checkboxes for priorities
                for i, priority in enumerate(business_priorities_list):
                    priority_title = priority.get('title') if isinstance(priority, dict) else str(priority)
                    priority_icon = priority.get('icon', '📋') if isinstance(priority, dict) else '📋'
                    display_text = f"{priority_icon} **{priority_title}**"
                    
                    # Create unique key for this checkbox based on role and index
                    checkbox_key = f"business_priority_checkbox_{i}_{hash(current_role or 'none')}"
                    
                    is_enabled = (
                        spoc_name_provided and 
                        current_role and 
                        current_role != "Select a role..."
                    )
                    
                    # Get checkbox state - let Streamlit handle the initial value
                    is_checked = st.checkbox(
                        display_text,
                        key=checkbox_key,
                        disabled=not is_enabled,
                        value=priority_title in client_data.selected_business_priorities
                    )
                    
                    # Store the state for batch update
                    checkbox_states[priority_title] = is_checked
                    if is_checked:
                        selected_priorities.append(priority_title)

                # Batch update client data only if there are actual changes
                current_selections = set(client_data.selected_business_priorities)
                new_selections = set(selected_priorities)
                
                if current_selections != new_selections:
                    ClientDataManager.update_client_data(selected_business_priorities=selected_priorities)
        # Create columns with proper error handling
        try:
            col9, col10 = st.columns([1, 1])
            logger.info("Created additional requirements columns")
            
            # COL9 - Additional Client Requirements
            with col9:
                try:
                    st.markdown('''
                    <div class="tooltip-label">
                        Additional Client Requirements
                        <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ⓘ</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    logger.info("Rendered additional client requirements tooltip")
                except Exception as e:
        
                    logger.error(f"Error rendering additional client requirements tooltip: {str(e)}")
                
                try:
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
                except Exception as e:
        
                    logger.error(f"Error creating additional requirements text area: {str(e)}")
                    client_additional_requirements = ""
                
                try:
                    # Update the dataclass when the text area changes (only if enabled)
                    if client_name_provided and client_additional_requirements != client_data.client_additional_requirements_content:
                        ClientDataManager.update_client_data(client_additional_requirements_content=client_additional_requirements)
                        client_data = ClientDataManager.get_client_data()  # Refresh reference
                        logger.info("Updated additional client requirements content")
                except Exception as e:
        
                    logger.error(f"Error updating additional client requirements: {str(e)}")
                
                try:
                    client_additional_requirements_provided = bool(client_name_provided and client_additional_requirements.strip())
                    logger.info(f"Additional requirements provided status: {client_additional_requirements_provided}")
                except Exception as e:
        
                    logger.error(f"Error checking additional requirements provided status: {str(e)}")
                    client_additional_requirements_provided = False

            # COL10 - Additional Specifications
            with col10:
                try:
                    # Title with tooltip only (no buttons)
                    st.markdown('''
                    <div class="tooltip-label">
                        Additional Specifications to be considered
                        <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    logger.info("Rendered additional specifications tooltip")
                except Exception as e:
        
                    logger.error(f"Error rendering additional specifications tooltip: {str(e)}")
                
                try:
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
                except Exception as e:
        
                    logger.error(f"Error preparing additional specs items: {str(e)}")
                    additional_specs_items = {}

                try:
                    # Use a single container for all additional specs items
                    with st.container():
                        # Display additional specs items with add/remove buttons
                        for i, (key, value) in enumerate(additional_specs_items.items()):
                            try:
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
                                            try:
                                                # REMOVE FUNCTIONALITY
                                                # Get current content from the dataclass
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
                                                
                                                # Update the dataclass
                                                client_data.client_additional_requirements_content = updated_content
                                                client_data.selected_additional_specs.discard(key)
                                                if key in client_data.additional_specs_content_map:
                                                    del client_data.additional_specs_content_map[key]
                                                
                                                # Save changes to session state
                                                ClientDataManager.save_client_data(client_data)
                                                logger.info(f"Removed additional spec: {key}")
                                            except Exception as remove_error:
                                                logger.error(f"Error removing additional spec '{key}': {str(remove_error)}")
                                                
                                        else:
                                            try:
                                                # ADD FUNCTIONALITY
                                                # Get current content from the dataclass
                                                current_content = client_data.client_additional_requirements_content
                                                
                                                # Append the value to the content
                                                new_content = current_content + f"\n\n{value}" if current_content else value
                                                
                                                # Update the dataclass
                                                client_data.client_additional_requirements_content = new_content
                                                client_data.additional_specs_content_map[key] = value
                                                client_data.selected_additional_specs.add(key)
                                                
                                                # Save changes to session state
                                                ClientDataManager.save_client_data(client_data)
                                                logger.info(f"Added additional spec: {key}")
                                            except Exception as add_error:
                                                logger.error(f"Error adding additional spec '{key}': {str(add_error)}")
                                        
                                        st.rerun()

                                with col_content:
                                    try:
                                        # Style the content box based on selection state
                                        if is_selected:
                                            background_color = "#DCEBD6"
                                            border_color = "#4a90e2"
                                            text_color = "#000000"
                                            icon = "✅"
                                            box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                                        else:
                                            background_color = "#f5f5f5"
                                            border_color = "#5a9f9f"
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
                                    except Exception as content_error:
                                        logger.error(f"Error rendering content box for '{key}': {str(content_error)}")
                            except Exception as item_error:
                                logger.error(f"Error processing additional spec item '{key}': {str(item_error)}")

                except Exception as e:
        
                    logger.error(f"Error displaying additional specs items: {str(e)}")
                    
        except Exception as e:
            # If column creation fails, show error and return early

            logger.error(f"Error creating additional requirements columns: {str(e)}")
            return client_data  # Return early to prevent further issues

        try:
            # Handle validation trigger from main app
            if client_data.show_validation:
                # Your validation logic here
                logger.info("Validation triggered")
                pass
        except Exception as e:

            logger.error(f"Error handling validation: {str(e)}")
    except Exception as e:

            logger.error(f"Error handling validation: {str(e)}")
             
    return client_data