import streamlit as st
import pandas as pd
import os
from typing import List
from client_utils import *


from client_css import client_css

# Apply CSS only once at the beginning with a unique key to prevent duplication
if 'css_applied' not in st.session_state:
    st.session_state.css_applied = True
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
    
    # Top section with client name and URLs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
            <div class="tooltip-label">
                Client Enterprise Name <span style="color:red;">*</span>
                <div class="tooltip-icon" data-tooltip="Enter the full legal name of the client organization. This is the primary identifier for the client in all documentation and communications. This field is mandatory for creating the client profile.">ℹ️</div>
            </div>
        """, unsafe_allow_html=True)
        client_enterprise_name = st.text_input(
            label="Client Enterprise Name", 
            placeholder="Enter client enterprise name...", 
            key="client_enterprise_name_input",
            label_visibility="collapsed"
        )
            
        # Auto-fetch URLs when company name changes
        if client_enterprise_name and client_enterprise_name != st.session_state['last_company_name']:
            if len(client_enterprise_name.strip()) > 2:  # Only fetch if name has more than 2 characters
                try:
                    st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name.strip())
                    st.session_state['last_company_name'] = client_enterprise_name
                except Exception as e:
                    st.session_state['client_website_urls_list'] = []
        
        # Clear URLs if company name is cleared
        elif not client_enterprise_name and st.session_state['last_company_name']:
            st.session_state['client_website_urls_list'] = []
            st.session_state['last_company_name'] = ""
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")
    

    with col2:
        # Label row with inline emoji buttons (FIRST)
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Client Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the client's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help customize your proposal.">ℹ️</div>
            <span style="margin-left: 8px; font-size: 16px; cursor: pointer;" title="Refresh suggested website links">🔄</span>
            <span style="margin-left: 4px; font-size: 16px; cursor: pointer;" title="Open selected client website in new tab">🌐</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # URL selection logic (DROPDOWN SECOND)
        if not client_enterprise_name:
            client_website_url = st.selectbox(
                label="Client Website URL",
                options=["Select / Enter client website URL"],
                key="client_website_url_selector",
                label_visibility="collapsed",
                disabled=True
            )
        elif not st.session_state['client_website_urls_list']:
            client_website_url = st.selectbox(
                label="Client Website URL",
                options=["No URLs found - try manual entry"],
                key="client_website_url_selector",
                label_visibility="collapsed"
            )
        else:
            # Selectbox for URL selection with fetched URLs
            url_options = ["Select / Enter client website URL"] + st.session_state['client_website_urls_list']
            client_website_url = st.selectbox(
                label="Client Website URL",
                options=url_options,
                key="client_website_url_selector",
                label_visibility="collapsed"
            )
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
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        rfi_document_upload = st.file_uploader(
            label="Upload RFI Document", 
            type=['pdf', 'docx', 'txt', 'csv'], 
            key="rfi_document_uploader",
            label_visibility="collapsed",
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
                        st.session_state.enterprise_details_content = get_pain_points(file_path, client_enterprise_name)
                        
                        # Automatically generate RFI pain points items
                        pain_points_data = get_pain_items(file_path, client_enterprise_name)
                        st.session_state['rfi_pain_points_items'] = pain_points_data
                        st.session_state['document_analyzed'] = True
                        
                        #st.success("✅ RFI document analyzed successfully!")
                        #st.success(f"✅ Generated {len(pain_points_data)} pain points for analysis!")
                    else:
                        if not client_enterprise_name:
                            st.error("❌ Please enter the Client Enterprise Name first")
                        else:
                            st.error("❌ Error saving the uploaded file")
                except Exception as e:
                    st.error(f"❌ Error analyzing RFI document: {str(e)}")
                    st.session_state['rfi_pain_points_items'] = {}
                    st.session_state['document_analyzed'] = False
        
        # Show analysis status
        # if st.session_state.get('document_analyzed', False):
        #     st.info(f"📊 Document analyzed - {len(st.session_state['rfi_pain_points_items'])} pain points generated")
        
        # Visual upload prompt box (only shows when no file is uploaded)
        if rfi_document_upload is None:
            st.markdown('''
            <div style="
                height: 50px;
                border: 2px dashed #4A90E2;
                border-radius: 8px;
                background-color: rgba(74, 144, 226, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 10px;
                color: #4A90E2;
                font-size: 16px;
                font-weight: 500;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
            ">
                📄 Upload ur RFI document here
            </div>
            ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="tooltip-label">
            Client Enterprise Details
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Use the enterprise details content from session state
        enterprise_details = st.text_area(
            label="Client Enterprise Details", 
            value=st.session_state.enterprise_details_content,
            placeholder="Select/Enter the client website URL to fetch enterprise details", 
            height=150, 
            key="enterprise_details_textarea",
            label_visibility="collapsed"
        )
        
        # Update session state when text area changes
        st.session_state.enterprise_details_content = enterprise_details

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
            label="Client Requirements", 
            value=st.session_state.client_requirements_content, 
            height=160, 
            key="client_requirements_textarea",
            label_visibility="collapsed"
        )
        
        # Update the session state when the text area changes
        st.session_state.client_requirements_content = client_requirements
          
    with col6:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div style="margin-bottom: 10px;">
            <h4 style="margin: 0; padding: 0;">
                Select Client Pain Points
                <span style="font-size: 0.8em;">ℹ️</span>
            </h4>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get RFI pain points items from session state
        rfi_pain_points_items = st.session_state['rfi_pain_points_items']
        
        # Display pain points if available
        if rfi_pain_points_items and len(rfi_pain_points_items) > 0:
            # Show count of pain points
            #st.markdown(f"**Found {len(rfi_pain_points_items)} Pain Points:**")
            
            # Use a single container for all pain points items
            with st.container():
                
                # Display RFI pain points items with add buttons
                for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                    # Create a box container for the key with + button
                    col_content, col_add = st.columns([4, 1])
                    
                    with col_content:
                        # Display key in a styled container box
                        st.markdown(f"""
                        <div style="
                            background-color: #f0f2f6;
                            padding: 10px;
                            border-radius: 5px;
                            border-left: 4px solid #0066cc;
                            margin: 5px 0;
                        ">
                            📋 {key}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_add:
                        if st.button("➕", key=f"add_rfi_pain_point_item_{i}", help=f"Add '{key}' to client requirements section"):
                            # Get current content from the session state (not the widget key)
                            current_content = st.session_state.client_requirements_content
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update the session state content variable
                            st.session_state.client_requirements_content = new_content
                            
                            # Show success message
                            #st.success(f"✅ '{key}' added to Client Requirements!")
                            st.rerun()
        
        else:
            # Create a container to match the spacing of the pain points items
            with st.container():
                # Show different messages based on document analysis status
                if st.session_state.get('document_analyzed', False):
                    st.markdown("""
                    <div style="
                        background-color: #fff3cd;
                        padding: 15px;
                        border-radius: 5px;
                        border-left: 4px solid #ffc107;
                        margin: 5px 0;
                        text-align: center;
                        color: #856404;
                    ">
                        ⚠️ No pain points found in the analyzed document
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Show placeholder when no pain points are available with consistent styling
                    st.markdown("""
                    <div style="
                        background-color: #273042;
                        padding: 15px;
                        border-radius: 5px;
                        border: 2px dashed #dee2e6;
                        margin: 5px 0;
                        text-align: center;
                        color: #6c757d;
                        min-height: 150px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        📄 Upload and analyze an RFI document to see pain points here
                    </div>
                    """, unsafe_allow_html=True)
    
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
            label="SPOC Name", 
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input",
            label_visibility="collapsed"
        )
    
    with col_spoc2:
        st.markdown('''
        <div class="tooltip-label">
            Select SPOC LinkedIn Profile
            <div class="tooltip-icon" data-tooltip="Enter or select the LinkedIn profile URL of the SPOC. This helps in understanding their professional background, expertise, and communication style for better relationship building.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Initialize LinkedIn profiles in session state if not exists
        if 'spoc_linkedin_profiles_list' not in st.session_state:
            st.session_state['spoc_linkedin_profiles_list'] = get_linkedin_profiles_list()
        
        # Create a single editable selectbox
        spoc_linkedin_profile = st.selectbox(
            label="SPOC LinkedIn Profile",
            options=[""] + st.session_state['spoc_linkedin_profiles_list'],
            key="spoc_linkedin_profile_selector",
            label_visibility="collapsed"
        )
    
    # Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])
    
    with col7:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Role 
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
            label="Target Role Selector", 
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
                        help=f"Edit target role: {role}",
                        label_visibility="collapsed"
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
    # Create dark container wrapper
    st.markdown("""
    <style>
    .dark-container {
        background-color: #1e2329;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #2d3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .section-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #3a4453;
    }

    .business-priority-container {
        background-color: #273042;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #3a4453;
    }

    .priority-item {
        margin-bottom: 15px;
        color: white;
    }

    .priority-description {
        margin-left: 25px;
        color: #b8c2cc;
        font-size: 14px;
        margin-top: 5px;
        line-height: 1.4;
    }

    .additional-specs {
        background-color: #2a3441;
        padding: 18px;
        border-radius: 8px;
        margin-top: 20px;
        border: 1px solid #3a4453;
    }

    .suggestion-box {
        background-color: #1a2332;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4a9eff;
    }

    .suggestion-title {
        color: #4a9eff;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .suggestion-content {
        color: #e2e8f0;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

    with col8:
        # Start dark container
        st.markdown('<div class="dark-container">', unsafe_allow_html=True)
        
        # LinkedIn Profile Section
        st.markdown('<div class="section-title">Select SPOC LinkedIn Profile</div>', unsafe_allow_html=True)
        linkedin_profile = st.selectbox(
            "Choose LinkedIn Profile",
            options=["Profile 1", "Profile 2", "Profile 3"],
            key="linkedin_profile_select",
            label_visibility="collapsed"
        )
        
        # Business Priorities Section
        st.markdown('<div class="section-title">Select SPOC Business Priorities</div>', unsafe_allow_html=True)
        
        # Define business priorities
        business_priorities_list = [
            {
                'icon': '🚀',
                'title': 'Digital Transformation Initiative',
                'description': 'Modernize business processes through digital technologies and automation'
            },
            {
                'icon': '📊',
                'title': 'Data Analytics & Business Intelligence',
                'description': 'Leverage data-driven insights for strategic decision making and operational efficiency'
            },
            {
                'icon': '⚙️',
                'title': 'Process Optimization & Automation',
                'description': 'Streamline workflows and automate repetitive tasks to improve productivity'
            }
        ]
        
        # Initialize session state for selected priorities
        if 'selected_business_priorities' not in st.session_state:
            st.session_state['selected_business_priorities'] = []
        
        # Display business priorities with functional checkboxes
        for i, priority in enumerate(business_priorities_list):
            business_priority_checkbox_key = f"business_priority_checkbox_{i}"
            
            # Create checkbox with custom styling
            is_priority_checked = st.checkbox(
                f"{priority['icon']} **{priority['title']}**", 
                key=business_priority_checkbox_key,
                help=f"Business Priority: {priority['description']} - Select if this aligns with client's strategic objectives."
            )
            
            # Display description below checkbox
            st.markdown(f'<div class="priority-description">{priority["description"]}</div>', unsafe_allow_html=True)
            
            # Update selected business priorities based on checkbox state
            if is_priority_checked and priority['title'] not in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].append(priority['title'])
            elif not is_priority_checked and priority['title'] in st.session_state['selected_business_priorities']:
                st.session_state['selected_business_priorities'].remove(priority['title'])
        
        # Additional Specifications Section
        st.markdown('<div class="section-title" style="margin-top: 30px;">Additional Specifications to be considered</div>', unsafe_allow_html=True)
        
        additional_specs = st.text_area(
            "Enter additional specifications",
            placeholder="Add any specific requirements or considerations...",
            key="additional_specs_input",
            label_visibility="collapsed",
            height=100
        )
        
        # AI Suggestions Section
        if additional_specs:
            st.markdown('''
            <div class="suggestion-box">
                <div class="suggestion-title">🤖 AI Suggestion 1 - Strategic Recommendations:</div>
                <div class="suggestion-content">
                    <strong>⚠️ Based on analysis, here are key strategic recommendations:</strong><br><br>
                    • Implement agile project management methodologies<br>
                    • Establish clear communication protocols<br>
                    • Define measurable success metrics and KPIs<br>
                    • Create a phased implementation timeline<br>
                    • Ensure stakeholder alignment and buy-in
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Display selected business priorities summary
        if st.session_state['selected_business_priorities']:
            st.markdown('<div class="section-title" style="margin-top: 25px;">Selected Business Priorities Summary:</div>', unsafe_allow_html=True)
            for priority in st.session_state['selected_business_priorities']:
                st.markdown(f'<div style="color: #4a9eff; margin: 5px 0;">• {priority}</div>', unsafe_allow_html=True)
        
        # Close dark container
        st.markdown('</div>', unsafe_allow_html=True)


    # New row with Client Additional Requirements and RFI Additional Specs
    col9, col10= st.columns([1, 1])
    
    with col9:
        st.markdown('''
        <div class="tooltip-label">
            Additional Client Requirements
            <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        client_additional_requirements = st.text_area(
            label="Additional Client Requirements", 
            placeholder="Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...", 
            height=200, 
            key="client_additional_requirements_textarea",
            label_visibility="collapsed"
        )
    
    with col10:
        st.markdown('''
        <div class="tooltip-label">
             Additional Specifications to be considered
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ℹ️</div>
        </div>
        ''', unsafe_allow_html=True)
        # Get AI suggestion 1 from function
        rfi_additional_specs_content = get_ai_suggestion_1()
        rfi_additional_specs = st.text_area(
            label="Additional Specifications", 
            value=rfi_additional_specs_content, 
            height=200, 
            key="rfi_additional_specs_textarea",
            label_visibility="collapsed"
        )

    # Handle validation trigger from main app
    if 'trigger_validation' in st.session_state and st.session_state.trigger_validation:
        st.session_state.show_validation = True
        st.session_state.trigger_validation = False