import streamlit as st
import pandas as pd
import os
import logging
import re
import threading
import time
from typing import List, Dict

# Assuming these are the correct paths to your modules
from .client_utils import *
from Search.Linkedin.linkedin_serp import get_linkedin
from Recommendation.recommendation_utils import get_roles_list, get_ai_business_priorities, get_pain_points
from .client_css import client_css
from .client_dataclass import client_state_manager, ClientTabState
from datetime import datetime
from WebScraper.webscraper_without_ai import get_url_details_without_ai
from Common_Utils.common_utils import set_global_message

def normalize_url(url: str) -> str:
    """Normalize the URL format."""
    url = url.strip()
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    domain_part = re.sub(r'^https?://', '', url).split('/')[0]
    if not re.search(r'\.(com|in|org|net|co|io|edu|gov)(/|$)', domain_part):
        url = url.rstrip('/') + '.com'
    return url

def save_uploaded_file_and_get_path(uploaded_file, logger, client_enterprise_name):
    """Save uploaded file to a directory and return the file path."""
    logger.info(f"Starting file upload for: {uploaded_file.name if uploaded_file else 'None'}")
    try:
        if uploaded_file is not None:
            base_upload_dir = os.getenv("FILE_SAVE_PATH")
            enterprise_upload_dir = os.path.join(base_upload_dir, client_enterprise_name)
            if not os.path.exists(enterprise_upload_dir):
                os.makedirs(enterprise_upload_dir)
                logger.info(f"Created directory: {enterprise_upload_dir}")
            
            file_path = os.path.join(enterprise_upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            logger.info(f"Successfully saved file to: {file_path}")
            return file_path
        else:
            logger.warning("No file provided for upload.")
            return None
    except Exception as e:
        set_global_message(str(e))
        logger.error(f"Error in save_uploaded_file_and_get_path: {str(e)}", exc_info=True)
        raise

def validate_client_mandatory_fields():
    """Validate client mandatory fields using the state manager."""
    try:
        return client_state_manager.is_mandatory_data_complete()
    except Exception as e:
        set_global_message(f"Error during validation: {str(e)}")
        return False

@st.fragment
def render_client_name_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the client enterprise name section."""
    try:
        st.markdown("""
            <div class="tooltip-label">
                Client Enterprise Name <span style="color:red;">*</span>
                <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client in all documentation and communications. This field is mandatory for creating the client profile.">ⓘ</div>
            </div>
        """, unsafe_allow_html=True)
        
        name_col, button_col = st.columns([3, 1])
        
        with name_col:
            client_enterprise_name = st.text_input(
                label="Client Enterprise Name",
                placeholder="Enter client enterprise name...",
                key="client_enterprise_name_input",
                label_visibility="collapsed",
                disabled=is_locked,
                value=client_data.enterprise_name
            )
            if client_enterprise_name != client_data.enterprise_name:
                client_state_manager.update_multiple_fields(enterprise_name=client_enterprise_name)
                logger.info(f"Updated enterprise name: {client_enterprise_name}")
                st.rerun()

        with button_col:
            find_urls_disabled = not (client_enterprise_name and len(client_enterprise_name.strip()) > 2)
            if st.button("🔍 Find Website", disabled=find_urls_disabled, help="Find website URLs for this company", key="find_urls_button"):
                logger.info(f"Find URLs button clicked for: {client_enterprise_name.strip()}")
                set_global_message(f"Finding websites for '{client_enterprise_name.strip()}'...", 'info')
                try:
                    urls_list = get_urls_list(client_enterprise_name.strip())
                    client_state_manager.update_multiple_fields(website_urls_list=urls_list)
                    set_global_message(f"Found {len(urls_list)} URLs." if urls_list else "No URLs found.", 'success' if urls_list else 'info')
                except Exception as e:
                    logger.error(f"Error finding URLs: {str(e)}", exc_info=True)
                    set_global_message("Failed to find websites.", "error")
                st.rerun()

        if not client_enterprise_name and client_data.enterprise_name:
            client_state_manager.update_multiple_fields(website_urls_list=[], enterprise_name="")
            logger.info("Company name cleared, clearing URLs list.")
            st.rerun()

    except Exception as e:
        logger.error(f"Error in client name section: {str(e)}", exc_info=True)
        set_global_message("An error occurred in the client name section.", 'error')
        st.rerun()
    return client_enterprise_name

@st.fragment
def render_client_website_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the client website URL section."""
    try:
        client_enterprise_name = client_data.enterprise_name
        client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())

        st.markdown(...) # Tooltip HTML remains the same

        url_col, btn1_col, btn2_col = st.columns([7, 1, 2])
        
        with url_col:
            url_options = ["Select client website URL"] + client_data.website_urls_list
            default_index = url_options.index(client_data.website_url) if client_data.website_url in url_options else 0
            
            client_website_url_input = st.selectbox(
                label="Client Website URL",
                options=url_options,
                index=default_index,
                key="client_website_url_selector",
                label_visibility="collapsed",
                disabled=not client_name_provided or is_locked,
                accept_new_options=True,
            )
            
            client_website_url = "" if client_website_url_input == "Select client website URL" else normalize_url(client_website_url_input)

            if client_website_url != client_data.website_url:
                client_state_manager.update_multiple_fields(website_url=client_website_url)
                logger.info(f"Updated website URL: {client_website_url}")
                st.rerun()

        with btn1_col:
            if st.button("🔄", help="Refresh website URLs list", key="refresh_urls_btn", use_container_width=True, disabled=not client_name_provided):
                try:
                    set_global_message("Refreshing URLs...", 'info')
                    urls_list = get_urls_list(client_enterprise_name)
                    client_state_manager.update_multiple_fields(website_urls_list=urls_list)
                    set_global_message(f"Found {len(urls_list)} URLs.", 'success')
                except Exception as e:
                    logger.error(f"Error refreshing URLs: {str(e)}", exc_info=True)
                    set_global_message("Failed to refresh URLs.", 'error')
                st.rerun()

        with btn2_col:
            if st.button("📑 Get Details", help="Get enterprise details", key="scrape_website_btn", use_container_width=True, disabled=not client_website_url or is_locked):
                logger.info(f"Scrape button clicked for URL: {client_website_url}")
                client_state_manager.update_multiple_fields(pending_scrape_url=client_website_url, scraping_in_progress=True)
                set_global_message(f"Starting website analysis for {client_website_url}", 'info')
                st.rerun()

        if client_data.scraping_in_progress and client_data.pending_scrape_url:
            try:
                logger.info(f"Scraping {client_data.pending_scrape_url}")
                scrape_result = get_url_details_without_ai(client_data.pending_scrape_url)
                website_details = f"Company: {scrape_result.name}\n\n"
                if scrape_result.description: website_details += f"Description:\n{scrape_result.description}\n\n"
                if scrape_result.services:
                    website_details += "Services:\n" + "".join([f"• {s}\n" for s in scrape_result.services])

                if not website_details.strip() or len(website_details.strip()) < 10:
                    set_global_message("Website scraping failed: No content extracted.", "error")
                    client_state_manager.update_multiple_fields(scraping_in_progress=False, pending_scrape_url=None)
                else:
                    update_params = {
                        'enterprise_details_content': website_details,
                        'last_analyzed_url': client_data.pending_scrape_url,
                        'scraping_in_progress': False,
                        'pending_scrape_url': None,
                        'enterprise_logo': scrape_result.logo
                    }
                    client_state_manager.update_multiple_fields(**update_params)
                    set_global_message("Website details extracted successfully!", 'success')
                st.rerun()
            except Exception as e:
                logger.error(f"Error during website scraping: {str(e)}", exc_info=True)
                client_state_manager.update_multiple_fields(scraping_in_progress=False, pending_scrape_url=None)
                set_global_message("Error scraping website.", 'error')
                st.rerun()

    except Exception as e:
        logger.error(f"Error in website section: {str(e)}", exc_info=True)
        set_global_message("An error occurred in the website section.", 'error')
        st.rerun()

@st.fragment
def render_first_section(logger, client_data, is_locked):
    """Render the first section with two columns."""
    col1, col2 = st.columns([1, 1])
    with col1:
        render_client_name_section(logger, client_data, is_locked)
    with col2:
        render_client_website_section(logger, client_data, is_locked)

@st.fragment
def enterprise_content(logger, client_data: ClientTabState, is_locked: bool):
    """Render the enterprise details section."""
    try:
        st.markdown(...) # Tooltip HTML
        client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
        
        enterprise_details = st.text_area(
            label="Client Enterprise Details",
            value=client_data.enterprise_details_content if client_name_provided else "",
            placeholder="Enter client name first..." if not client_name_provided else "Website analysis results appear here...",
            height=150,
            key="enterprise_details_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked
        )
        if client_name_provided and enterprise_details != client_data.enterprise_details_content:
            client_state_manager.update_multiple_fields(enterprise_details_content=enterprise_details)

    except Exception as e:
        logger.error(f"Error in enterprise_content: {str(e)}", exc_info=True)
        set_global_message("Error rendering enterprise details.", 'error')

@st.fragment
def doc_upload_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the document upload section."""
    try:
        st.markdown(...) # Tooltip HTML and CSS
        client_enterprise_name = client_data.enterprise_name

        rfi_document_upload = st.file_uploader(
            label="Upload RFI Document", 
            type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
            key="rfi_document_uploader",
            label_visibility="hidden",
            disabled=is_locked
        )
        
        if rfi_document_upload is not None:
            if st.button("Get pain points", key="analyze_rfi_document_btn"):
                if not client_enterprise_name:
                    set_global_message("Please enter a client name first.", 'error')
                else:
                    set_global_message("Analyzing document...", "info")
                    try:
                        file_path = save_uploaded_file_and_get_path(rfi_document_upload, logger, client_enterprise_name)
                        if file_path:
                            pain_points_data = get_pain_points(file_path, client_enterprise_name)
                            client_state_manager.update_multiple_fields(
                                uploaded_file_path=file_path,
                                rfi_pain_points_items=pain_points_data,
                                document_analyzed=True
                            )
                            set_global_message("RFI analyzed successfully!", "success")
                        else:
                            set_global_message("Failed to save uploaded file.", 'error')
                    except Exception as e:
                        logger.error(f"Error analyzing RFI: {str(e)}", exc_info=True)
                        set_global_message("Failed to analyze document.", 'error')
                    st.rerun()

    except Exception as e:
        logger.error(f"Error in doc_upload_section: {str(e)}", exc_info=True)
        set_global_message("Error with document upload section.", 'error')

@st.fragment
def render_second_section(logger, client_data, is_locked):
    """Render the second section with two columns."""
    col3, col4 = st.columns([1, 1])
    with col3:
        doc_upload_section(logger, client_data, is_locked)
    with col4:
        enterprise_content(logger, client_data, is_locked)

@st.fragment
def render_client_requirements_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the client requirements section."""
    try:
        client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
        st.markdown(...) # Tooltip HTML
        
        client_requirements = st.text_area(
            label="Client Requirements", 
            value=client_data.client_requirements_content,
            height=200, 
            key="client_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked,
            placeholder="Enter client name first..." if not client_name_provided else "Add client requirements here..."
        )
        if client_name_provided and client_requirements != client_data.client_requirements_content:
            client_state_manager.update_multiple_fields(client_requirements_content=client_requirements)

    except Exception as e:
        logger.error(f"Error in requirements section: {str(e)}", exc_info=True)
        set_global_message("Error in requirements section.", 'error')

@st.fragment
def render_client_pain_points_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the client pain points section."""
    try:
        client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
        st.markdown(...) # Tooltip HTML
        
        rfi_pain_points_items = client_data.rfi_pain_points_items or { # Default data
            "Revenue Challenges": "...", "Cost and Margin Pressure": "...", "Market Expansion": "..."
        }

        with st.container():
            for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                is_selected = key in client_data.selected_pain_points
                col_add, col_content = st.columns([0.5, 9], gap="medium")

                with col_add:
                    if st.button("❌" if is_selected else "➕", key=f"toggle_pain_point_{i}", disabled=not client_name_provided or is_locked):
                        current_content = client_data.client_requirements_content
                        if is_selected:
                            client_data.selected_pain_points.discard(key)
                            original_content = client_data.pain_point_content_map.get(key, value)
                            updated_content = current_content.replace(original_content, "").strip()
                        else:
                            client_data.selected_pain_points.add(key)
                            client_data.pain_point_content_map[key] = value
                            updated_content = (current_content + f"\n\n{value}").strip()
                        
                        client_state_manager.update_multiple_fields(
                            selected_pain_points=client_data.selected_pain_points,
                            pain_point_content_map=client_data.pain_point_content_map,
                            client_requirements_content=updated_content
                        )
                        st.rerun()

                with col_content:
                    # Div styling based on is_selected...
                    st.markdown(f"<div>{key}</div>", unsafe_allow_html=True) 

    except Exception as e:
        logger.error(f"Error in pain points section: {str(e)}", exc_info=True)
        set_global_message("Error displaying pain points.", 'error')

@st.fragment
def render_third_section(logger, client_data, is_locked):
    """Render client requirements and pain points sections."""
    col5, col6 = st.columns([1, 1])
    with col5:
        render_client_requirements_section(logger, client_data, is_locked)
    with col6:
        render_client_pain_points_section(logger, client_data, is_locked)

@st.fragment
def render_spoc_name_section(logger, client_data: ClientTabState, is_locked: bool):
    """Render the SPOC name input section."""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    st.markdown(...) # Tooltip
    
    spoc_name = st.text_input(
        label="SPOC Name",
        value=client_data.spoc_name,
        key="spoc_name_input",
        label_visibility="collapsed",
        disabled=not client_name_provided or is_locked
    )
    
    if spoc_name != client_data.spoc_name:
        client_state_manager.update_multiple_fields(spoc_name=spoc_name)
        # Trigger search on name change
        if spoc_name.strip():
            set_global_message(f"Searching for {spoc_name}...", "info")
            try:
                profiles = get_linkedin(spoc_name.strip()) or {}
                client_state_manager.update_multiple_fields(
                    linkedin_profiles=profiles,
                    last_searched_spoc=spoc_name
                )
            except Exception as e:
                logger.error(f"LinkedIn search failed: {e}", exc_info=True)
                set_global_message("LinkedIn search failed.", "error")
        st.rerun()
    return spoc_name

@st.fragment
def render_linkedin_profile_section(logger, client_data: ClientTabState, is_locked: bool, spoc_name: str):
    """Render the LinkedIn profile selection section."""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    spoc_name_provided = bool(spoc_name and spoc_name.strip())
    st.markdown(...) # Tooltip

    options = ["Select a LinkedIn profile..."]
    url_map = {}
    if spoc_name_provided and client_data.linkedin_profiles:
        for url, data in client_data.linkedin_profiles.items():
            display_text = f"{data.get('name', 'N/A')} - {data.get('role', 'N/A')}"
            options.append(display_text)
            url_map[display_text] = url

    selected_display = st.selectbox(
        "SPOC LinkedIn Profile",
        options=options,
        key="spoc_linkedin_profile_selector",
        label_visibility="collapsed",
        disabled=not spoc_name_provided or is_locked
    )

    selected_url = url_map.get(selected_display)
    if selected_url != client_data.spoc_linkedin_profile:
        client_state_manager.update_multiple_fields(spoc_linkedin_profile=selected_url)
        st.rerun()
    return selected_url

