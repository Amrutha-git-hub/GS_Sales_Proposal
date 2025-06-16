import streamlit as st
import pandas as pd
import os
from typing import List
from client_utils import *

from client_css import client_css

# Theme CSS definitions
def get_theme_css(is_dark=True):
    if is_dark:
        return """
        <style>
        /* Dark Mode Styles */
        .stApp {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        
        .main .block-container {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        
        /* Text inputs and text areas - Dark Mode */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #464851 !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 1px #667eea !important;
        }
        
        /* File uploader - Dark Mode */
        .stFileUploader > div {
            background-color: #262730 !important;
            border: 2px dashed #464851 !important;
            color: #fafafa !important;
        }
        
        /* Buttons - Dark Mode */
        .stButton > button {
            background-color: #667eea !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton > button:hover {
            background-color: #5a67d8 !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3) !important;
        }
        
        /* Containers and boxes - Dark Mode */
        .tooltip-container {
            background-color: #262730 !important;
            border: 1px solid #464851 !important;
            color: #fafafa !important;
        }
        
        /* Info boxes - Dark Mode */
        .stAlert {
            background-color: #262730 !important;
            color: #fafafa !important;
            border-left: 4px solid #667eea !important;
        }
        
        /* Checkboxes - Dark Mode */
        .stCheckbox > label {
            color: #fafafa !important;
        }
        
        /* Custom styled boxes - Dark Mode */
        div[style*="background: #3a3a3a"] {
            background: #2d3748 !important;
            color: #f8f9fa !important;
        }
        
        /* Selectbox dropdown - Dark Mode */
        .stSelectbox [data-baseweb="select"] {
            background-color: #262730 !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        
        /* Theme toggle button specific styling */
        .theme-toggle-btn {
            position: fixed !important;
            top: 10px !important;
            right: 10px !important;
            z-index: 999999 !important;
            background: #667eea !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 20px !important;
            cursor: pointer !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .theme-toggle-btn:hover {
            background: #5a67d8 !important;
            transform: scale(1.1) !important;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Light Mode Styles */
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        .main .block-container {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Text inputs and text areas - Light Mode */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #d1d5db !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 1px #667eea !important;
        }
        
        /* File uploader - Light Mode */
        .stFileUploader > div {
            background-color: #f9fafb !important;
            border: 2px dashed #d1d5db !important;
            color: #000000 !important;
        }
        
        /* Buttons - Light Mode */
        .stButton > button {
            background-color: #667eea !important;
            color: white !important;
            border: none !important;
        }
        
        .stButton > button:hover {
            background-color: #5a67d8 !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3) !important;
        }
        
        /* Containers and boxes - Light Mode */
        .tooltip-container {
            background-color: #f9fafb !important;
            border: 1px solid #d1d5db !important;
            color: #000000 !important;
        }
        
        /* Info boxes - Light Mode */
        .stAlert {
            background-color: #f9fafb !important;
            color: #000000 !important;
            border-left: 4px solid #667eea !important;
        }
        
        /* Checkboxes - Light Mode */
        .stCheckbox > label {
            color: #000000 !important;
        }
        
        /* Custom styled boxes - Light Mode */
        div[style*="background: #3a3a3a"],
        div[style*="background: #2d3748"] {
            background: #f3f4f6 !important;
            color: #000000 !important;
            border: 1px solid #d1d5db !important;
        }
        
        /* Selectbox dropdown - Light Mode */
        .stSelectbox [data-baseweb="select"] {
            background-color: #ffffff !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Custom content boxes - Light Mode */
        div[style*="background-color: #3a3a3a"],
        div[style*="background-color: #2d3748"] {
            background-color: #e5e7eb !important;
            color: #000000 !important;
            border: 1px solid #d1d5db !important;
        }
        
        /* Theme toggle button specific styling */
        .theme-toggle-btn {
            position: fixed !important;
            top: 10px !important;
            right: 10px !important;
            z-index: 999999 !important;
            background: #667eea !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 20px !important;
            cursor: pointer !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }
        
        .theme-toggle-btn:hover {
            background: #5a67d8 !important;
            transform: scale(1.1) !important;
        }
        
        /* Tooltip styles for light mode */
        .tooltip-label {
            color: #000000 !important;
        }
        
        .tooltip-icon {
            color: #667eea !important;
        }
        
        /* Markdown content - Light Mode */
        .stMarkdown {
            color: #000000 !important;
        }
        
        /* Success/Error messages - Light Mode */
        .stSuccess {
            background-color: #d4edda !important;
            color: #155724 !important;
            border: 1px solid #c3e6cb !important;
        }
        
        .stError {
            background-color: #f8d7da !important;
            color: #721c24 !important;
            border: 1px solid #f5c6cb !important;
        }
        
        .stWarning {
            background-color: #fff3cd !important;
            color: #856404 !important;
            border: 1px solid #ffeaa7 !important;
        }
        
        .stInfo {
            background-color: #d1ecf1 !important;
            color: #0c5460 !important;
            border: 1px solid #bee5eb !important;
        }
        </style>
        """

# Apply CSS based on theme
def apply_theme_css():
    is_dark = st.session_state.get('dark_theme', True)  # Default to dark mode
    theme_css = get_theme_css(is_dark)
    st.markdown(theme_css, unsafe_allow_html=True)
    
    # Also apply the original client CSS
    st.markdown(client_css, unsafe_allow_html=True)

# Function to save uploaded file and return the file path
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

# Theme toggle function
def toggle_theme():
    """Toggle between dark and light theme"""
    st.session_state.dark_theme = not st.session_state.get('dark_theme', True)

# Main App
def client_tab():
    # Initialize theme state if not exists
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = True  # Default to dark mode
    
    # Apply theme CSS
    apply_theme_css()
    
    # Theme toggle button
    theme_icon = "🌙" if st.session_state.dark_theme else "☀️"
    theme_tooltip = "Switch to Light Mode" if st.session_state.dark_theme else "Switch to Dark Mode"
    
    # Create a container for the theme toggle button
    st.markdown(f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index: 999999;">
        <button class="theme-toggle-btn" onclick="document.getElementById('theme-toggle-btn').click();" 
                title="{theme_tooltip}">
            {theme_icon}
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button for theme toggle functionality
    if st.button(theme_icon, key="theme-toggle-btn", help=theme_tooltip):
        toggle_theme()
        st.rerun()
    
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
    
    # Top section with client name and URLs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('''
        <div class="tooltip-label">
            Client Enterprise Name <span style="color:red;">*</span>
            <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client in all documentation and communications. This field is mandatory for creating the client profile.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        client_enterprise_name = st.text_input(
            label="", 
            placeholder="Enter client enterprise name...", 
            key="client_enterprise_name_input",
            label_visibility="collapsed"
        )
        
        # Auto-fetch URLs when company name changes
        if client_enterprise_name and client_enterprise_name != st.session_state['last_company_name']:
            if len(client_enterprise_name.strip()) > 2:  # Only fetch if name has more than 2 characters
                with st.spinner(f"🔍 Fetching URLs for {client_enterprise_name}..."):
                    try:
                        st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name.strip())
                        st.session_state['last_company_name'] = client_enterprise_name
                        # Show success message
                        if st.session_state['client_website_urls_list']:
                            st.success(f"✅ Found {len(st.session_state['client_website_urls_list'])} URL(s) for {client_enterprise_name}")
                        else:
                            st.info(f"ℹ️ No URLs found for {client_enterprise_name}")
                    except Exception as e:
                        st.error(f"❌ Error fetching URLs: {str(e)}")
                        st.session_state['client_website_urls_list'] = []
        
        # Clear URLs if company name is cleared
        elif not client_enterprise_name and st.session_state['last_company_name']:
            st.session_state['client_website_urls_list'] = []
            st.session_state['last_company_name'] = ""
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")
    
    with col2:
        # Embed compact button CSS directly in the component to ensure it persists
        st.markdown("""
        <style>
        div[data-testid="stApp"] .compact-button {
            padding: 0.15rem 0.25rem !important;
            font-size: 1.2em !important;
            min-height: 2.5rem !important;
            border-radius: 0.275rem !important;
        }
        
        /* Ensure button styling persists after reruns */
        .stButton > button {
            transition: all 0.3s ease !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create columns for selectbox and buttons with desired ratios
        select_col, btn_col1, btn_col2, btn_col3 = st.columns([0.7, 0.1, 0.1, 0.1])
        
        with select_col:
            st.markdown('''
            <div class="tooltip-label">
                Client Website URL
                <div class="tooltip-icon" data-tooltip="Select or enter the primary website URL of the client. URLs are automatically fetched when you enter the company name above. This helps in understanding their digital presence, business model, and organizational structure for better proposal customization.">ℹ️</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Show different states based on URLs availability
            if not client_enterprise_name:
                st.info("💡 Enter company name above to auto-fetch URLs")
                client_website_url = st.selectbox(
                    label="", 
                    options=["Enter company name first..."], 
                    key="client_website_url_selector",
                    label_visibility="collapsed",
                    disabled=True
                )
            elif not st.session_state['client_website_urls_list']:
                client_website_url = st.selectbox(
                    label="", 
                    options=["No URLs found - try manual entry"], 
                    key="client_website_url_selector",
                    label_visibility="collapsed"
                )
            else:
                # Selectbox for URL selection with fetched URLs
                url_options = ["Select a URL..."] + st.session_state['client_website_urls_list']
                client_website_url = st.selectbox(
                    label="", 
                    options=url_options, 
                    key="client_website_url_selector",
                    label_visibility="collapsed"
                )
                if client_website_url == "Select a URL...":
                    client_website_url = ""
        
        # URL action buttons with compact styling
        if client_website_url and client_website_url not in ["Enter company name first...", "No URLs found - try manual entry", "Select a URL..."]:
            with btn_col1:
                if st.button("🔄", key="refresh_client_website_urls_btn", help="Refresh suggested website links"):
                    if client_enterprise_name:
                        with st.spinner(f"🔍 Refreshing URLs for {client_enterprise_name}..."):
                            try:
                                st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name.strip())
                                st.success("✅ URLs refreshed!")
                            except Exception as e:
                                st.error(f"❌ Error refreshing URLs: {str(e)}")
                    st.rerun()
            
            with btn_col2:
                if st.button("🌐", key="open_client_website_btn", help="Open selected client website in new tab"):
                    st.markdown(f'<a href="{client_website_url}" target="_blank">Opening {client_website_url}</a>', unsafe_allow_html=True)
            
            with btn_col3:
                if st.button("ℹ️", key="client_website_details_btn", help="Extract and analyze details from selected client website"):
                    # Get URL details and set it as enterprise details content
                    with st.spinner(f"🔍 Analyzing website: {client_website_url}..."):
                        try:
                            website_details = get_url_details(client_website_url)
                            st.session_state.enterprise_details_content = website_details
                            st.success("✅ Website details extracted!")
                        except Exception as e:
                            st.error(f"❌ Error extracting website details: {str(e)}")
                    st.rerun()
        else:
            # Show disabled buttons when no valid URL is selected
            with btn_col1:
                st.button("🔄", key="refresh_client_website_urls_btn_disabled", help="Select a valid URL first", disabled=True)
            with btn_col2:
                st.button("🌐", key="open_client_website_btn_disabled", help="Select a valid URL first", disabled=True)
            with btn_col3:
                st.button("ℹ️", key="client_website_details_btn_disabled", help="Select a valid URL first", disabled=True)

    st.markdown("---")
    
    # Document upload and pain points section
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown('''
        <div class="tooltip-label">
            Upload RFI Document
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        rfi_document_upload = st.file_uploader(
            label="", 
            type=['pdf', 'docx', 'txt', 'csv'], 
            key="rfi_document_uploader",
            label_visibility="collapsed"
        )
        
        if rfi_document_upload is not None and st.button("Analyze RFI Document", key="analyze_rfi_document_btn", help="Process and extract key information from uploaded RFI document"):
            # Save the uploaded file and get the file path
            with st.spinner("Saving and analyzing RFI document..."):
                try:
                    # Save the file and get the path
                    file_path = save_uploaded_file_and_get_path(rfi_document_upload)
                    st.session_state['uploaded_file_path'] = file_path
                    
                    if file_path and client_enterprise_name:
                        # Extract pain points using the file path and company name
                        st.session_state.enterprise_details_content = extract_pain_points(file_path, client_enterprise_name)
                        
                        # Also update the RFI pain points items with the new data
                        st.session_state['rfi_pain_points_items'] = get_summary_items(file_path, client_enterprise_name)
                        
                        st.success("✅ RFI document analyzed successfully!")
                    else:
                        if not client_enterprise_name:
                            st.error("❌ Please enter the Client Enterprise Name first")
                        else:
                            st.error("❌ Error saving the uploaded file")
                except Exception as e:
                    st.error(f"❌ Error analyzing RFI document: {str(e)}")
            st.rerun()
    
    with col4:
        st.markdown('''
        <div class="tooltip-label">
            Enterprise Details
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Use the enterprise details content from session state
        enterprise_details = st.text_area(
            label="", 
            value=st.session_state.enterprise_details_content,
            placeholder="Upload RFI document and analyze to extract pain points or click ℹ️ button to view website details...", 
            height=200, 
            key="enterprise_details_textarea",
            label_visibility="collapsed"
        )
        
        # Update session state when text area changes
        st.session_state.enterprise_details_content = enterprise_details

    st.markdown("---")
    
    # Additional row with editable content and summary with + buttons
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown('''
        <div class="tooltip-label">
            Client Requirement <span style="color:red;">*</span>
            <div class="tooltip-icon" data-tooltip="Define the core client requirements, technical specifications, project scope, deliverables, and expected outcomes. This forms the foundation of your proposal and helps ensure all client needs are addressed.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Use the separate session state variable for content
        client_requirements = st.text_area(
            label="", 
            value=st.session_state.client_requirements_content, 
            height=250, 
            key="client_requirements_textarea",
            label_visibility="collapsed"
        )
        
        # Update the session state when the text area changes
        st.session_state.client_requirements_content = client_requirements
          
    with col6:
        st.markdown('''
        <div class="tooltip-label">
            RFI Pain Points
            <div class="tooltip-icon" data-tooltip="Generated pain points analysis based on RFI document analysis and client information. Click generate to create new analysis or refresh to update existing data.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Action buttons for summary
        col_generate, col_refresh = st.columns([1, 1])
        with col_generate:
            if st.button("🎯 Generate", key="generate_rfi_pain_points_btn", help="Generate new RFI pain points analysis based on current information"):
                if st.session_state.get('uploaded_file_path') and client_enterprise_name:
                    with st.spinner("Generating RFI pain points..."):
                        try:
                            st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                            st.success("✅ RFI pain points generated!")
                        except Exception as e:
                            st.error(f"❌ Error generating pain points: {str(e)}")
                            # Fallback to hardcoded values
                            st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                else:
                    st.warning("⚠️ Please upload and analyze an RFI document first, and ensure Client Enterprise Name is entered")
                    # Fallback to hardcoded values
                    st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                st.rerun()
                
        with col_refresh:
            if st.button("🔄 Refresh", key="refresh_rfi_pain_points_btn", help="Refresh and update RFI pain points data"):
                if st.session_state.get('uploaded_file_path') and client_enterprise_name:
                    with st.spinner("Refreshing RFI pain points..."):
                        try:
                            st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                            st.success("✅ RFI pain points refreshed!")
                        except Exception as e:
                            st.error(f"❌ Error refreshing pain points: {str(e)}")
                            # Fallback to hardcoded values
                            st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                else:
                    st.warning("⚠️ Please upload and analyze an RFI document first, and ensure Client Enterprise Name is entered")
                    # Fallback to hardcoded values
                    st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
                st.rerun()
        
        # Initialize RFI pain points items in session state
        if 'rfi_pain_points_items' not in st.session_state:
            st.session_state['rfi_pain_points_items'] = get_summary_items(st.session_state['uploaded_file_path'], client_enterprise_name)
        
        # Get RFI pain points items from session state
        rfi_pain_points_items = st.session_state['rfi_pain_points_items']
        
        # Dynamic styling for boxes based on theme
        theme_dependent_style = """
        background: #f3f4f6; 
        color: #000000;
        border: 1px solid #d1d5db;
        """ if not st.session_state.dark_theme else """
        background: #2d3748; 
        color: #f8f9fa;
        border-left: 3px solid #667eea;
        """
        
        # Display RFI pain points items with add buttons
        for i, (key, value) in enumerate(rfi_pain_points_items.items()):
            with st.container():
                # Create a box container for the key with + button
                col_content, col_add = st.columns([4, 1])
                
                with col_content:
                    # Display key in a styled container box with theme-dependent styling
                    st.markdown(f"""
                    <div style="
                        {theme_dependent_style}
                        padding: 8px 12px; 
                        border-radius: 6px; 
                        margin-bottom: 4px;
                        font-weight: 600;
                    ">
                        📋 {key}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_add:
                    if st.button("➕", key=f"add_rfi_pain_point_item_{i}", help=f"Add '{key}' to client requirements section"):
                        # Get current content from the session state (not the widget key)
                        current_content = st.session_state.client_requirements_content
                        
                        # Append the value to the content
                        new_content = current_content + f"\n\n{value}"
                        
                        # Update the session state content variable
                        st.session_state.client_requirements_content = new_content
                        
                        # Show success message
                        st.success(f"✅ '{key}' added to Client Requirements!")
                        st.rerun()
    st.markdown("---")
    
    # SPOC Row
    col_spoc1, col_spoc2 = st.columns([1, 1])
    
    with col_spoc1:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Name
            <div class="tooltip-icon" data-tooltip="Enter the Single Point of Contact (SPOC) name - the primary person responsible for communication and decision-making on the client side. This person will be your main contact throughout the project lifecycle.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        spoc_name = st.text_input(
            label="", 
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input",
            label_visibility="collapsed"
        )
    
    with col_spoc2:
        st.markdown('''
        <div class="tooltip-label">
            SPOC LinkedIn Profile
            <div class="tooltip-icon" data-tooltip="Enter or select the LinkedIn profile URL of the SPOC. This helps in understanding their professional background, expertise, and communication style for better relationship building.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Initialize LinkedIn profiles in session state if not exists
        if 'spoc_linkedin_profiles_list' not in st.session_state:
            st.session_state['spoc_linkedin_profiles_list'] = get_linkedin_profiles_list()
        
        # Create a single editable selectbox
        spoc_linkedin_profile = st.selectbox(
            label="",
            options=[""] + st.session_state['spoc_linkedin_profiles_list'],
            key="spoc_linkedin_profile_selector",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
    
    # Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])
    
    with col7:
        st.markdown('''
        <div class="tooltip-label">
            Target Roles 
            <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get roles from function
        target_roles_list = get_roles_list()
        
        # Initialize session state for roles if not exists
        if 'selected_target_roles' not in st.session_state:
            st.session_state['selected_target_roles'] = []
        
        # Dropdown for adding roles
        new_target_role = st.selectbox(
            label="", 
            options=["Select a target role..."] + target_roles_list, 
            key="target_role_selector_dropdown",
            label_visibility="collapsed"
        )
        
        # Add role button
        if st.button("Add Target Role", key="add_target_role_btn", help="Add selected role to target roles list") and new_target_role != "Select a target role...":
            if new_target_role not in st.session_state['selected_target_roles']:
                st.session_state['selected_target_roles'].append(new_target_role)
                # Force rerun to update the display
                st.rerun()
        
        # Display and manage selected target roles
        if st.session_state['selected_target_roles']:
            st.write("**Selected Target Roles:**")
            target_roles_to_remove = []
            for i, role in enumerate(st.session_state['selected_target_roles']):
                col_role, col_remove = st.columns([4, 1])
                with col_role:
                    # Make role editable with unique key
                    edited_target_role = st.text_input(
                        label=f"Target Role {i+1}", 
                        value=role, 
                        key=f"target_role_edit_input_{i}",
                        help=f"Edit target role: {role}"
                    )
                    st.session_state['selected_target_roles'][i] = edited_target_role
                with col_remove:
                    if st.button("🗑️", key=f"remove_target_role_btn_{i}", help="Remove this target role from the list"):
                        target_roles_to_remove.append(i)
            
            # Remove roles (in reverse order to maintain indices)
            for idx in reversed(target_roles_to_remove):
                st.session_state['selected_target_roles'].pop(idx)
                # Force rerun to update the display
                st.rerun()
    
    with col8:
        st.markdown('''
        <div class="tooltip-label">
            Business Priorities 
            <div class="tooltip-icon" data-tooltip="Select business priorities that align with client's strategic objectives. These help in understanding the client's focus areas and tailoring the proposal accordingly.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get priorities from function
        business_priorities_list = get_priority_suggestions()
        
        # Priority checkboxes
        st.write("**Business Priorities :**")
        
        # Initialize session state for selected priorities
        if 'selected_business_priorities' not in st.session_state:
            st.session_state['selected_business_priorities'] = []
        
        # Generate checkboxes dynamically from function
        for i, priority in enumerate(business_priorities_list):
            business_priority_checkbox_key = f"business_priority_checkbox_{i}"
            is_priority_checked = st.checkbox(
                f"{priority['icon']} **{priority['title']}**", 
                key=business_priority_checkbox_key,
                help=f"Business Priority: {priority['description']} - Select if this aligns with client's strategic objectives."
            )
            
            # Update selected business priorities based on checkbox state
            if is_priority_checked and priority['title'] not in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].append(priority['title'])
            elif not is_priority_checked and priority['title'] in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].remove(priority['title'])
        
        # Display selected business priorities summary
        if st.session_state['selected_business_priorities']:
            st.write("**Selected Business Priorities:**")
            for priority in st.session_state['selected_business_priorities']:
                st.write(f"• {priority}")

    st.markdown("---")
    # New row with Client Additional Requirements and RFI Additional Specs
    col9, col10= st.columns([1, 1])
    
    with col9:
        st.markdown('''
        <div class="tooltip-label">
            Client Additional Requirements
            <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        client_additional_requirements = st.text_area(
            label="", 
            placeholder="Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...", 
            height=200, 
            key="client_additional_requirements_textarea",
            label_visibility="collapsed"
        )
    
    with col10:
        st.markdown('''
        <div class="tooltip-label">
            RFI Additional Specs
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        # Get AI suggestion 1 from function
        rfi_additional_specs_content = get_ai_suggestion_1()
        rfi_additional_specs = st.text_area(
            label="", 
            value=rfi_additional_specs_content, 
            height=200, 
            key="rfi_additional_specs_textarea",
            label_visibility="collapsed"
        )
        
        # Refresh button for RFI additional specs
        if st.button("🔄 Refresh RFI Additional Specs", key="refresh_rfi_additional_specs_btn", help="Generate new AI-powered additional specifications based on current RFI analysis"):
            st.session_state['rfi_additional_specs_refreshed'] = get_ai_suggestion_1()
            st.rerun()
    
    st.markdown("---")
    # Handle validation trigger from main app
    if 'trigger_validation' in st.session_state and st.session_state.trigger_validation:
        st.session_state.show_validation = True
        st.session_state.trigger_validation = False


client_tab()