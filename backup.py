# Show validation warning if triggered and field is empty
import streamlit as st
import pandas as pd
from typing import List
from client_utils import *

from client_css import client_css

# Custom CSS for dark theme styling
st.markdown(client_css, unsafe_allow_html=True)

# Additional CSS for consistent styling
st.markdown("""
<style>
/* Consistent label styling for all field types */
.mandatory-label, .optional-label, .ai-label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #f8f9fa !important;
    margin-bottom: 8px !important;
    display: block !important;
}

.mandatory-label {
    color: #ff6b6b !important;
}

.optional-label {
    color: #74c0fc !important;
}

.ai-label {
    color: #51cf66 !important;
}

/* Info button styling */
.info-button {
    display: inline-block;
    margin-left: 8px;
    cursor: help;
    font-size: 14px;
    color: #adb5bd;
    opacity: 0.7;
    transition: opacity 0.2s;
}

.info-button:hover {
    opacity: 1;
    color: #74c0fc;
}

/* Compact button styling */
.compact-button {
    padding: 0.15rem 0.25rem !important;
    font-size: 1.2em !important;
    min-height: 2.5rem !important;
    border-radius: 0.275rem !important;
}

/* Enhanced help text styling */
.help-tooltip {
    font-size: 14px !important;
    line-height: 1.4 !important;
    max-width: 300px !important;
    padding: 8px 12px !important;
}

/* Hide default Streamlit labels */
.stTextInput > label,
.stSelectbox > label,
.stTextArea > label,
.stFileUploader > label,
.stCheckbox > label {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Main App
def client_tab():
    # Initialize validation trigger
    if 'show_validation' not in st.session_state:
        st.session_state.show_validation = False
    
    # Initialize enterprise details content in session state
    if 'enterprise_details_content' not in st.session_state:
        st.session_state.enterprise_details_content = ""
    
    # Top section with client name and URLs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<span class="mandatory-label">Client Enterprise Name<span style="color: red;">*</span><span class="info-button" title="Official name of the client company or organization">ℹ️</span></span>', unsafe_allow_html=True)
        client_enterprise_name = st.text_input(
            label="", 
            placeholder="Enter client enterprise name...", 
            key="client_enterprise_name_input",
            )
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")
    
    with col2:
        st.markdown('<span class="optional-label">Client Website URL<span class="info-button" title="Main website URL of the client organization">ℹ️</span></span>', unsafe_allow_html=True)
        
        # Initialize URLs in session state if not exists
        if 'client_website_urls_list' not in st.session_state:
            st.session_state['client_website_urls_list'] = get_urls_list()
        
        # Create columns for selectbox and buttons with desired ratios
        select_col, btn_col1, btn_col2, btn_col3 = st.columns([0.7, 0.1, 0.1, 0.1])
        
        with select_col:
            # Selectbox for URL selection
            client_website_url = st.selectbox(
                label="", 
                options=st.session_state['client_website_urls_list'], 
                key="client_website_url_selector",
                   )
        
        # URL action buttons with compact styling
        if client_website_url:
            with btn_col1:
                if st.button("🔄", key="refresh_client_website_urls_btn", help="Refresh suggested website links"):
                    st.session_state['client_website_urls_list'] = get_urls_list()
                    st.rerun()
            
            with btn_col2:
                if st.button("🌐", key="open_client_website_btn", help="Open selected client website in new tab"):
                    if client_website_url:
                        st.markdown(f'<a href="{client_website_url}" target="_blank">Opening {client_website_url}</a>', unsafe_allow_html=True)
            
            with btn_col3:
                if st.button("ℹ️", key="client_website_details_btn", help="Extract and analyze details from selected client website"):
                    if client_website_url:
                        # Get URL details and set it as enterprise details content
                        website_details = get_url_details(client_website_url)
                        st.session_state.enterprise_details_content = website_details
                        st.rerun()

    st.markdown("---")
    
    # Document upload and pain points section
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown('<span class="optional-label">Upload RFI Document<span class="info-button" title="Upload RFI/RFP document in PDF, Word, or text format">ℹ️</span></span>', unsafe_allow_html=True)
        rfi_document_upload = st.file_uploader(
            label="", 
            type=['pdf', 'docx', 'txt', 'csv'], 
            key="rfi_document_uploader",
            )
        
        if rfi_document_upload is not None and st.button("Analyze RFI Document", key="analyze_rfi_document_btn", help="Process and extract key information from uploaded RFI document"):
            with st.spinner("Analyzing RFI document..."):
                import time
                time.sleep(1)
                st.session_state.enterprise_details_content = extract_pain_points("document_content")
                st.rerun()
    
    with col4:
        st.markdown('<span class="optional-label">Enterprise Details<span class="info-button" title="Key information about the client company and their business context">ℹ️</span></span>', unsafe_allow_html=True)
        
        # Use the enterprise details content from session state
        enterprise_details = st.text_area(
            label="", 
            value=st.session_state.enterprise_details_content,
            placeholder="Upload RFI document and analyze to extract pain points or click ℹ️ button to view website details...", 
            height=200, 
            key="enterprise_details_textarea", 
              )
        
        # Update session state when text area changes
        st.session_state.enterprise_details_content = enterprise_details

    st.markdown("---")
    
    # Additional row with editable content and summary with + buttons
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown('<span class="mandatory-label">Client Requirement<span style="color: red;">*</span><span class="info-button" title="Detailed requirements and specifications from the client">ℹ️</span></span>', unsafe_allow_html=True)
        # Get editable content from function
        client_requirement_content = get_editable_content()
        client_requirements = st.text_area(
            label="", 
            value=client_requirement_content, 
            height=250, 
            key="client_requirements_textarea", 
           )
          
    with col6:
        st.markdown('<span class="optional-label">RFI Pain Points<span class="info-button" title="Key challenges and pain points extracted from RFI analysis">ℹ️</span></span>', unsafe_allow_html=True)
        
        # Action buttons for summary
        col_generate, col_refresh = st.columns([1, 1])
        with col_generate:
            if st.button("🎯 Generate", key="generate_rfi_pain_points_btn", help="Generate new RFI pain points analysis based on current information"):
                st.session_state['rfi_pain_points_items'] = get_summary_items()
                st.success("RFI pain points generated!")
                st.rerun()
                
        with col_refresh:
            if st.button("🔄 Refresh", key="refresh_rfi_pain_points_btn", help="Refresh and update RFI pain points data"):
                st.session_state['rfi_pain_points_items'] = get_summary_items()
                st.success("RFI pain points refreshed!")
                st.rerun()
        
        # Initialize RFI pain points items in session state
        if 'rfi_pain_points_items' not in st.session_state:
            st.session_state['rfi_pain_points_items'] = get_summary_items()
        
        # Get RFI pain points items from function
        rfi_pain_points_items = st.session_state['rfi_pain_points_items']
        
        # Display RFI pain points items with add buttons
        for i, (key, value) in enumerate(rfi_pain_points_items.items()):
            with st.container():
                # Create a box container for the key with + button
                col_content, col_add = st.columns([4, 1])
                
                with col_content:
                    # Display key in a styled container box
                    st.markdown(f"""
                    <div style="
                        background: #3a3a3a; 
                        padding: 8px 12px; 
                        border-radius: 6px; 
                        border-left: 3px solid #667eea;
                        margin-bottom: 4px;
                        color: #f8f9fa;
                        font-weight: 600;
                    ">
                        📋 {key}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_add:
                    if st.button("➕", key=f"add_rfi_pain_point_item_{i}", help=f"Add '{key}' to client requirements section"):
                        # Get current content from the text area
                        current_content = st.session_state.get('client_requirements_textarea', '')
                        
                        # Append only the value to the additional content
                        new_content = current_content + f"\n\n{value}"
                        
                        # Update the session state for the text area
                        st.session_state['client_requirements_textarea'] = new_content
                        
                        # Show success message
                        st.success(f"✅ '{key}' added to Client Requirements!")
                        st.rerun()
    st.markdown("---")
    
    # SPOC Row
    col_spoc1, col_spoc2 = st.columns([1, 1])
    
    with col_spoc1:
        st.markdown('<span class="optional-label">SPOC Name<span class="info-button" title="Single Point of Contact - primary person for communication">ℹ️</span></span>', unsafe_allow_html=True)
        spoc_name = st.text_input(
            label="", 
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input", 
               )
    
    with col_spoc2:
        st.markdown('<span class="optional-label">SPOC LinkedIn Profile<span class="info-button" title="LinkedIn profile URL of the primary contact person">ℹ️</span></span>', unsafe_allow_html=True)
        
        # Initialize LinkedIn profiles in session state if not exists
        if 'spoc_linkedin_profiles_list' not in st.session_state:
            st.session_state['spoc_linkedin_profiles_list'] = get_linkedin_profiles_list()
        
        # Create a single editable selectbox
        spoc_linkedin_profile = st.selectbox(
            label="",
            options=[""] + st.session_state['spoc_linkedin_profiles_list'],
            key="spoc_linkedin_profile_selector",
            placeholder="Enter or select SPOC LinkedIn profile URL...",
              )
        
        st.markdown("---")
    
    # Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])
    
    with col7:
        st.markdown('<span class="optional-label">Target Roles<span class="info-button" title="Specific job roles or positions to target for this RFI">ℹ️</span></span>', unsafe_allow_html=True)
        
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
                        label="", 
                        value=role, 
                        key=f"target_role_edit_input_{i}",
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
        st.markdown('<span class="optional-label">Business Priorities<span class="info-button" title="Key business priorities and focus areas for the client">ℹ️</span></span>', unsafe_allow_html=True)
        
        # Get priorities from function
        business_priorities_list = get_priority_suggestions()
        
        # Priority checkboxes
        st.write("**Select top business priorities:**")
        
        # Initialize session state for selected priorities
        if 'selected_business_priorities' not in st.session_state:
            st.session_state['selected_business_priorities'] = []
        
        # Generate checkboxes dynamically from function
        for i, priority in enumerate(business_priorities_list):
            business_priority_checkbox_key = f"business_priority_checkbox_{i}"
            is_priority_checked = st.checkbox(
                f"{priority['icon']} **{priority['title']}**", 
                key=business_priority_checkbox_key,
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
        st.markdown('<span class="optional-label">Client Additional Requirements<span class="info-button" title="Extra requirements, constraints, or specific needs from the client">ℹ️</span></span>', unsafe_allow_html=True)
        client_additional_requirements = st.text_area(
            label="", 
            placeholder="Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...", 
            height=200, 
            key="client_additional_requirements_textarea", 
        )
    
    with col10:
        st.markdown('<span class="ai-label">RFI Additional Specs<span class="info-button" title="AI-generated additional specifications based on RFI analysis">ℹ️</span></span>', unsafe_allow_html=True)
        # Get AI suggestion 1 from function
        rfi_additional_specs_content = get_ai_suggestion_1()
        rfi_additional_specs = st.text_area(
            label="", 
            value=rfi_additional_specs_content, 
            height=200, 
            key="rfi_additional_specs_textarea", 
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