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

def reset_downstream_fields(changed_field):
    """Reset fields that come after the changed field in the form hierarchy"""
    field_hierarchy = ['seller_name', 'website', 'file_upload', 'document_details']
    
    try:
        changed_index = field_hierarchy.index(changed_field)
        
        # Reset all fields that come after the changed field
        for i in range(changed_index + 1, len(field_hierarchy)):
            field = field_hierarchy[i]
            
            if field == 'website':
                st.session_state.website_select = ""
                st.session_state.prev_website = ""
                # Clear website data cache
                st.session_state.website_data = {}
                # Clear info popup state
                if 'show_info' in st.session_state:
                    st.session_state.show_info = False
            
            elif field == 'file_upload':
                # For file uploader, we'll use a key increment to force re-render
                if 'file_uploader_key' not in st.session_state:
                    st.session_state.file_uploader_key = 0
                st.session_state.file_uploader_key += 1
                st.session_state.prev_uploaded_file = None
                # Clear any stored file reference
                if 'current_uploaded_file' in st.session_state:
                    del st.session_state.current_uploaded_file
            
            elif field == 'document_details':
                st.session_state.document_details = ""
        
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
    current_seller = st.session_state.get('seller_name_input', '')
    current_website = st.session_state.get('website_select', '')
    
    # Get current file using the dynamic key
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    current_file = st.session_state.get(file_key)
    
    # Check seller name change
    if current_seller != st.session_state.prev_seller_name:
        if st.session_state.prev_seller_name != "":  # Only reset if there was a previous value
            reset_downstream_fields('seller_name')
            st.success("🔄 Seller name changed - subsequent fields have been reset")
        st.session_state.prev_seller_name = current_seller
    
    # Check website change
    if current_website != st.session_state.prev_website:
        if st.session_state.prev_website != "":  # Only reset if there was a previous value
            reset_downstream_fields('website')
            st.success("🔄 Website changed - subsequent fields have been reset")
        st.session_state.prev_website = current_website
    
    # Check file upload change (comparing file names to detect changes)
    current_file_name = current_file.name if current_file else None
    prev_file_name = st.session_state.prev_uploaded_file.name if st.session_state.prev_uploaded_file else None
    
    if current_file_name != prev_file_name:
        if st.session_state.prev_uploaded_file is not None:  # Only reset if there was a previous file
            reset_downstream_fields('file_upload')
            st.success("🔄 File changed - document details have been reset")
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

def add_validation_css():
    """Add custom CSS for form validation styling"""
    st.markdown("""
    <style>
    /* Red border for invalid fields */
    .stTextInput > div > div > input.invalid {
        border: 2px solid #ff4444 !important;
        border-radius: 4px !important;
        background-color: #fff5f5 !important;
    }
    
    .stSelectbox > div > div > div.invalid {
        border: 2px solid #ff4444 !important;
        border-radius: 4px !important;
        background-color: #fff5f5 !important;
    }
    
    .stTextArea > div > div > textarea.invalid {
        border: 2px solid #ff4444 !important;
        border-radius: 4px !important;
        background-color: #fff5f5 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div.invalid {
        border: 2px solid #ff4444 !important;
        border-radius: 4px !important;
        background-color: #fff5f5 !important;
        padding: 10px !important;
    }
    
    /* Green border for valid fields */
    .stTextInput > div > div > input.valid {
        border: 2px solid #28a745 !important;
        border-radius: 4px !important;
        background-color: #f8fff8 !important;
    }
    
    .stSelectbox > div > div > div.valid {
        border: 2px solid #28a745 !important;
        border-radius: 4px !important;
        background-color: #f8fff8 !important;
    }
    
    .stTextArea > div > div > textarea.valid {
        border: 2px solid #28a745 !important;
        border-radius: 4px !important;
        background-color: #f8fff8 !important;
    }
    
    .stFileUploader > div > div.valid {
        border: 2px solid #28a745 !important;
        border-radius: 4px !important;
        background-color: #f8fff8 !important;
        padding: 10px !important;
    }
    
    /* Required field asterisk styling */
    .required-asterisk {
        color: #ff4444;
        font-weight: bold;
    }
    
    /* Error message styling */
    .validation-error {
        color: #ff4444;
        font-size: 14px;
        margin-top: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Success message styling */
    .validation-success {
        color: #28a745;
        font-size: 14px;
        margin-top: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Reset notification styling */
    .reset-notification {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
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

def move_to_website():
    st.session_state.focus_website = True

async def get_website_image_async(website_url):
    """Async function to get website image"""
    await asyncio.sleep(0.1)
    
    website_images = {
        "https://www.amazon.com": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1024px-Amazon_logo.svg.png",
        "https://www.ebay.com": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/1024px-EBay_logo.svg.png",
        "https://www.shopify.com": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Shopify_logo_2018.svg/1024px-Shopify_logo_2018.svg.png",
        "https://www.etsy.com": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Etsy_logo.svg/1024px-Etsy_logo.svg.png",
        "https://www.facebook.com/marketplace": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/1024px-Facebook_Logo_%282019%29.png",
    }
    return website_images.get(website_url)

async def get_website_colors_async(website_url):
    """Async function to get website colors"""
    await asyncio.sleep(0.1)
    
    website_colors = {
        "https://www.amazon.com": ["#FF9900", "#232F3E", "#FFFFFF"],
        "https://www.ebay.com": ["#E53238", "#0064D2", "#F7C41F"],
        "https://www.shopify.com": ["#95BF47", "#5E8E3E", "#004C3F"],
        "https://www.etsy.com": ["#F16521", "#F56500", "#D15600"],
        "https://www.facebook.com/marketplace": ["#1877F2", "#42B883", "#E7F3FF"],
    }
    return website_colors.get(website_url, ["#000000", "#666666", "#CCCCCC"])

async def load_website_data(website_url):
    """Load both image and colors data asynchronously"""
    image_task = get_website_image_async(website_url)
    colors_task = get_website_colors_async(website_url)
    
    image_url, colors = await asyncio.gather(image_task, colors_task)
    return image_url, colors

def get_or_load_website_data(website_url):
    """Get cached data or trigger loading for website"""
    if website_url not in st.session_state.website_data:
        st.session_state.website_data[website_url] = {'loading': True, 'image': None, 'colors': None}
        
        try:
            image_url, colors = asyncio.run(load_website_data(website_url))
            st.session_state.website_data[website_url] = {
                'loading': False, 
                'image': image_url, 
                'colors': colors
            }
            st.rerun()
        except:
            st.session_state.website_data[website_url]['loading'] = False
    
    return st.session_state.website_data[website_url]

# Check for changes before rendering the form
check_for_changes()

# Add custom CSS for validation styling
add_validation_css()

# First section - Seller info
st.title("Seller Information")

# Create two columns for left and right boxes
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Seller Name** <span class='required-asterisk'>*</span>", unsafe_allow_html=True)
    seller_name = st.text_input(
        "Seller Name", 
        placeholder="Enter seller name",
        on_change=move_to_website,
        key="seller_name_input",
        help="This field is required",
        label_visibility="collapsed"
    )
    
    # Add validation styling via JavaScript
    seller_validation_class = get_field_validation_class('seller_name', seller_name)
    if seller_validation_class:
        st.markdown(f"""
        <script>
        setTimeout(function() {{
            const inputs = document.querySelectorAll('input[aria-label="Seller Name"]');
            inputs.forEach(input => {{
                input.classList.add('{seller_validation_class}');
            }});
        }}, 100);
        </script>
        """, unsafe_allow_html=True)
    
    # Show validation message
    show_field_validation_message('seller_name', seller_name)

with col2:
    # Website dropdown with just URLs
    website_options = [
        "https://www.amazon.com",
        "https://www.ebay.com", 
        "https://www.shopify.com",
        "https://www.etsy.com",
        "https://www.facebook.com/marketplace",
    ]
    
    # Company information for the info popup
    company_info = {
        "https://www.amazon.com": {
            "name": "Amazon",
            "description": "World's largest online marketplace and cloud computing platform",
            "founded": "1994",
            "founder": "Jeff Bezos",
            "headquarters": "Seattle, Washington, USA",
            "services": "E-commerce, Cloud Computing (AWS), Digital Streaming, AI"
        },
        "https://www.ebay.com": {
            "name": "eBay",
            "description": "Global online marketplace for buying and selling goods",
            "founded": "1995", 
            "founder": "Pierre Omidyar",
            "headquarters": "San Jose, California, USA",
            "services": "Online Auctions, E-commerce, Payment Processing"
        },
        "https://www.shopify.com": {
            "name": "Shopify",
            "description": "E-commerce platform for online stores and retail point-of-sale systems",
            "founded": "2006",
            "founder": "Tobias Lütke, Daniel Weinand, Scott Lake",
            "headquarters": "Ottawa, Ontario, Canada", 
            "services": "E-commerce Platform, Payment Processing, Inventory Management"
        },
        "https://www.etsy.com": {
            "name": "Etsy",
            "description": "Global marketplace for unique and creative goods",
            "founded": "2005",
            "founder": "Rob Kalin, Chris Maguire, Haim Schoppik",
            "headquarters": "Brooklyn, New York, USA",
            "services": "Handmade Goods, Vintage Items, Craft Supplies"
        },
        "https://www.facebook.com/marketplace": {
            "name": "Facebook Marketplace",
            "description": "Local buying and selling platform within Facebook",
            "founded": "2016",
            "parent_company": "Meta (formerly Facebook)",
            "headquarters": "Menlo Park, California, USA",
            "services": "Local Commerce, Community Marketplace, Social Shopping"
        }
    }

    # Create sub-columns for dropdown and buttons
    subcol1, subcol2, subcol3, subcol4 = st.columns([3, 1, 1, 1])
    
    with subcol1:
        st.markdown("**Website/Platform** <span class='required-asterisk'>*</span>", unsafe_allow_html=True)
        website = st.selectbox(
            "Website/Platform",
            options=[""] + website_options,  # Add empty option for validation
            key="website_select",
            help="This field is required",
            label_visibility="collapsed"
        )
        
        # Add validation styling
        website_validation_class = get_field_validation_class('website', website)
        if website_validation_class:
            st.markdown(f"""
            <script>
            setTimeout(function() {{
                const selects = document.querySelectorAll('div[data-testid="stSelectbox"] > div > div > div');
                selects.forEach(select => {{
                    if (select.textContent.includes('Website') || select.closest('div[data-testid="stSelectbox"]')) {{
                        select.classList.add('{website_validation_class}');
                    }}
                }});
            }}, 100);
            </script>
            """, unsafe_allow_html=True)
        
        # Show validation message
        show_field_validation_message('website', website)
    
    with subcol2:
        st.write("\n")
        if website:
            st.link_button("↗️", website)
    
    with subcol3:
        st.write("\n")
        if website and st.button("💡", help="Get Suggestion", key="suggestion_btn"):
            suggestions = {
                "https://www.amazon.com": "🛒 Try browsing Amazon's daily deals for great discounts!",
                "https://www.ebay.com": "🔍 Use eBay's advanced search filters to find exactly what you need!",
                "https://www.shopify.com": "🏪 Consider Shopify's free trial to start your online store!",
                "https://www.etsy.com": "🎨 Explore Etsy's handmade categories for unique finds!",
                "https://www.facebook.com/marketplace": "📍 Check local pickup options to save on shipping!"
            }
            st.success(suggestions.get(website, "💡 Great choice! Explore what this platform has to offer."))
    
    with subcol4:
        st.write("\n")
        if website and st.button("ℹ️", help="Company Info", key="info_btn"):
            st.session_state.show_info = True
            st.session_state.selected_website = website

    # Show popup if triggered
    if st.session_state.get('show_info', False):
        info = company_info.get(st.session_state.get('selected_website', ''), {})
        if info:
            with st.container():
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"### 📋 About {info.get('name', 'Company')}")
                    st.markdown(f"**Description:** {info.get('description', 'N/A')}")
                    st.markdown(f"**Founded:** {info.get('founded', 'N/A')}")
                    if 'founder' in info:
                        st.markdown(f"**Founder:** {info['founder']}")
                    if 'parent_company' in info:
                        st.markdown(f"**Parent Company:** {info['parent_company']}")
                    st.markdown(f"**Headquarters:** {info.get('headquarters', 'N/A')}")
                    st.markdown(f"**Services:** {info.get('services', 'N/A')}")
                    
                    if st.button("✖️ Close", key="close_info_popup"):
                        st.session_state.show_info = False
                        st.rerun()
                st.markdown("---")

# Image and colors section
if website:
    website_data = get_or_load_website_data(website)
    
    if website_data['loading']:
        with st.spinner("Loading website data..."):
            st.info("🔄 Fetching website logo and Org colors...")
    elif website_data['image'] and website_data['colors']:
        st.write("---")
        
        logo_colors_html = f"""
<div style="display: flex; align-items: center; gap: 20px; margin: 10px 0;">
    <img src="{website_data['image']}" style="height: 60px; width: auto; object-fit: contain;">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-weight: bold; margin-right: 10px;">Org Colors:</span>"""
        
        for i, color in enumerate(website_data['colors'][:3]):
            logo_colors_html += f"""
        <div style="text-align: center;">
            <div style="width: 40px; height: 40px; background-color: {color}; border: 2px solid #ddd; border-radius: 6px; margin-bottom: 3px;"></div>
            <p style="font-size: 10px; margin: 0;">{color}</p>
        </div>"""
        
        logo_colors_html += """
    </div>
</div>"""
        
        st.markdown(logo_colors_html, unsafe_allow_html=True)

st.divider()

# Create two columns for the layout
col1, col2 = st.columns([1, 1])

# Left column - File upload section
with col1:
    st.markdown("### 📄 Upload RFI Document <span class='required-asterisk'>*</span>", unsafe_allow_html=True)
    
    # File uploader with dynamic key
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    uploaded_file = st.file_uploader(
        "Choose your RFI document",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Required: Supported formats: PDF, DOCX, DOC, TXT",
        key=file_key,
        label_visibility="collapsed"
    )
    
    # Add validation styling for file uploader
    file_validation_class = get_field_validation_class('file_upload', uploaded_file)
    if file_validation_class:
        st.markdown(f"""
        <script>
        setTimeout(function() {{
            const fileUploaders = document.querySelectorAll('div[data-testid="stFileUploader"] > div');
            fileUploaders.forEach(uploader => {{
                uploader.classList.add('{file_validation_class}');
            }});
        }}, 100);
        </script>
        """, unsafe_allow_html=True)
    
    # Show validation message
    show_field_validation_message('file_upload', uploaded_file)
    
    # Display file information if uploaded
    if uploaded_file is not None:
        st.success("✅ Document uploaded successfully!")
        
        file_details = {
            "Filename": uploaded_file.name,
            "File Type": uploaded_file.type,
            "File Size": f"{uploaded_file.size} bytes"
        }
        
        with st.expander("📋 File Details"):
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
    
    else:
        st.info("👆 Please upload your RFI document to get started")

# Right column - Text details section
with col2:
    st.markdown("### ✏️ Document Details <span class='required-asterisk'>*</span>", unsafe_allow_html=True)
    
    # Text area for writing details
    document_details = st.text_area(
        "Write details about the RFI document:",
        placeholder="Enter document summary, key points, requirements, or any other relevant details...",
        height=300,
        help="Required: Provide detailed information about the RFI document",
        key="document_details",
        label_visibility="collapsed"
    )
    
    # Add validation styling for text area
    details_validation_class = get_field_validation_class('document_details', document_details)
    if details_validation_class:
        st.markdown(f"""
        <script>
        setTimeout(function() {{
            const textareas = document.querySelectorAll('textarea');
            textareas.forEach(textarea => {{
                textarea.classList.add('{details_validation_class}');
            }});
        }}, 100);
        </script>
        """, unsafe_allow_html=True)
    
    # Show validation message
    show_field_validation_message('document_details', document_details)

# Add validation button and status
st.divider()

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🔍 Validate Form", type="primary", use_container_width=True):
        st.session_state.show_validation = True
        if validate_required_fields():
            st.success("✅ All required fields are completed!")
            st.balloons()
        else:
            st.error("❌ Please complete all required fields marked with *")
            st.rerun()  # Rerun to show validation styling

# Manual reset button (optional)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🔄 Reset All Fields", type="secondary", use_container_width=True):
        # Reset all fields
        st.session_state.seller_name_input = ""
        st.session_state.website_select = ""
        st.session_state.document_details = ""
        
        # Reset file uploader by incrementing key
        st.session_state.file_uploader_key += 1
        
        # Reset previous values
        st.session_state.prev_seller_name = ""
        st.session_state.prev_website = ""
        st.session_state.prev_uploaded_file = None
        
        # Clear validation
        st.session_state.validation_errors = {}
        st.session_state.show_validation = False
        
        # Clear website data
        st.session_state.website_data = {}
        
        st.success("🔄 All fields have been reset!")
        st.rerun()

# Optional: Real-time validation indicator
if st.session_state.validation_errors:
    with st.sidebar:
        st.markdown("### ⚠️ Required Fields Missing:")
        for field, error in st.session_state.validation_errors.items():
            st.markdown(f"- {error}")
else:
    # Show completion status in sidebar
    seller_filled = bool(st.session_state.get('seller_name_input', '').strip())
    website_filled = bool(st.session_state.get('website_select'))
    file_key = f"uploaded_file_{st.session_state.file_uploader_key}"
    file_filled = st.session_state.get(file_key) is not None
    details_filled = bool(st.session_state.get('document_details', '').strip())
    
    if any([seller_filled, website_filled, file_filled, details_filled]):
        with st.sidebar:
            st.markdown("### 📋 Form Progress:")
            st.markdown(f"{'✅' if seller_filled else '❌'} Seller Name")
            st.markdown(f"{'✅' if website_filled else '❌'} Website/Platform")
            st.markdown(f"{'✅' if file_filled else '❌'} RFI Document")
            st.markdown(f"{'✅' if details_filled else '❌'} Document Details")
            
            progress = sum([seller_filled, website_filled, file_filled, details_filled]) / 4
            st.progress(progress, text=f"Completed: {int(progress * 100)}%")

# Show cascade reset info in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔄 Cascade Reset Info")
    st.markdown("**How it works:**")
    st.markdown("- Changing **Seller Name** resets everything below")
    st.markdown("- Changing **Website** resets file upload & details")
    st.markdown("- Changing **File Upload** resets document details")
    st.markdown("- This ensures data consistency in your form")