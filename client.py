import streamlit as st
import pandas as pd
from typing import List

# Custom CSS for dark theme styling
st.markdown("""
<style>
    .client-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        color: #f8f9fa;
    }
    
    .url-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #764ba2;
        margin-bottom: 1rem;
        color: #f8f9fa;
    }
    
    .document-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #3a3a3a;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        color: #f8f9fa;
    }
    
    .pain-points-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        color: #f8f9fa;
    }
    
    .roles-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        color: #f8f9fa;
    }
    
    .priorities-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #9c27b0;
        color: #f8f9fa;
    }
    
    .ai-suggestion-section {
        background: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00bcd4;
        color: #f8f9fa;
    }
    
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #2a2a2a;
        color: #f8f9fa;
    }
    
    /* Style section headers */
    .section-header {
        color: #f8f9fa;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Mandatory field styling */
    .mandatory-label {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .field-warning {
        color: #e74c3c;
        font-size: 0.85rem;
        margin-top: 0.25rem;
        font-weight: 500;
        background: rgba(231, 76, 60, 0.1);
        padding: 0.5rem;
        border-radius: 4px;
        border-left: 3px solid #e74c3c;
    }
    
    .optional-label {
        color: #95a5a6;
        font-size: 0.8rem;
        font-style: italic;
    }
    
    .ai-label {
        color: #00bcd4;
        font-size: 0.8rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Function to get URLs (placeholder function)
def get_urls_list() -> List[str]:
    """
    Placeholder function that returns a list of URLs
    Replace this with your actual function that fetches URLs
    """
    return [
        "https://example1.com",
        "https://example2.com", 
        "https://api-endpoint1.com",
        "https://api-endpoint2.com",
        "https://dashboard.company.com"
    ]

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

# Function to get URL details (new function for popup)
def get_url_details(url: str) -> str:
    """
    Function that returns detailed information about a specific URL
    Replace this with your actual function that fetches URL details
    """
    # Mock data - replace with your actual implementation
    url_details_data = {
        "https://example1.com": {
            "title": "Example Website 1",
            "description": "This is the primary company website with product information and contact details.",
            "status": "Active",
            "last_updated": "2024-01-15",
            "purpose": "Marketing & Sales",
            "access_level": "Public"
        },
        "https://example2.com": {
            "title": "Example Website 2", 
            "description": "Secondary website for customer support and documentation.",
            "status": "Active",
            "last_updated": "2024-01-10",
            "purpose": "Customer Support",
            "access_level": "Public"
        },
        "https://api-endpoint1.com": {
            "title": "API Endpoint 1",
            "description": "REST API for user authentication and management.",
            "status": "Active",
            "last_updated": "2024-01-20",
            "purpose": "Authentication API",
            "access_level": "Restricted"
        },
        "https://api-endpoint2.com": {
            "title": "API Endpoint 2",
            "description": "Data processing API for analytics and reporting.",
            "status": "Under Maintenance",
            "last_updated": "2024-01-18",
            "purpose": "Analytics API",
            "access_level": "Internal"
        },
        "https://dashboard.company.com": {
            "title": "Company Dashboard",
            "description": "Internal dashboard for monitoring system metrics and KPIs.",
            "status": "Active",
            "last_updated": "2024-01-22",
            "purpose": "Internal Monitoring",
            "access_level": "Internal"
        }
    }
    
    details = url_details_data.get(url, {
        "title": "Unknown URL",
        "description": "No detailed information available for this URL.",
        "status": "Unknown",
        "last_updated": "N/A",
        "purpose": "N/A",
        "access_level": "Unknown"
    })
    
    return f"""
    <div style="background: #2a2a2a; padding: 1rem; border-radius: 8px; border-left: 4px solid #007bff;">
        <h4 style="color: #7bff; margin-top: 0;">{details['title']}</h4>
        <p><strong>URL:</strong> <code>{url}</code></p>
        <p><strong>Description:</strong> {details['description']}</p>
        <p><strong>Status:</strong> <span style="color: {'#28a745' if details['status'] == 'Active' else '#ffc107' if details['status'] == 'Under Maintenance' else '#dc3545'};">{details['status']}</span></p>
        <p><strong>Last Updated:</strong> {details['last_updated']}</p>
        <p><strong>Purpose:</strong> {details['purpose']}</p>
        <p><strong>Access Level:</strong> {details['access_level']}</p>
    </div>
    """

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

# Function to extract pain points from document (placeholder function)
def extract_pain_points(document_content: str) -> str:
    """
    Placeholder function that extracts pain points from document content
    Replace this with your actual pain point extraction logic
    """
    return """Based on the uploaded document, here are the identified pain points:

1. **Process Inefficiencies**: Manual processes are causing delays in workflow
2. **Communication Gaps**: Lack of clear communication channels between teams
3. **Resource Constraints**: Limited budget allocation for critical operations
4. **Technology Limitations**: Outdated systems affecting productivity
5. **Quality Control Issues**: Inconsistent quality standards across departments

These pain points require immediate attention and strategic planning to resolve."""

# Function to get editable content (placeholder function)
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

# Function to get pain points display (placeholder function)
def get_pain_points_display() -> str:
    """
    Placeholder function that returns pain points for display
    Replace this with your actual function that fetches pain points
    """
    return """Current Pain Points Summary:

• User Experience Issues
• Performance Bottlenecks
• Integration Challenges
• Scalability Concerns
• Maintenance Overhead
• Resource Allocation Problems

These are automatically generated pain points from analysis."""

# Function to get AI suggestion 1 (placeholder function)
def get_ai_suggestion_1() -> str:
    """
    Placeholder function that returns AI suggestion 1
    Replace this with your actual AI suggestion logic
    """
    return """AI Suggestion 1 - Strategic Recommendations:

🎯 Based on analysis, here are key strategic recommendations:

• Implement agile project management methodologies
• Establish clear communication protocols
• Invest in automation tools for repetitive tasks
• Create a centralized knowledge management system
• Develop cross-functional team collaboration frameworks

These suggestions are generated based on industry best practices and current client requirements."""

# Function to get AI suggestion 2 (placeholder function)
def get_ai_suggestion_2() -> str:
    """
    Placeholder function that returns AI suggestion 2
    Replace this with your actual AI suggestion logic
    """
    return """AI Suggestion 2 - Technical Solutions:

⚡ Recommended technical implementations:

• Cloud migration strategy for scalability
• API-first architecture for better integration
• Real-time monitoring and alerting systems
• Automated testing and deployment pipelines
• Data governance and security protocols

These technical solutions align with modern development practices and client infrastructure needs."""

def check_field_validation(field_name: str, field_value: str, is_mandatory: bool = False) -> bool:
    """Check if field validation should show warning"""
    if is_mandatory and not field_value.strip():
        return True
    return False

def show_field_warning(field_name: str):
    """Show warning message for mandatory fields"""
    st.markdown(f'<div class="field-warning">⚠️ {field_name} is mandatory and cannot be empty!</div>', unsafe_allow_html=True)

# Main App
def client_tab():
    # Initialize validation trigger
    if 'show_validation' not in st.session_state:
        st.session_state.show_validation = False
    
    # Initialize URL details popup state
    if 'show_url_details' not in st.session_state:
        st.session_state.show_url_details = False
    if 'selected_url_for_details' not in st.session_state:
        st.session_state.selected_url_for_details = ''
    
    # Top section with client name and URLs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<span class="mandatory-label">Client Name *</span>', unsafe_allow_html=True)
        client_name = st.text_input(
            label="Client Name Input", 
            placeholder="Enter client name...", 
            key="client_name_input", 
            label_visibility="collapsed"
        )
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Name", client_name, True):
            show_field_warning("Client Name")
    
    with col2:
        st.markdown('<span class="optional-label">Select URL (Optional)</span>', unsafe_allow_html=True)
        
        # Initialize URLs in session state if not exists
        if 'urls_list' not in st.session_state:
            st.session_state['urls_list'] = get_urls_list()
        
        # Create columns for selectbox and buttons all in same line
        url_col, refresh_col, open_col, details_col = st.columns([3, 0.5, 0.5, 0.5])
        
        with url_col:
            selected_url = st.selectbox(
                label="URL Selector", 
                options=st.session_state['urls_list'], 
                key="url_selector", 
                label_visibility="collapsed"
            )
        
        with refresh_col:
            if st.button("🔄", key="refresh_urls_btn", help="Refresh suggested links", use_container_width=True):
                st.session_state['urls_list'] = get_urls_list()
                st.rerun()
        
        with open_col:
            if st.button("🌐", key="open_website_btn", help="Open selected website", use_container_width=True):
                if selected_url:
                    st.markdown(f'<a href="{selected_url}" target="_blank">Opening {selected_url}</a>', unsafe_allow_html=True)
                    # Alternative: Use st.link_button if you prefer (Streamlit 1.29+)
                    # st.link_button("Open Website", selected_url)
        
        with details_col:
            if st.button("ℹ️", key="url_details_btn", help="Get more details about selected URL", use_container_width=True):
                if selected_url:
                    st.session_state['show_url_details'] = True
                    st.session_state['selected_url_for_details'] = selected_url
    
    # URL Details Popup/Modal (outside of columns to avoid layout issues)
    if st.session_state.get('show_url_details', False):
        url_details = get_url_details(st.session_state.get('selected_url_for_details', ''))
        
        # Create a modal-like container
        with st.container():
            st.markdown("### 🔍 URL Details")
            
            # Close button
            if st.button("❌ Close", key="close_url_details"):
                st.session_state['show_url_details'] = False
                st.rerun()
            
            # Display URL details
            st.markdown(url_details, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Document upload and pain points section
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown('<span class="optional-label">Upload Document (Optional)</span>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            label="Document Uploader", 
            type=['pdf', 'docx', 'txt', 'csv'], 
            key="doc_uploader", 
            label_visibility="collapsed",
        )
        
        if uploaded_file is not None and st.button("Analyze Document", key="analyze_btn"):
            with st.spinner("Processing..."):
                import time
                time.sleep(1)
                st.session_state['pain_points'] = extract_pain_points("document_content")
    
    with col4:
        st.markdown('<span class="optional-label">Pain Points (Optional)</span>', unsafe_allow_html=True)
        if 'pain_points' in st.session_state:
            pain_points_text = st.text_area(
                label="Pain Points Extracted", 
                value=st.session_state['pain_points'], 
                height=200, 
                key="pain_points_extracted", 
                label_visibility="collapsed"
            )
        else:
            pain_points_text = st.text_area(
                label="Pain Points Placeholder", 
                placeholder="Upload document and analyze to extract pain points...", 
                height=200, 
                key="pain_points_placeholder", 
                label_visibility="collapsed"
            )

    st.markdown("---")
    
    # Additional row with editable content and pain points display
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown('<span class="mandatory-label">Additional Content</span>', unsafe_allow_html=True)
        # Get editable content from function
        editable_content = get_editable_content()
        edited_content = st.text_area(
            label="Editable Content Area", 
            value=editable_content, 
            height=200, 
            key="editable_content_area", 
            label_visibility="collapsed"
        )
          
    with col6:
        st.markdown('<span class="optional-label">Summary (Auto-generated)</span>', unsafe_allow_html=True)
        # Get pain points display from function
        pain_points_display = get_pain_points_display()
        st.text_area(
            label="Pain Points Summary", 
            value=pain_points_display, 
            height=200, 
            disabled=True, 
            key="pain_points_summary", 
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    # Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])
    
    with col7:
        st.markdown('<span class="optional-label">Target Roles (Optional)</span>', unsafe_allow_html=True)
        
        # Get roles from function
        roles_list = get_roles_list()
        
        # Initialize session state for roles if not exists
        if 'selected_roles' not in st.session_state:
            st.session_state['selected_roles'] = []
        
        # Dropdown for adding roles
        new_role = st.selectbox(
            label="Role Selector Dropdown", 
            options=["Select a role..."] + roles_list, 
            key="role_selector_dropdown",
            label_visibility="collapsed"
        )
        
        # Add role button
        if st.button("Add Role", key="add_role_btn") and new_role != "Select a role...":
            if new_role not in st.session_state['selected_roles']:
                st.session_state['selected_roles'].append(new_role)
                # Force rerun to update the display
                st.rerun()
        
        # Display and manage selected roles
        if st.session_state['selected_roles']:
            st.write("**Selected Roles:**")
            roles_to_remove = []
            for i, role in enumerate(st.session_state['selected_roles']):
                col_role, col_remove = st.columns([4, 1])
                with col_role:
                    # Make role editable with unique key
                    edited_role = st.text_input(
                        label=f"Role Edit Input {i}", 
                        value=role, 
                        key=f"role_edit_input_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state['selected_roles'][i] = edited_role
                with col_remove:
                    if st.button("🗑️", key=f"remove_role_btn_{i}", help="Remove role"):
                        roles_to_remove.append(i)
            
            # Remove roles (in reverse order to maintain indices)
            for idx in reversed(roles_to_remove):
                st.session_state['selected_roles'].pop(idx)
                # Force rerun to update the display
                st.rerun()
    
    with col8:
        st.markdown('<span class="optional-label">Business Priorities (Optional)</span>', unsafe_allow_html=True)
        
        # Get priorities from function
        priorities_list = get_priority_suggestions()
        
        # Priority checkboxes
        st.write("**Select top priorities:**")
        
        # Initialize session state for selected priorities
        if 'selected_priorities' not in st.session_state:
            st.session_state['selected_priorities'] = []
        
        # Generate checkboxes dynamically from function
        for i, priority in enumerate(priorities_list):
            checkbox_key = f"priority_checkbox_{i}"
            is_checked = st.checkbox(
                f"{priority['icon']} **{priority['title']}**", 
                key=checkbox_key,
                help=priority['description']
            )
            
            # Update selected priorities based on checkbox state
            if is_checked and priority['title'] not in st.session_state['selected_priorities']:
                st.session_state['selected_priorities'].append(priority['title'])
            elif not is_checked and priority['title'] in st.session_state['selected_priorities']:
                st.session_state['selected_priorities'].remove(priority['title'])
        
        # Display selected priorities summary
        if st.session_state['selected_priorities']:
            st.write("**Selected Priorities:**")
            for priority in st.session_state['selected_priorities']:
                st.write(f"• {priority}")

    st.markdown("---")
  # New row with Client Requirements and AI Suggestions
    col9, col10= st.columns([1, 1])
    
    with col9:
        st.markdown('<span class="optional-label">Client Requirements (Optional)</span>', unsafe_allow_html=True)
        client_requirements = st.text_area(
            label="Client Requirements Input", 
            placeholder="Enter specific client requirements, expectations, and project scope...", 
            height=200, 
            key="client_requirements_input", 
            label_visibility="collapsed"
        )
    
    with col10:
        st.markdown('<span class="ai-label">AI Suggestion 1 (Editable)</span>', unsafe_allow_html=True)
        # Get AI suggestion 1 from function
        ai_suggestion_1 = get_ai_suggestion_1()
        edited_ai_suggestion_1 = st.text_area(
            label="AI Suggestion 1 Area", 
            value=ai_suggestion_1, 
            height=200, 
            key="ai_suggestion_1_area", 
            label_visibility="collapsed"
        )
        
        # Refresh button for AI suggestion 1
        if st.button("🔄 Refresh AI Suggestion 1", key="refresh_ai_1_btn", help="Generate new AI suggestion"):
            st.session_state['ai_suggestion_1_refreshed'] = get_ai_suggestion_1()
            st.rerun()
    


    st.markdown("---")
    # Handle validation trigger from main app
    if 'trigger_validation' in st.session_state and st.session_state.trigger_validation:
        st.session_state.show_validation = True
        st.session_state.trigger_validation = False