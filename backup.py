import streamlit as st
import asyncio

# Initialize session state for focus control
if 'focus_website' not in st.session_state:
    st.session_state.focus_website = False

# Initialize session state for async data
if 'website_data' not in st.session_state:
    st.session_state.website_data = {}

# Initialize validation state
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = {}
if 'show_validation' not in st.session_state:
    st.session_state.show_validation = False

# Initialize previous values for change detection
if 'prev_seller_name' not in st.session_state:
    st.session_state.prev_seller_name = ""
if 'prev_website' not in st.session_state:
    st.session_state.prev_website = ""
if 'prev_uploaded_file' not in st.session_state:
    st.session_state.prev_uploaded_file = None

# Initialize file uploader key for forcing re-render
if 'file_uploader_key' not in st.session_state:
    st.session_state.file_uploader_key = 0
# Add these session state keys for widget recreation
if 'seller_key' not in st.session_state:
    st.session_state.seller_key = 0
if 'website_key' not in st.session_state:
    st.session_state.website_key = 0

def reset_downstream_fields(changed_field):
    """Reset fields that come after the changed field in the form hierarchy"""
    field_hierarchy = ['seller_name', 'website', 'file_upload', 'document_details']
    
    try:
        changed_index = field_hierarchy.index(changed_field)
        
        # Reset all fields that come after the changed field
        for i in range(changed_index + 1, len(field_hierarchy)):
            field = field_hierarchy[i]
            
            if field == 'website':
                # Reset website by incrementing its key (forces widget recreation)
                st.session_state.website_key += 1
                st.session_state.prev_website = ""
                # Clear info popup state
                if 'show_info' in st.session_state:
                    st.session_state.show_info = False
            
            elif field == 'file_upload':
                # For file uploader, increment key to force re-render
                st.session_state.file_uploader_key += 1
                st.session_state.prev_uploaded_file = None
                # Clear any stored file reference
                if 'current_uploaded_file' in st.session_state:
                    del st.session_state.current_uploaded_file
            
            elif field == 'document_details':
                # Reset document details by clearing the session state
                if 'document_details' in st.session_state:
                    del st.session_state.document_details
        
        # Clear validation errors for reset fields
        fields_to_clear = field_hierarchy[changed_index + 1:]
        for field in fields_to_clear:
            if field in st.session_state.validation_errors:
                del st.session_state.validation_errors[field]
        
        # Reset validation display
        st.session_state.show_validation = False
        
    except ValueError:
        pass  # Field not in hierarchy

def check_for_changes():
    """Check if any field has changed and trigger cascading reset if needed"""
    # Get current values using dynamic keys
    seller_key = f"seller_name_input_{st.session_state.seller_key}"
    website_key = f"website_select_{st.session_state.website_key}"
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    
    current_seller = st.session_state.get(seller_key, '')
    current_website = st.session_state.get(website_key, '')
    current_file = st.session_state.get(file_key)
    
    # Check seller name change
    if current_seller != st.session_state.prev_seller_name:
        if st.session_state.prev_seller_name != "":  # Only reset if there was a previous value
            reset_downstream_fields('seller_name')
            st.info("🔄 Seller name changed - subsequent fields have been reset")
        st.session_state.prev_seller_name = current_seller
    
    # Check website change
    if current_website != st.session_state.prev_website:
        if st.session_state.prev_website != "":  # Only reset if there was a previous value
            reset_downstream_fields('website')
            st.info("🔄 Website changed - subsequent fields have been reset")
        st.session_state.prev_website = current_website
    
    # Check file upload change (comparing file names to detect changes)
    current_file_name = current_file.name if current_file else None
    prev_file_name = st.session_state.prev_uploaded_file.name if st.session_state.prev_uploaded_file else None
    
    if current_file_name != prev_file_name:
        if st.session_state.prev_uploaded_file is not None:  # Only reset if there was a previous file
            reset_downstream_fields('file_upload')
            st.info("🔄 File changed - document details have been reset")
        st.session_state.prev_uploaded_file = current_file


def validate_required_fields():
    """Validate all required fields and return validation status"""
    errors = {}
    
    # Check seller name
    if not st.session_state.get('seller_name_input', '').strip():
        errors['seller_name'] = "Seller name is required"
    
    # Check website selection
    if not st.session_state.get('website_select'):
        errors['website'] = "Please select a website/platform"
    
    # Check file upload using dynamic key
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    if not st.session_state.get(file_key):
        errors['file_upload'] = "RFI document upload is required"
    
    # Check document details
    if not st.session_state.get('document_details', '').strip():
        errors['document_details'] = "Document details are required"
    
    st.session_state.validation_errors = errors
    return len(errors) == 0

def show_validation_error(field_name):
    """Display validation error for a specific field"""
    if field_name in st.session_state.validation_errors:
        st.error(f"⚠️ {st.session_state.validation_errors[field_name]}")

def add_professional_css():
    """Add professional CSS styling"""
    st.markdown("""
    <style>
    /* Global styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1200px;
        background: #1a1a1a;
    }
    
    /* Header styling - more compact */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #f0f0f0;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 600;
        color: #f0f0f0;
    }
    
    .main-header p {
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        color: #f0f0f0;
    }
    
    /* Section styling - much more compact */
    .form-section {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        border: 1px solid #444;
        background: #2d2d2d;
    }
    
    .section-title {
        color: #e0e0e0;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #3498db;
    }
    
    /* Form field styling */
    .field-label {
        color: #d0d0d0;
        font-weight: 600;
        margin-bottom: 0.3rem;
        display: block;
        font-size: 0.9rem;
    }
    
    .required-asterisk {
        color: #e74c3c;
        font-weight: bold;
        margin-left: 3px;
    }
    
    /* Input field improvements - more compact */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #555;
        padding: 0.5rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 6px;
        border: 1px solid #555;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #555;
        padding: 0.5rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    /* File uploader styling - more compact */
    .stFileUploader > div {
        border: 2px dashed #666;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        background: #333;
        color: #d0d0d0;
    }
    
    .stFileUploader > div:hover {
        border-color: #3498db;
        background: #404040;
    }
    
    /* Button styling - more compact */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        padding: 0.4rem 1rem;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3498db, #2980b9);
        border: none;
        color: #f0f0f0;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2980b9, #21618c);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="secondary"] {
        border: 2px solid #666;
        color: #d0d0d0;
        background: #3a3a3a;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #555;
        border-color: #777;
    }
    
    /* Link button styling - more compact */
    .external-link-btn {
        background: #27ae60;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        display: inline-block;
        font-size: 0.8rem;
        color: #f0f0f0;
    }
    
    .external-link-btn:hover {
        background: #219a52;
        transform: translateY(-1px);
        text-decoration: none;
        color: #f0f0f0;
    }
    
    /* Validation styling - more compact */
    .validation-success {
        color: #27ae60;
        font-size: 0.8rem;
        margin-top: 0.3rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .validation-error {
        color: #e74c3c;
        font-size: 0.8rem;
        margin-top: 0.3rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Progress styling - more compact */
    .progress-container {
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.3);
        border: 1px solid #444;
        background: #2d2d2d;
        color: #e0e0e0;
    }
    
    /* Info styling - more compact */
    .info-container {
        background: #333;
        border-left: 4px solid #3498db;
        padding: 0.8rem;
        border-radius: 0 6px 6px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #d0d0d0;
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Compact sidebar */
    .css-1d391kg {
        padding-top: 1rem;
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* General dark theme colors */
    .stApp {
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Streamlit element colors */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Hide default streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def get_field_validation_class(field_name, value):
    """Get CSS class based on field validation status"""
    if not st.session_state.show_validation:
        return ""
    
    if field_name in st.session_state.validation_errors:
        return "invalid"
    elif value and str(value).strip():
        return "valid"
    return ""

def show_field_validation_message(field_name, value):
    """Show validation message for a field"""
    if not st.session_state.show_validation:
        return
        
    if field_name in st.session_state.validation_errors:
        st.markdown(f"""
        <div class="validation-error">
            <span>⚠️</span>
            <span>{st.session_state.validation_errors[field_name]}</span>
        </div>
        """, unsafe_allow_html=True)
    elif value and str(value).strip():
        st.markdown(f"""
        <div class="validation-success">
            <span>✅</span>
            <span>Field completed</span>
        </div>
        """, unsafe_allow_html=True)


def get_pain_point_suggestions(problem_statement):
    """
    Returns pain point suggestions in the format:
    {'Short 2-liner key': 'Detailed summary to be appended'}
    
    Replace this function with your actual AI/API call that returns
    suggestions in the same dictionary format.
    """
    
    suggestions = {
            'Process Automation Needs': 'Manual processes are creating bottlenecks and inefficiencies. Identify automation opportunities, implement workflow management systems, and establish process standardization across departments.',
            
            'Technology Integration Issues': 'Disconnected systems are causing data silos and operational inefficiencies. Plan system integration roadmap, implement API connectivity, and establish data synchronization protocols.',
            
            'Scalability Challenges': 'Current infrastructure cannot support business growth plans. Assess scalability requirements, plan for increased capacity, and implement scalable technology solutions.'
        }
    
    return suggestions


def move_to_website():
    st.session_state.focus_website = True

# Check for changes before rendering the form
check_for_changes()

# Add professional CSS styling
add_professional_css()

# Header section
st.markdown("""
<div class="main-header">
    <h1>Seller Info Collection</h1>
    <p>Request for Information - Seller & Document Management System</p>
</div>
""", unsafe_allow_html=True)

# Seller Information Section
st.markdown("""
<div class="form-section">
    <div class="section-title">👤 Seller Information</div>
</div>
""", unsafe_allow_html=True)

# Create columns for seller info
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="field-label">Seller Name <span class="required-asterisk">*</span></div>', unsafe_allow_html=True)

    seller_name = st.text_input(
    "Seller Name", 
    placeholder="Enter the seller's full name or company name",
    on_change=move_to_website,
    key=f"seller_name_input_{st.session_state.seller_key}",
    help="This field is required",
    label_visibility="collapsed"
        )

    show_field_validation_message('seller_name', seller_name)

with col2:
    # Website dropdown with professional options
    website_options = [
        "Amazon Marketplace",
        "eBay",
        "Shopify Store", 
        "Etsy",
        "Facebook Marketplace",
        "WooCommerce",
        "BigCommerce",
        "Other Platform"
    ]
    
    website_urls = {
        "Amazon Marketplace": "https://www.amazon.com",
        "eBay": "https://www.ebay.com",
        "Shopify Store": "https://www.shopify.com",
        "Etsy": "https://www.etsy.com",
        "Facebook Marketplace": "https://www.facebook.com/marketplace",
        "WooCommerce": "https://woocommerce.com",
        "BigCommerce": "https://www.bigcommerce.com",
        "Other Platform": "#"
    }
    
    # Create sub-columns for dropdown and link
    subcol1, subcol2 = st.columns([4, 1])
    
    with subcol1:
        st.markdown('<div class="field-label">Website/Platform <span class="required-asterisk">*</span></div>', unsafe_allow_html=True)
        website = st.selectbox(
            "Website/Platform",
            options=["Select a platform..."] + website_options,
            key=f"website_select_{st.session_state.website_key}",
            help="This field is required",
            label_visibility="collapsed"
        )
        show_field_validation_message('website', website if website != "Select a platform..." else "")
    
    with subcol2:
        st.write("&nbsp;")  # Add some space
        if website and website != "Select a platform...":
            url = website_urls.get(website, "#")
            if url != "#":
                st.markdown(f'<a href="{url}" target="_blank" class="external-link-btn">Visit Site</a>', unsafe_allow_html=True)

# Document Upload Section
st.markdown("""
<div class="form-section">
    <div class="section-title">📄 Document Upload & Details</div>
</div>
""", unsafe_allow_html=True)

# Create columns for file upload and details
col1, col2 = st.columns([1, 1])

# Left column - File upload section
with col1:
    st.markdown('<div class="field-label">Upload RFI Document <span class="required-asterisk">*</span></div>', unsafe_allow_html=True)
    
    # File uploader with dynamic key
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    uploaded_file = st.file_uploader(
        "Choose your RFI document",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Supported formats: PDF, DOCX, DOC, TXT (Max size: 200MB)",
        key=file_key,
        label_visibility="collapsed"
    )
    
    show_field_validation_message('file_upload', uploaded_file)
    
    # Display file information if uploaded
    if uploaded_file is not None:
        st.markdown("""
        <div class="info-container">
            <strong>✅ Document uploaded successfully!</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # File details
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.markdown(f"""
        **📋 File Details:**
        - **Name:** {uploaded_file.name}
        - **Type:** {uploaded_file.type}
        - **Size:** {file_size_mb:.2f} MB
        """)
    else:
        st.markdown("""
        <div class="info-container">
            <strong>📤 Please upload your RFI document</strong><br>
            Drag and drop your file here or click to browse
        </div>
        """, unsafe_allow_html=True)

# Right column - Document details section
with col2:
    st.markdown('<div class="field-label">Document Details <span class="required-asterisk">*</span></div>', unsafe_allow_html=True)
    
    # Text area for writing details
    document_details = st.text_area(
        "Document Details",
        placeholder="Please provide:\n• Document summary\n• Key requirements\n• Specific details or constraints\n• Timeline information\n• Any other relevant information...",
        height=200,
        help="Provide detailed information about the RFI document",
        key="document_details",
        label_visibility="collapsed"
    )
    
    show_field_validation_message('document_details', document_details)





# Initialize session state
if "client_requirement" not in st.session_state:
    st.session_state.client_requirement = ""
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "suggestion_details" not in st.session_state:
    st.session_state.suggestion_details = {}
if "temp_suggestion" not in st.session_state:
    st.session_state.temp_suggestion = ""
if "suggestions_generated" not in st.session_state:
    st.session_state.suggestions_generated = False
if "added_suggestions" not in st.session_state:
    st.session_state.added_suggestions = set()  # Track added suggestions

# Create two equal columns with custom HTML container
st.markdown('<div class="column-container">', unsafe_allow_html=True)

# Create the columns using Streamlit
left_col, right_col = st.columns([1, 1], gap="medium")

# LEFT COLUMN: Text area for client requirements
with left_col:
    st.markdown("""
    <div class="left-column">
        <div class="column-header">📋 Project Description or Client Requirements <span class="required-asterisk">*</span></div>
        <div class="column-content">
    """, unsafe_allow_html=True)
    
    st.session_state.client_requirement = st.text_area(
        "Project Description or Client Requirements",
        value=st.session_state.client_requirement,
        height=350,
        key="client_req_input",
        placeholder="Enter the client's project requirements, objectives, and specifications here...",
        label_visibility="collapsed"
    )
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# RIGHT COLUMN: Suggestions and Autocomplete
with right_col:
    st.markdown("""
    <div class="right-column">
        <div class="column-header">🤖 AI-Powered Suggestions</div>
        <div class="column-content">
    """, unsafe_allow_html=True)
    
    # Generate button at the top
    if st.button("🔮 Generate Suggestions", type="primary", use_container_width=True, key="generate_btn"):
        try:
            with st.spinner("Generating AI-powered suggestions..."):
                # Store the dictionary in session state
                st.session_state.suggestion_details = {
                    'Enhanced User Experience': 'Implement intuitive UI/UX design with responsive layouts, accessibility features, and user-friendly navigation to improve overall user satisfaction and engagement.',
                    'Performance Optimization': 'Optimize application performance through code refactoring, database optimization, caching strategies, and efficient resource management.',
                    'Security Implementation': 'Integrate comprehensive security measures including data encryption, user authentication, authorization protocols, and vulnerability assessments.'
                }
                st.session_state.suggestions = list(st.session_state.suggestion_details.keys())
                st.session_state.temp_suggestion = ""  # Reset selection
                st.session_state.suggestions_generated = True
                st.session_state.added_suggestions = set()  # Reset added suggestions
        except Exception as e:
            st.error(f"Error generating suggestions: {str(e)}")
    
    # Suggestions content area
    if st.session_state.suggestions_generated and st.session_state.suggestions:
        # Display suggestions using streamlit components in a scrollable container
        for i, suggestion in enumerate(st.session_state.suggestions):
            is_added = suggestion in st.session_state.added_suggestions
            
            col1, col2 = st.columns([1, 9])
            
            with col1:
                # Change button appearance based on whether it's already added
                if is_added:
                    st.button("✅", key=f"added_{i}", disabled=True, help="Already added", use_container_width=True)
                else:
                    if st.button("➕", key=f"add_{i}", help="Add to requirements", use_container_width=True):
                        # Get detailed description from session state dictionary
                        detailed_description = st.session_state.suggestion_details.get(
                            suggestion, f"• {suggestion}"
                        )
                        
                        if st.session_state.client_requirement.strip():
                            st.session_state.client_requirement += f"\n\n• {detailed_description}"
                        else:
                            st.session_state.client_requirement = f"• {detailed_description}"
                        
                        # Mark this suggestion as added
                        st.session_state.added_suggestions.add(suggestion)
                        st.session_state.temp_suggestion = suggestion
                        st.rerun()
            
            with col2:
                # Use different styling for added suggestions
                if is_added:
                    st.markdown(f"""
                    <div class="suggestion-container suggestion-added">
                        <div class="suggestion-title">✅ {suggestion} (Added)</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="suggestion-container">
                        <div class="suggestion-title">💡 {suggestion}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif st.session_state.suggestions_generated and not st.session_state.suggestions:
        st.markdown("""
        <div class="warning-container">
            <div>
                <strong>⚠️ No suggestions found</strong><br>
                Try modifying your requirements or check if data is available.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="info-container">
            <div>
                <strong>🚀 Get AI-Powered Recommendations</strong><br>
                Click 'Generate Suggestions' to get intelligent recommendations for your project requirements based on industry best practices and common client needs.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons at the bottom (only show if suggestions are generated)
    if st.session_state.suggestions_generated:
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🗑️ Clear", type="secondary", use_container_width=True, key="clear_btn"):
                st.session_state.suggestions = []
                st.session_state.suggestion_details = {}
                st.session_state.temp_suggestion = ""
                st.session_state.suggestions_generated = False
                st.session_state.added_suggestions = set()  # Clear added suggestions
                st.rerun()
        with col2:
            if st.button("🔄 Refresh", type="secondary", use_container_width=True, key="refresh_btn"):
                try:
                    with st.spinner("Refreshing suggestions..."):
                        # Generate new suggestions using the same function
                        st.session_state.suggestion_details = {
                            'Advanced Analytics': 'Implement comprehensive analytics dashboard with real-time data visualization, custom reporting features, and predictive analytics capabilities.',
                            'Mobile Compatibility': 'Ensure full mobile responsiveness with native app features, offline functionality, and optimized mobile user interface.',
                            'Integration Capabilities': 'Develop robust API integration with third-party services, seamless data synchronization, and automated workflow connections.'
                        }
                        st.session_state.suggestions = list(st.session_state.suggestion_details.keys())
                        st.session_state.temp_suggestion = ""
                        st.session_state.added_suggestions = set()  # Reset added suggestions
                        st.rerun()
                except Exception as e:
                    st.error(f"Error refreshing suggestions: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Action Buttons Section
st.markdown("""
<div class="form-section">
    <div class="section-title">🔧 Form Actions</div>
</div>
""", unsafe_allow_html=True)
# Replace your Problem Statement & AI Suggestions Section with this fixed version:



col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔍 Validate Form", type="primary", use_container_width=True):
        st.session_state.show_validation = True
        website_value = website if website != "Select a platform..." else ""
        # Update validation for website
        if not website_value:
            st.session_state.validation_errors['website'] = "Please select a website/platform"
        elif 'website' in st.session_state.validation_errors:
            del st.session_state.validation_errors['website']
            
        if validate_required_fields():
            st.success("✅ All required fields are completed!")
            st.balloons()
        else:
            st.error("❌ Please complete all required fields marked with *")
            st.rerun()

with col2:
    if st.button("💾 Save Draft", type="secondary", use_container_width=True):
        st.info("💾 Form progress saved as draft")

with col3:
    if st.button("🔄 Reset Form", type="secondary", use_container_width=True):
        # Reset all fields by incrementing their keys (forces widget recreation)
        st.session_state.seller_key += 1
        st.session_state.website_key += 1
        st.session_state.file_uploader_key += 1
        
        # Clear document details
        if 'document_details' in st.session_state:
            del st.session_state.document_details
        
        # Reset previous values
        st.session_state.prev_seller_name = ""
        st.session_state.prev_website = ""
        st.session_state.prev_uploaded_file = None
        
        # Clear validation
        st.session_state.validation_errors = {}
        st.session_state.show_validation = False
        
        # Clear AI suggestions
        st.session_state.client_requirement = ""
        st.session_state.suggestions = []
        st.session_state.suggestion_details = {}
        st.session_state.temp_suggestion = ""
        st.session_state.suggestions_generated = False
        st.session_state.added_suggestions = set()
        
        st.success("🔄 Form has been reset successfully!")
        st.rerun()
# Sidebar Progress and Information
with st.sidebar:
    st.markdown("""
    <div class="progress-container">
        <h3>📊 Form Progress</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate progress
    seller_filled = bool(st.session_state.get('seller_name_input', '').strip())
    website_filled = bool(st.session_state.get('website_select')) and st.session_state.get('website_select') != "Select a platform..."
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    file_filled = st.session_state.get(file_key) is not None
    details_filled = bool(st.session_state.get('document_details', '').strip())
    
    # Progress indicators
    st.markdown(f"{'✅' if seller_filled else '❌'} **Seller Name**")
    st.markdown(f"{'✅' if website_filled else '❌'} **Website/Platform**")
    st.markdown(f"{'✅' if file_filled else '❌'} **RFI Document**")
    st.markdown(f"{'✅' if details_filled else '❌'} **Document Details**")
    
    progress = sum([seller_filled, website_filled, file_filled, details_filled]) / 4
    st.progress(progress, text=f"**{int(progress * 100)}% Complete**")
    
    # Show validation errors if any
    if st.session_state.validation_errors:
        st.markdown("---")
        st.markdown("### ⚠️ Issues to Fix:")
        for field, error in st.session_state.validation_errors.items():
            st.markdown(f"• {error}")
    
    # Cascade reset information
    st.markdown("---")
    st.markdown("### 🔄 Smart Reset Feature")
    st.markdown("""
    **Automatic field reset:**
    • Changing seller → resets all below
    • Changing platform → resets file & details  
    • Changing file → resets details
    
    This ensures data consistency.
    """)