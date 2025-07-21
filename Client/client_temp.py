import streamlit as st
import pandas as pd
import os
import logging
import re
import threading
import time
from typing import List, Dict, Any

# Local application imports
from .client_utils import get_urls_list, check_field_validation, show_field_warning # Assuming these exist
from Search.Linkedin.linkedin_serp import get_linkedin
from Recommendation.recommendation_utils import get_roles_list, get_ai_business_priorities, get_pain_points
from .client_css import client_css
from .client_dataclass import client_state_manager, ClientTabState
from datetime import datetime
from WebScraper.webscraper_without_ai import get_url_details_without_ai
from Common_Utils.common_utils import set_global_message


# --- Helper Functions ---

def normalize_url(url: str) -> str:
    """Normalize the URL format by adding a scheme and a common TLD if missing."""
    if not url or not isinstance(url, str):
        return ""
    url = url.strip()
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    try:
        domain_part = re.sub(r'^https?://', '', url).split('/')[0]
        if not re.search(r'\.(com|in|org|net|co|io|edu|gov|ai)(/|$)', domain_part):
            url = url.rstrip('/') + '.com'
    except Exception:
        # Fallback for invalid URL patterns
        return url
    return url

def save_uploaded_file_and_get_path(uploaded_file, logger, client_enterprise_name: str) -> str | None:
    """Save uploaded file to a directory specific to the enterprise and return the file path."""
    logger.info(f"Starting file upload for: {uploaded_file.name if uploaded_file else 'None'}")
    try:
        if uploaded_file is not None and client_enterprise_name:
            base_upload_dir = os.getenv("FILE_SAVE_PATH", "uploads")
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
            logger.warning("No file provided or enterprise name missing.")
            return None
    except Exception as e:
        set_global_message(f"File save error: {e}", "error")
        logger.error(f"Error in save_uploaded_file_and_get_path: {e}", exc_info=True)
        return None

# --- Section Rendering Functions ---

@st.fragment
def render_client_name_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the client enterprise name input and website search button."""
    st.markdown("""
        <div class="tooltip-label">
            Client Enterprise Name <span style="color:red;">*</span>
            <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client.">ⓘ</div>
        </div>
    """, unsafe_allow_html=True)
    
    name_col, button_col = st.columns([3, 1])
    
    with name_col:
        enterprise_name = st.text_input(
            label="Client Enterprise Name",
            value=client_data.enterprise_name,
            placeholder="Enter client enterprise name...",
            key="client_enterprise_name_input",
            label_visibility="collapsed",
            disabled=is_locked,
        )
        if enterprise_name != client_data.enterprise_name:
            client_state_manager.update_field('enterprise_name', enterprise_name)
            if not enterprise_name: # If name is cleared, clear related data
                client_data.clear_url_data()
            st.rerun()

    with button_col:
        find_urls_disabled = not (client_data.enterprise_name and len(client_data.enterprise_name.strip()) > 2)
        if st.button("🔍 Find Website", disabled=find_urls_disabled, help="Find website URLs for this company", key="find_urls_button"):
            logger.info(f"Finding URLs for: {client_data.enterprise_name}")
            set_global_message(f"Finding websites for '{client_data.enterprise_name}'...", 'info')
            try:
                urls_list = get_urls_list(client_data.enterprise_name.strip())
                client_state_manager.update_multiple_fields(website_urls_list=urls_list, url_search_in_progress=False)
                set_global_message(f"Found {len(urls_list)} URLs." if urls_list else "No URLs found.", 'success' if urls_list else 'info')
            except Exception as e:
                logger.error(f"Error finding URLs: {e}", exc_info=True)
                client_state_manager.update_field('url_search_in_progress', False)
                set_global_message("Failed to find websites.", "error")
            st.rerun()

@st.fragment
def render_client_website_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the client website URL selection and analysis controls."""
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    st.markdown(...) # Tooltip HTML remains the same

    url_col, btn1_col, btn2_col = st.columns([7, 1, 2])
    
    with url_col:
        url_options = ["Select client website URL"] + client_data.website_urls_list
        try:
            default_index = url_options.index(client_data.website_url) if client_data.website_url in url_options else 0
        except ValueError:
            default_index = 0

        website_url_input = st.selectbox(
            label="Client Website URL",
            options=url_options,
            index=default_index,
            key="client_website_url_selector",
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked,
        )
        
        website_url = "" if website_url_input == "Select client website URL" else normalize_url(website_url_input)
        if website_url != client_data.website_url:
            client_state_manager.update_field('website_url', website_url)
            st.rerun()

    with btn2_col:
        if st.button("📑 Get Details", help="Get enterprise details from website", key="scrape_website_btn", use_container_width=True, disabled=not client_data.website_url or is_locked):
            logger.info(f"Scrape button clicked for URL: {client_data.website_url}")
            client_state_manager.update_multiple_fields(pending_scrape_url=client_data.website_url, scraping_in_progress=True)
            set_global_message(f"Analyzing {client_data.website_url}...", 'info')
            st.rerun()

    if client_data.website_url:
        st.markdown(f'🌐 <a href="{client_data.website_url}" target="_blank">Visit Website</a>', unsafe_allow_html=True)

    if client_data.scraping_in_progress and client_data.pending_scrape_url:
        try:
            scrape_result = get_url_details_without_ai(client_data.pending_scrape_url)
            details = f"Company: {scrape_result.name}\n\nDescription:\n{scrape_result.description}\n\nServices:\n" + "\n".join([f"• {s}" for s in scrape_result.services])
            updates = {
                'enterprise_details_content': details,
                'last_analyzed_url': client_data.pending_scrape_url,
                'enterprise_logo': scrape_result.logo,
                'scraping_in_progress': False,
                'pending_scrape_url': None
            }
            client_state_manager.update_multiple_fields(**updates)
            set_global_message("Website details extracted!", 'success')
        except Exception as e:
            logger.error(f"Scraping failed: {e}", exc_info=True)
            client_state_manager.reset_processing_states()
            set_global_message("Failed to extract website details.", 'error')
        st.rerun()

@st.fragment
def render_first_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the first main section (Name and Website)."""
    col1, col2 = st.columns([1, 1])
    with col1:
        render_client_name_section(logger, client_data, is_locked)
    with col2:
        render_client_website_section(logger, client_data, is_locked)

@st.fragment
def enterprise_content(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the enterprise details text area."""
    st.markdown(...) # Tooltip HTML
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    details_content = st.text_area(
        label="Client Enterprise Details",
        value=client_data.enterprise_details_content,
        placeholder="Details from website analysis will appear here, or you can enter them manually.",
        height=150,
        key="enterprise_details_textarea",
        label_visibility="collapsed",
        disabled=not client_name_provided or is_locked
    )
    if details_content != client_data.enterprise_details_content:
        client_state_manager.update_field('enterprise_details_content', details_content)

@st.fragment
def doc_upload_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the RFI document upload and analysis section."""
    st.markdown(...) # Tooltip and CSS
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())

    rfi_document = st.file_uploader(
        label="Upload RFI Document", 
        type=['pdf', 'docx', 'txt'], 
        key="rfi_document_uploader",
        label_visibility="hidden",
        disabled=not client_name_provided or is_locked
    )
    
    if rfi_document:
        if st.button("Get Pain Points", key="analyze_rfi_btn", help="Analyze the document to extract pain points"):
            set_global_message("Analyzing document...", "info")
            try:
                file_path = save_uploaded_file_and_get_path(rfi_document, logger, client_data.enterprise_name)
                if file_path:
                    pain_points = get_pain_points(file_path, client_data.enterprise_name)
                    client_state_manager.update_multiple_fields(
                        uploaded_file_path=file_path,
                        rfi_pain_points_items=pain_points,
                        document_analyzed=True
                    )
                    set_global_message("Document analyzed successfully!", "success")
                else:
                    set_global_message("Failed to save file for analysis.", "error")
            except Exception as e:
                logger.error(f"Error analyzing RFI: {e}", exc_info=True)
                set_global_message("Failed to analyze document.", "error")
            st.rerun()

@st.fragment
def render_second_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the second main section (Doc Upload and Enterprise Content)."""
    col3, col4 = st.columns([1, 1])
    with col3:
        doc_upload_section(logger, client_data, is_locked)
    with col4:
        enterprise_content(logger, client_data, is_locked)

@st.fragment
def render_client_requirements_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the client requirements text area."""
    st.markdown(...) # Tooltip HTML
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    requirements_content = st.text_area(
        label="Client Requirements", 
        value=client_data.client_requirements_content, 
        height=200, 
        key="client_requirements_textarea",
        label_visibility="collapsed",
        disabled=not client_name_provided or is_locked,
        placeholder="Define core client requirements, scope, and deliverables..."
    )
    if requirements_content != client_data.client_requirements_content:
        client_state_manager.update_field('client_requirements_content', requirements_content)

@st.fragment
def render_generic_items_section(
    logger: logging.Logger, 
    client_data: ClientTabState, 
    is_locked: bool,
    title: str,
    tooltip: str,
    items_source_field: str,
    selected_items_field: str,
    content_map_field: str,
    target_content_field: str,
    default_items: Dict[str, str],
    key_prefix: str
):
    """A generic function to render a list of selectable items."""
    st.markdown(f'<div class="tooltip-label">{title}<div class="tooltip-icon" data-tooltip="{tooltip}">ⓘ</div></div>', unsafe_allow_html=True)
    
    items_to_display = getattr(client_data, items_source_field) or default_items
    selected_items = getattr(client_data, selected_items_field)
    content_map = getattr(client_data, content_map_field)
    
    with st.container():
        for i, (key, value) in enumerate(items_to_display.items()):
            is_selected = key in selected_items
            col_add, col_content = st.columns([0.5, 9], gap="medium")

            with col_add:
                if st.button("❌" if is_selected else "➕", key=f"{key_prefix}_{i}", disabled=is_locked, help=f"{'Remove' if is_selected else 'Add'} '{key}'"):
                    current_target_content = getattr(client_data, target_content_field)
                    if is_selected:
                        selected_items.discard(key)
                        original_content = content_map.pop(key, value)
                        updated_content = current_target_content.replace(original_content, "").strip()
                    else:
                        selected_items.add(key)
                        content_map[key] = value
                        updated_content = (current_target_content + f"\n\n{value}").strip()
                    
                    updates = {
                        selected_items_field: selected_items,
                        content_map_field: content_map,
                        target_content_field: updated_content
                    }
                    client_state_manager.update_multiple_fields(**updates)
                    st.rerun()

            with col_content:
                bg = "#DCEBD6" if is_selected else "#f5f5f5"
                st.markdown(f'<div style="background-color:{bg}; padding:12px; border-radius:6px;">{"✅" if is_selected else "📋"} {key}</div>', unsafe_allow_html=True)

@st.fragment
def render_third_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render requirements and pain points sections."""
    col5, col6 = st.columns([1, 1])
    with col5:
        render_client_requirements_section(logger, client_data, is_locked)
    with col6:
        render_generic_items_section(
            logger, client_data, is_locked,
            title="Client Pain Points",
            tooltip="Select pain points extracted from RFI or analysis.",
            items_source_field="rfi_pain_points_items",
            selected_items_field="selected_pain_points",
            content_map_field="pain_point_content_map",
            target_content_field="client_requirements_content",
            default_items={"Revenue Challenges": "...", "Cost Pressure": "..."},
            key_prefix="pain_point"
        )

@st.fragment
def render_spoc_name_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the SPOC name input and handle LinkedIn search."""
    st.markdown(...) # Tooltip
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    spoc_name = st.text_input("SPOC Name", value=client_data.spoc_name, label_visibility="collapsed", disabled=not client_name_provided or is_locked)
    
    if spoc_name != client_data.spoc_name:
        client_state_manager.update_field('spoc_name', spoc_name)
        if spoc_name.strip() and spoc_name != client_data.last_searched_spoc:
            set_global_message(f"Searching LinkedIn for {spoc_name}...", "info")
            try:
                profiles = get_linkedin(spoc_name.strip()) or {}
                client_state_manager.update_multiple_fields(linkedin_profiles=profiles, last_searched_spoc=spoc_name)
            except Exception as e:
                logger.error(f"LinkedIn search failed: {e}", exc_info=True)
                set_global_message("LinkedIn search failed.", "error")
        st.rerun()

@st.fragment
def render_linkedin_profile_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render LinkedIn profile selection and display."""
    st.markdown(...) # Tooltip
    spoc_name_provided = bool(client_data.spoc_name and client_data.spoc_name.strip())
    
    options = ["Select a LinkedIn profile..."]
    url_map = {}
    if spoc_name_provided and client_data.linkedin_profiles:
        for url, data in client_data.linkedin_profiles.items():
            display_text = f"{data.get('name', 'N/A')} - {data.get('role', 'N/A')}"
            options.append(display_text)
            url_map[display_text] = url

    selected_display = st.selectbox("SPOC LinkedIn Profile", options, label_visibility="collapsed", disabled=not spoc_name_provided or is_locked)
    selected_url = url_map.get(selected_display)

    if selected_url != client_data.spoc_linkedin_profile:
        client_state_manager.update_field('spoc_linkedin_profile', selected_url)
        # Auto-update roles and priorities from profile
        if selected_url and selected_url in client_data.linkedin_profiles:
            profile_data = client_data.linkedin_profiles[selected_url]
            updates = {}
            if profile_data.get('role'):
                updates['selected_target_roles'] = [profile_data['role']]
            if profile_data.get('top_3_priorities'):
                updates['selected_business_priorities'] = profile_data['top_3_priorities']
            if updates:
                client_state_manager.update_multiple_fields(**updates)
        st.rerun()
    
    if client_data.spoc_linkedin_profile:
        st.markdown(f'<a href="{client_data.spoc_linkedin_profile}" target="_blank">Visit LinkedIn Profile</a>', unsafe_allow_html=True)

@st.fragment
def render_fourth_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the fourth main section (SPOC Name and LinkedIn Profile)."""
    col_spoc1, col_spoc2 = st.columns([1, 1])
    with col_spoc1:
        render_spoc_name_section(logger, client_data, is_locked)
    with col_spoc2:
        render_linkedin_profile_section(logger, client_data, is_locked)

@st.fragment
def render_spoc_role_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the SPOC Role multiselect."""
    st.markdown(...) # Tooltip
    spoc_name_provided = bool(client_data.spoc_name and client_data.spoc_name.strip())
    
    all_roles = get_roles_list() or []
    
    selected_roles = st.multiselect(
        "SPOC Roles",
        options=all_roles,
        default=client_data.selected_target_roles,
        label_visibility="collapsed",
        disabled=not spoc_name_provided or is_locked
    )
    
    if selected_roles != client_data.selected_target_roles:
        client_state_manager.update_field('selected_target_roles', selected_roles)
        st.rerun()

@st.fragment
def render_spoc_business_priorities_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the SPOC Business Priorities multiselect."""
    st.markdown(...) # Tooltip
    spoc_name_provided = bool(client_data.spoc_name and client_data.spoc_name.strip())
    
    # Simplified version: In a real app, this would be dynamic based on role
    all_priorities = ["Revenue Growth", "Cost Optimization", "Digital Transformation", "Customer Experience"]
    
    selected_priorities = st.multiselect(
        "SPOC Business Priorities",
        options=all_priorities,
        default=client_data.selected_business_priorities,
        label_visibility="collapsed",
        disabled=not spoc_name_provided or is_locked
    )
    
    if selected_priorities != client_data.selected_business_priorities:
        client_state_manager.update_field('selected_business_priorities', selected_priorities)
        st.rerun()

@st.fragment
def render_fifth_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render the fifth main section (SPOC Role and Priorities)."""
    col7, col8 = st.columns([1, 1])
    with col7:
        render_spoc_role_section(logger, client_data, is_locked)
    with col8:
        render_spoc_business_priorities_section(logger, client_data, is_locked)

@st.fragment
def render_sixth_section(logger: logging.Logger, client_data: ClientTabState, is_locked: bool):
    """Render additional requirements and specifications sections."""
    col9, col10 = st.columns([1, 1])
    client_name_provided = bool(client_data.enterprise_name and client_data.enterprise_name.strip())
    
    with col9:
        st.markdown(...) # Tooltip
        additional_reqs = st.text_area(
            "Additional Client Requirements",
            value=client_data.client_additional_requirements_content,
            height=200,
            label_visibility="collapsed",
            disabled=not client_name_provided or is_locked
        )
        if additional_reqs != client_data.client_additional_requirements_content:
            client_state_manager.update_field('client_additional_requirements_content', additional_reqs)

    with col10:
        render_generic_items_section(
            logger, client_data, is_locked,
            title="Additional Specifications",
            tooltip="Select any additional technical or compliance specifications.",
            items_source_field="additional_specs_items",
            selected_items_field="selected_additional_specs",
            content_map_field="additional_specs_content_map",
            target_content_field="client_additional_requirements_content",
            default_items={"Technical Infrastructure": "...", "Compliance Standards": "..."},
            key_prefix="add_spec"
        )

# --- Main Tab Function ---

def client_tab(st, logger: logging.Logger, is_locked: bool):
    """Main function to render the entire client tab."""
    logger.info("Rendering client_tab.")
    
    try:
        # Get the current state from the manager
        client_data = client_state_manager.get_state()

        # Apply CSS
        st.markdown(client_css, unsafe_allow_html=True)
        
        # Render all sections in order
        render_first_section(logger, client_data, is_locked)
        render_second_section(logger, client_data, is_locked)
        render_third_section(logger, client_data, is_locked)
        render_fourth_section(logger, client_data, is_locked)
        render_fifth_section(logger, client_data, is_locked)
        render_sixth_section(logger, client_data, is_locked)

    except Exception as e:
        logger.error(f"Fatal error in client_tab: {e}", exc_info=True)
        set_global_message("A critical error occurred. Please refresh the page.", "error")
        st.error("An unexpected error occurred. Please see the message below and refresh.")
             
    return client_data
