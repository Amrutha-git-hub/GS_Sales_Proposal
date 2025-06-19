import streamlit as st
import pandas as pd
import os
from typing import List
from .client_utils import *
import threading
import time
from LinkedIN.linkedin_serp import *
from Recommendation.recommendation_utils import *
from .client_css import client_css


# Apply CSS only once at the beginning with a unique key to prevent duplication
if 'css_applied' not in st.session_state:
    st.session_state.css_applied = True
    st.markdown(client_css, unsafe_allow_html=True)

# Function to save uploaded file and return the file path

# Main App
def client_tab():
    # Re-apply CSS after every rerun to ensure persistence
    st.markdown(client_css, unsafe_allow_html=True)
    
    # Initialize validation trigger
    if 'show_validation' not in st.session_state:
        st.session_state.show_validation = False
    
    # Initialize enterprise details content in session state
    if 'enterprise_details_content' not in st.session_state:
        st.session_state.enterprise_details_content = ""
    
    # Initialize client requirements content in session state
    if 'client_requirements_content' not in st.session_state:
        st.session_state.client_requirements_content = get_editable_content()
    
    # Initialize URLs list in session state
    if 'client_website_urls_list' not in st.session_state:
        st.session_state['client_website_urls_list'] = []
    
    # Initialize last company name to track changes
    if 'last_company_name' not in st.session_state:
        st.session_state['last_company_name'] = ""
    
    # Initialize uploaded file path in session state
    if 'uploaded_file_path' not in st.session_state:
        st.session_state['uploaded_file_path'] = None
    
    # Initialize RFI pain points items in session state
    if 'rfi_pain_points_items' not in st.session_state:
        st.session_state['rfi_pain_points_items'] = {}
    
    # Initialize document analysis status
    if 'document_analyzed' not in st.session_state:
        st.session_state['document_analyzed'] = False
    
    if 'linkedin_profiles' not in st.session_state:
        st.session_state['linkedin_profiles'] = {}
    if 'last_searched_spoc' not in st.session_state:
        st.session_state['last_searched_spoc'] = ""
    
    # Initialize added pain points tracking
    if 'added_pain_points' not in st.session_state:
        st.session_state['added_pain_points'] = set()
    
    # Initialize processing state
    if 'processing_rfi' not in st.session_state:
        st.session_state['processing_rfi'] = False
    
    # Initialize uploaded file info
    if 'uploaded_file_info' not in st.session_state:
        st.session_state['uploaded_file_info'] = None
    
    # Top section with client name and URLs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div class="tooltip-label">
                Client Enterprise Name <span style="color:red;">*</span>
                <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client in all documentation and communications. This field is mandatory for creating the client profile.">ⓘ</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create a sub-column layout for name input and find URLs button
        name_col, button_col = st.columns([4, 1])
        
        with name_col:
            client_enterprise_name = st.text_input(
                label="Client Enterprise Name", 
                placeholder="Enter client enterprise name...", 
                key="client_enterprise_name_input",
                label_visibility="collapsed"
            )
        
        with button_col:
            # Find URLs button - only enabled when client name has more than 2 characters
            find_urls_disabled = not (client_enterprise_name and len(client_enterprise_name.strip()) > 2)
            
            if st.button("🔍 Find URLs", 
                        disabled=find_urls_disabled,
                        help="Find website URLs for this company",
                        key="find_urls_button"):
                # Fetch URLs without any spinner or screen reloading
                try:
                    st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name.strip())
                    st.session_state['last_company_name'] = client_enterprise_name
                except Exception as e:
                    st.session_state['client_website_urls_list'] = []
        
        # Clear URLs if company name is cleared
        if not client_enterprise_name and st.session_state['last_company_name']:
            st.session_state['client_website_urls_list'] = []
            st.session_state['last_company_name'] = ""
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")

    with col2:
        # Label row with inline emoji buttons
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Client Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the client's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help customize your proposal.">ⓘ</div>
            <span style="margin-left: 8px; font-size: 16px; cursor: pointer;" title="Open selected client website in new tab">🌐</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # URL selection logic - Always show normal dropdown, just disable when no client name
        client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
        
        if not st.session_state.get('client_website_urls_list'):
            # No URLs available - show default option
            url_options = ["Select / Enter client website URL"]
        else:
            # URLs available - show them in dropdown
            url_options = ["Select / Enter client website URL"] + st.session_state['client_website_urls_list']
        
        client_website_url = st.selectbox(
            label="Client Website URL",
            options=url_options,
            key="client_website_url_selector",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Reset to empty string if default option is selected
        if client_website_url == "Select / Enter client website URL":
            client_website_url = ""
        
        # Auto-extract website details when URL is selected
        if client_website_url and client_website_url != st.session_state.get('last_analyzed_url', ''):
            try:
                website_details = get_url_details(client_website_url)
                st.session_state.enterprise_details_content = website_details
                st.session_state['last_analyzed_url'] = client_website_url
            except Exception as e:
                pass  # Silently handle errors in auto-extraction
        
        # Show validation warning if triggered and field is empty (optional)
        if st.session_state.show_validation and check_field_validation("Client Website URL", client_website_url, False):
            show_field_warning("Client Website URL")

    # Document upload and pain points section
    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown('''
        <div class="tooltip-label">
            Upload RFI Document
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add custom CSS to make file uploader more compact
        st.markdown("""
        <style>
        .stFileUploader > div > div > div {
            padding: 0.5rem !important;
            min-height: 2rem !important;
        }
        .stFileUploader > div > div {
            min-height: 2rem !important;
        }
        [data-testid="stFileUploader"] {
            height: auto !important;
        }
        [data-testid="stFileUploader"] > div {
            padding: 0.25rem 0.5rem !important;
            min-height: 2rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Show different UI based on analysis status
        if st.session_state.get('document_analyzed', False) and st.session_state.get('uploaded_file_info'):
            # Show analyzed document info with option to upload new
            file_info = st.session_state['uploaded_file_info']
            
            # Display analyzed document info
            st.markdown(f"""
            <div style="
                padding: 12px;
                border-radius: 6px;
                background-color: #2d5016;
                color: #ffffff;
                margin-bottom: 10px;
                border: 1px solid #4a7c20;
            ">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span>✅</span>
                    <div>
                        <div style="font-weight: 500;">Document Analyzed Successfully</div>
                        <div style="font-size: 0.85em; opacity: 0.9;">📄 {file_info['name']} ({file_info['size']})</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Option to upload new document
            if st.button("📤 Upload New Document", key="upload_new_doc_btn", help="Upload a different RFI document"):
                # Reset analysis state
                st.session_state['document_analyzed'] = False
                st.session_state['uploaded_file_info'] = None
                st.session_state['rfi_pain_points_items'] = {}
                st.session_state['uploaded_file_path'] = None
                st.session_state['added_pain_points'] = set()
                st.rerun()
        
        else:
            # Show file uploader when no document is analyzed
            rfi_document_upload = st.file_uploader(
                label="Upload RFI Document", 
                type=['pdf', 'docx', 'txt', 'csv','png','jpg','jpeg'], 
                key="rfi_document_uploader",
                label_visibility="collapsed"
            )
            
            # Show file info and analyze button in a compact way
            if rfi_document_upload is not None:
                # Very compact single line display
                file_size_kb = round(rfi_document_upload.size / 1024, 1)
                file_size_display = f"{file_size_kb}KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)}MB"
                
                # Single compact row
                col_info, col_btn = st.columns([2.5, 1])
                with col_info:
                    st.markdown(f"<span style='font-size:0.8em'>📄 {rfi_document_upload.name[:25]}{'...' if len(rfi_document_upload.name) > 25 else ''} ({file_size_display})</span>", 
                            unsafe_allow_html=True)
                with col_btn:
                    analyze_clicked = st.button("Analyze", key="analyze_rfi_document_btn",
                                            help="Process RFI document",
                                            type="primary", use_container_width=True)
                
                # Handle analyze button click
                if analyze_clicked:
                    if not client_enterprise_name:
                        st.error("❌ Please enter the Client Enterprise Name first")
                    else:
                        # Set processing flag
                        st.session_state['processing_rfi'] = True
                        st.rerun()  # Refresh to show processing state
            
            # Show processing indicator
            if st.session_state.get('processing_rfi', False):
                #st.info("🔄 Analyzing RFI document...")
                
                # Perform the actual processing
                try:
                    # Save the file and get the path
                    file_path = save_uploaded_file_and_get_path(rfi_document_upload)
                    st.session_state['uploaded_file_path'] = file_path
                    
                    if file_path and client_enterprise_name:
                        # Store file info for later display
                        file_size_kb = round(rfi_document_upload.size / 1024, 1)
                        file_size_display = f"{file_size_kb}KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)}MB"
                        st.session_state['uploaded_file_info'] = {
                            'name': rfi_document_upload.name,
                            'size': file_size_display
                        }
                        
                        # Extract pain points using the file path and company name
                        st.session_state.pain_point = get_pain_points(file_path, client_enterprise_name)
                        # Automatically generate RFI pain points items
                        pain_points_data = st.session_state.pain_point
                        st.session_state['rfi_pain_points_items'] = pain_points_data
                        st.session_state['document_analyzed'] = True
                        st.session_state['processing_rfi'] = False  # Reset processing flag
                        #st.success("✅ RFI document analyzed successfully!")
                        time.sleep(1)  # Brief pause to show success message
                        st.rerun()  # Refresh to update UI
                    else:
                        st.error("❌ Error saving the uploaded file")
                        st.session_state['processing_rfi'] = False
                        
                except Exception as e:
                    st.error(f"❌ Error analyzing RFI document: {str(e)}")
                    st.session_state['rfi_pain_points_items'] = {}
                    st.session_state['document_analyzed'] = False
                    st.session_state['processing_rfi'] = False

    with col4:
        st.markdown('''
        <div class="tooltip-label">
            Client Enterprise Details
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # TEXT AREA - DISABLED if no client name
        enterprise_details = st.text_area(
            label="Client Enterprise Details", 
            value=st.session_state.enterprise_details_content if client_name_provided else "",
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Select/Enter the client website URL to fetch enterprise details", 
            height=150, 
            key="enterprise_details_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Update session state when text area changes (only if enabled)
        if client_name_provided and enterprise_details != st.session_state.enterprise_details_content:
            st.session_state.enterprise_details_content = enterprise_details

    # Additional row with editable content and summary with + buttons
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown('''
        <div class="tooltip-label">
            Client Requirements <span style="color:red;">*</span>
            <div class="tooltip-icon" data-tooltip="Define the core client requirements, technical specifications, project scope, deliverables, and expected outcomes. This forms the foundation of your proposal and helps ensure all client needs are addressed.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # TEXT AREA - DISABLED if no client name
        client_requirements = st.text_area(
            label="Client Requirements", 
            value=st.session_state.client_requirements_content if client_name_provided else "", 
            height=200, 
            key="client_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided,
            placeholder="Enter client name first to enable this field" if not client_name_provided else ""
        )
        
        # Update the session state when the text area changes (only if enabled)
        if client_name_provided:
            st.session_state.client_requirements_content = client_requirements
        client_requirements_provided = bool(client_name_provided and client_requirements.strip())
          
    with col6:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Client Pain Points
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get RFI pain points items from session state or use dummy data
        if client_name_provided and st.session_state.get('rfi_pain_points_items'):
            rfi_pain_points_items = st.session_state['rfi_pain_points_items']
        else:
            # Dummy data when no client name or no file uploaded
            rfi_pain_points_items = {
                "Market Positioning & Competitive Advantage": "Need stronger market positioning and differentiation from competitors",
                "Lead Generation & Sales Conversion": "Struggling with consistent lead generation and converting prospects to customers",
                "Digital Presence & Brand Identity": "Lacking cohesive digital presence and professional brand identity"
            }
        
        # Use a single container for all pain points items
        with st.container():
            # Display pain points items with add buttons
            for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                # Create a box container with + button and content on same horizontal level
                col_add, col_content = st.columns([0.5, 9], gap="small")
                
                # Check if this pain point has been added
                is_added = key in st.session_state.get('added_pain_points', set())
                
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
                    
                    # Change button appearance based on whether it's been added
                    button_text = "✅" if is_added else "➕"
                    button_disabled = is_added
                    
                    if st.button(button_text, 
                               key=f"add_rfi_pain_point_item_{i}", 
                               help=f"Add '{key}' to client requirements section" if not is_added else "Already added",
                               disabled=button_disabled):
                        # Get current content from the session state (not the widget key)
                        current_content = st.session_state.get('client_requirements_content', '')
                        
                        # Append the value to the content
                        new_content = current_content + f"\n\n{value}" if current_content else value
                        
                        # Update the session state content variable
                        st.session_state.client_requirements_content = new_content
                        
                        # Mark this pain point as added
                        if 'added_pain_points' not in st.session_state:
                            st.session_state['added_pain_points'] = set()
                        st.session_state['added_pain_points'].add(key)
                        
                        # No success message, just rerun to update UI
                        st.rerun()

                with col_content:
                    # Display key in a styled container box with better visibility
                    # Change background color if added
                    bg_color = "#2d5016" if is_added else "#404040"  # Green background if added
                    
                    st.markdown(f"""
                    <div style="
                        padding: 12px;
                        border-radius: 6px;
                        margin: 5px 0;
                        background-color: {bg_color};
                        color: #ffffff;
                        font-weight: 500;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        min-height: 24px;
                        display: flex;
                        align-items: center;
                    ">
                        📋 {key}
                    </div>
                    """, unsafe_allow_html=True)
    
    # SPOC Row
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
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Automatically search for LinkedIn profiles when SPOC name changes
        if spoc_name and spoc_name.strip() and spoc_name != st.session_state['last_searched_spoc'] and client_name_provided:
            with st.spinner(f"Searching LinkedIn profiles for {spoc_name}..."):
                st.session_state['linkedin_profiles'] = search_linkedin_serpapi(spoc_name.strip())
                st.session_state['last_searched_spoc'] = spoc_name
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
        if spoc_name_provided and st.session_state['linkedin_profiles']:
            # Create options with profile titles for better selection
            linkedin_options = ["Select a LinkedIn profile..."]
            linkedin_url_mapping = {}  # To map display text to actual URL
            
            for url, profile_data in st.session_state['linkedin_profiles'].items():
                display_text = f"{profile_data['role']} ({profile_data['name']})"
                linkedin_options.append(display_text)
                linkedin_url_mapping[display_text] = url
            
            selected_linkedin_display = st.selectbox(
                label="SPOC LinkedIn Profile",
                options=linkedin_options,
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=not spoc_name_provided
            )
            
            # Extract the actual URL from the selected option
            if selected_linkedin_display != "Select a LinkedIn profile...":
                spoc_linkedin_profile = linkedin_url_mapping[selected_linkedin_display]
            else:
                spoc_linkedin_profile = None
                
        elif spoc_name_provided and not st.session_state['linkedin_profiles']:
            # Show message when no profiles found
            st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["No LinkedIn profiles found. Try a different name."],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=True
            )
            spoc_linkedin_profile = None
        else:
            # Default disabled state
            spoc_linkedin_profile = st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["Enter SPOC name to get LinkedIn profiles"],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=not spoc_name_provided
            )

    # Display selected profile information and handle dynamic updates
    if spoc_name_provided and st.session_state['linkedin_profiles']:
        # Initialize session state for tracking selected profile
        if 'current_selected_profile_url' not in st.session_state:
            st.session_state['current_selected_profile_url'] = None
        
        # Check if LinkedIn profile selection has changed
        profile_changed = False
        if 'spoc_linkedin_profile' in locals() and spoc_linkedin_profile:
            if st.session_state['current_selected_profile_url'] != spoc_linkedin_profile:
                st.session_state['current_selected_profile_url'] = spoc_linkedin_profile
                profile_changed = True
                
            selected_profile_data = st.session_state['linkedin_profiles'].get(spoc_linkedin_profile)
            if selected_profile_data:
                st.info(f"""**Selected Profile:** {selected_profile_data['role']} - {selected_profile_data['name']}  
**LinkedIn URL:** {spoc_linkedin_profile}""")
                
                # Update roles and priorities when profile changes
                if profile_changed:
                    # Clear existing auto-populated data
                    if 'selected_target_roles' not in st.session_state:
                        st.session_state['selected_target_roles'] = []
                    if 'selected_business_priorities' not in st.session_state:
                        st.session_state['selected_business_priorities'] = []
                    
                    # Remove previously auto-populated LinkedIn role if it exists
                    linkedin_roles_to_remove = []
                    for i, role in enumerate(st.session_state['selected_target_roles']):
                        # Check if this role was from a previous LinkedIn profile
                        for url, profile in st.session_state['linkedin_profiles'].items():
                            if url != spoc_linkedin_profile and profile['role'] == role:
                                linkedin_roles_to_remove.append(i)
                                break
                    
                    # Remove old LinkedIn roles
                    for idx in reversed(linkedin_roles_to_remove):
                        st.session_state['selected_target_roles'].pop(idx)
                    
                    # Add new LinkedIn role
                    linkedin_role = selected_profile_data['role']
                    if linkedin_role and linkedin_role not in st.session_state['selected_target_roles']:
                        st.session_state['selected_target_roles'].append(linkedin_role)
                    
                    # Remove old LinkedIn priorities and add new ones
                    linkedin_priorities_to_remove = []
                    for priority in st.session_state['selected_business_priorities']:
                        # Check if this priority was from a previous LinkedIn profile
                        for url, profile in st.session_state['linkedin_profiles'].items():
                            if url != spoc_linkedin_profile and priority in profile.get('top_3_priorities', []):
                                linkedin_priorities_to_remove.append(priority)
                                break
                    
                    # Remove old LinkedIn priorities
                    for priority in linkedin_priorities_to_remove:
                        if priority in st.session_state['selected_business_priorities']:
                            st.session_state['selected_business_priorities'].remove(priority)
                    
                    # Add new LinkedIn priorities
                    inferred_priorities = selected_profile_data.get('top_3_priorities', [])
                    for priority in inferred_priorities:
                        if priority not in st.session_state['selected_business_priorities']:
                            st.session_state['selected_business_priorities'].append(priority)
                    
                    # Force rerun to update the display
                    st.rerun()
        elif st.session_state['current_selected_profile_url'] is not None:
            # Profile was deselected
            st.session_state['current_selected_profile_url'] = None
            profile_changed = True

    # Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])

    with col7:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Role 
            <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)

        # Get roles from function
        target_roles_list = get_roles_list()

        # Initialize session state for roles if not exists
        if 'selected_target_roles' not in st.session_state:
            st.session_state['selected_target_roles'] = []

        # Prepare role options for dropdown
        role_options = ["Select a role..."]
        
        # Add standard roles from get_roles_list()
        if target_roles_list:
            role_options.extend(target_roles_list)
        
        # Add LinkedIn roles if available
        if spoc_name_provided and st.session_state.get('linkedin_profiles'):
            for url, profile_data in st.session_state['linkedin_profiles'].items():
                linkedin_role = profile_data.get('role')
                if linkedin_role and linkedin_role not in role_options:
                    role_options.append(linkedin_role)

        # ROLES DROPDOWN
        new_target_role = st.selectbox(
            label="Target Role Selector", 
            options=role_options,
            key="target_role_selector_dropdown",
            label_visibility="collapsed",
            disabled=not (client_name_provided and spoc_name_provided)
        )
    with col8:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Business priorities
            <div class="tooltip-icon" data-tooltip="Select Business priorities of the SPOC.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        if spoc_name_provided:
            business_priorities_list = get_ai_business_priorities(new_target_role)
        else:
            business_priorities_list = ['Strategic Growth and Vision',' Financial Performance and Sustainability','Leadership and Organizational Alignment']
        
        # Initialize session state for selected priorities
        if 'selected_business_priorities' not in st.session_state:
            st.session_state['selected_business_priorities'] = []
        
        # Generate checkboxes dynamically from function
        for i, priority in enumerate(business_priorities_list):
            business_priority_checkbox_key = f"business_priority_checkbox_{i}"
            
            # Handle both string and dict formats - FIXED
            if isinstance(priority, dict):
                # If priority is a dictionary
                priority_title = priority.get('title', str(priority))
                priority_icon = priority.get('icon', '📋')
                display_text = f"{priority_icon} **{priority_title}**"
            else:
                # If priority is a string
                priority_title = str(priority)
                priority_icon = '📋'  # Default icon
                display_text = f"{priority_icon} **{priority_title}**"
            
            # Check if this priority should be pre-selected - FIXED
            default_checked = priority_title in st.session_state.get('selected_business_priorities', [])
            
            is_priority_checked = st.checkbox(
                display_text,
                key=business_priority_checkbox_key,
                value=default_checked
            )
            
            # Update selected business priorities based on checkbox state
            if is_priority_checked and priority_title not in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].append(priority_title)
            elif not is_priority_checked and priority_title in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].remove(priority_title)
    col9, col10= st.columns([1, 1])
    
    with col9:
        st.markdown('''
        <div class="tooltip-label">
            Additional Client Requirements
            <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # TEXT AREA - DISABLED if no client name
        client_additional_requirements = st.text_area(
            label="Additional Client Requirements", 
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...", 
            height=200, 
            key="client_additional_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
    
    
    with col10:
        st.markdown('''
        <div class="tooltip-label">
             Additional Specifications to be considered
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get AI suggestion 1 from function
        rfi_additional_specs_content = get_ai_client_requirements(client_requirements=client_requirements,enterprise_details=enterprise_details) if client_name_provided and client_requirements_provided else  ""
        
        # TEXT AREA - DISABLED if no client name
        rfi_additional_specs = st.text_area(
            label="Additional Specifications", 
            value=rfi_additional_specs_content, 
            height=200, 
            key="rfi_additional_specs_textarea",
            label_visibility="collapsed",
            disabled=not client_requirements_provided,
            placeholder="Enter client name first to enable this field" if not client_name_provided else ""
        )

    # Handle validation trigger from main app
    if 'trigger_validation' in st.session_state and st.session_state.trigger_validation:
        st.session_state.show_validation = True
        st.session_state.trigger_validation = False