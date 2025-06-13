import streamlit as st
import asyncio
from utils import add_professional_css

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

# Initialize previous values for change detection - FIXED
if 'prev_seller_name' not in st.session_state:
    st.session_state.prev_seller_name = ""
if 'prev_website' not in st.session_state:
    st.session_state.prev_website = ""
if 'prev_uploaded_file' not in st.session_state:
    st.session_state.prev_uploaded_file = None

# Initialize file uploader key for forcing re-render
if 'file_uploader_key' not in st.session_state:
    st.session_state.file_uploader_key = 0

# Initialize form data in session state with default values
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'seller_name': '',
        'website_select': 'Select a platform...',
        'document_details': '',
        'client_requirement': ''
    }

def reset_downstream_fields(changed_field):
    """Reset fields that come after the changed field in the form hierarchy"""
    field_hierarchy = ['seller_name', 'website', 'file_upload', 'document_details']
    
    try:
        changed_index = field_hierarchy.index(changed_field)
        
        # Reset all fields that come after the changed field
        for i in range(changed_index + 1, len(field_hierarchy)):
            field = field_hierarchy[i]
            
            if field == 'website':
                # Reset website selection
                st.session_state.form_data['website_select'] = "Select a platform..."
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
                # Reset document details
                st.session_state.form_data['document_details'] = ""
        
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
    # Get current values from form_data
    current_seller = st.session_state.form_data.get('seller_name', '')
    current_website = st.session_state.form_data.get('website_select', '')
    current_file = st.session_state.get(f'uploaded_file_{st.session_state.file_uploader_key}')
    
    # Check seller name change
    if current_seller != st.session_state.prev_seller_name:
        if st.session_state.prev_seller_name != "":  # Only reset if there was a previous value
            reset_downstream_fields('seller_name')
            st.info("🔄 Seller name changed - subsequent fields have been reset")
        st.session_state.prev_seller_name = current_seller
    
    # Check website change
    if current_website != st.session_state.prev_website:
        if st.session_state.prev_website != "" and st.session_state.prev_website != "Select a platform...":  # Only reset if there was a previous value
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
    if not st.session_state.form_data.get('seller_name', '').strip():
        errors['seller_name'] = "Seller name is required"
    
    # Check website selection
    website_val = st.session_state.form_data.get('website_select', '')
    if not website_val or website_val == "Select a platform...":
        errors['website'] = "Please select a website/platform"
    
    # Check file upload using dynamic key
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    if not st.session_state.get(file_key):
        errors['file_upload'] = "RFI document upload is required"
    
    # Check document details
    if not st.session_state.form_data.get('document_details', '').strip():
        errors['document_details'] = "Document details are required"
    
    st.session_state.validation_errors = errors
    return len(errors) == 0

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

def move_to_website():
    st.session_state.focus_website = True

# Callback functions for form fields
def update_seller_name():
    st.session_state.form_data['seller_name'] = st.session_state.seller_name_input

def update_website():
    st.session_state.form_data['website_select'] = st.session_state.website_select_input

def update_document_details():
    st.session_state.form_data['document_details'] = st.session_state.document_details_input

def update_client_requirement():
    st.session_state.form_data['client_requirement'] = st.session_state.client_req_input

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
        value=st.session_state.form_data['seller_name'],
        placeholder="Enter the seller's full name or company name",
        on_change=update_seller_name,
        key="seller_name_input",
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
        
        # Get current index for selectbox
        current_website = st.session_state.form_data['website_select']
        options = ["Select a platform..."] + website_options
        try:
            index = options.index(current_website)
        except ValueError:
            index = 0
            
        website = st.selectbox(
            "Website/Platform",
            options=options,
            index=index,
            on_change=update_website,
            key="website_select_input",
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
        value=st.session_state.form_data['document_details'],
        placeholder="Please provide:\n• Document summary\n• Key requirements\n• Specific details or constraints\n• Timeline information\n• Any other relevant information...",
        height=150,
        help="Provide detailed information about the RFI document",
        on_change=update_document_details,
        key="document_details_input",
        label_visibility="collapsed"
    )
    
    show_field_validation_message('document_details', document_details)

# Initialize session state for suggestions
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
    
    client_requirement = st.text_area(
        "Project Description or Client Requirements",
        value=st.session_state.form_data['client_requirement'],
        height=280,
        on_change=update_client_requirement,
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
                        
                        if st.session_state.form_data['client_requirement'].strip():
                            st.session_state.form_data['client_requirement'] += f"\n\n• {detailed_description}"
                        else:
                            st.session_state.form_data['client_requirement'] = f"• {detailed_description}"
                        
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

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔍 Validate Form", type="primary", use_container_width=True):
        st.session_state.show_validation = True
        website_value = st.session_state.form_data['website_select'] if st.session_state.form_data['website_select'] != "Select a platform..." else ""
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
    def reset_all_fields():
        """Reset all form fields to their initial state"""
        # Reset form data to default values
        st.session_state.form_data = {
            'seller_name': '',
            'website_select': 'Select a platform...',
            'document_details': '',
            'client_requirement': ''
        }
        
        # Reset file uploader by incrementing key
        st.session_state.file_uploader_key += 1
        
        # Clear file references
        if 'current_uploaded_file' in st.session_state:
            del st.session_state.current_uploaded_file
        
        # Reset previous values for change detection
        st.session_state.prev_seller_name = ""
        st.session_state.prev_website = ""
        st.session_state.prev_uploaded_file = None
        
        # Clear validation states
        st.session_state.validation_errors = {}
        st.session_state.show_validation = False
        
        # Reset suggestion-related states
        st.session_state.suggestions = []
        st.session_state.suggestion_details = {}
        st.session_state.temp_suggestion = ""
        st.session_state.suggestions_generated = False
        st.session_state.added_suggestions = set()
        
        # Clear any info popup states
        if 'show_info' in st.session_state:
            st.session_state.show_info = False

    if st.button("🔄 Reset All Fields", type="secondary", use_container_width=True, help="Clear all form data and start over"):
        reset_all_fields()
        st.success("✅ All fields have been reset!")
        st.rerun()

# Sidebar Progress and Information
with st.sidebar:
    st.markdown("""
    <div class="progress-container">
        <h3>📊 Form Progress</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate progress
    seller_filled = bool(st.session_state.form_data.get('seller_name', '').strip())
    website_filled = bool(st.session_state.form_data.get('website_select')) and st.session_state.form_data.get('website_select') != "Select a platform..."
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    file_filled = st.session_state.get(file_key) is not None
    details_filled = bool(st.session_state.form_data.get('document_details', '').strip())
    
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