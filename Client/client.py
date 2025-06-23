



import streamlit as st
import pandas as pd
import os
from typing import List
from .client_utils import *
import threading
import time
from Search.Linkedin.linkedin_serp import *
from Recommendation.recommendation_utils import *
from .client_css import client_css



# Apply CSS only once at the beginning with a unique key to prevent duplication
if 'css_applied' not in st.session_state:
    st.session_state.css_applied = True
    st.markdown(client_css, unsafe_allow_html=True)

# Function to save uploaded file and return the file path
def save_uploaded_file_and_get_path(uploaded_file):
    """Save uploaded file to a temporary directory and return the file path"""
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        upload_dir = os.getenv("FILE_SAVE_PATH")
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
        st.session_state.client_requirements_content = ""
    
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
    
    # Initialize scraping states
    if 'scraping_in_progress' not in st.session_state:
        st.session_state['scraping_in_progress'] = False
    if 'pending_scrape_url' not in st.session_state:
        st.session_state['pending_scrape_url'] = None

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
        name_col, button_col = st.columns([3, 1])
        
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
            
            if st.button("🔍 Find Website",
                        disabled=find_urls_disabled,
                        help="Find website URLs for this company",
                        key="find_urls_button"):
                # Add spinner while fetching URLs
                with st.spinner(f"Finding Websites for '{client_enterprise_name.strip()}'..."):
                    try:
                        st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name.strip())
                        st.session_state['last_company_name'] = client_enterprise_name
                    except Exception as e:
                        st.session_state['client_website_urls_list'] = []
                        st.error(f"Error finding URLs: {str(e)}")
        
        # Clear URLs if company name is cleared
        if not client_enterprise_name and st.session_state['last_company_name']:
            st.session_state['client_website_urls_list'] = []
            st.session_state['last_company_name'] = ""
        
        # Show validation warning if triggered and field is empty
        if st.session_state.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")
    
    with col2:
        # Label row with inline emoji and tooltip
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Client Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the client's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create columns for dropdown and buttons - dropdown takes most space, buttons share remaining space
        url_col, btn1_col, btn2_col, btn3_col = st.columns([7, 1, 1, 1])
        
        with url_col:
            # URL selection logic - Always show normal dropdown, just disable when no client name
            client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
            
            if not st.session_state.get('client_website_urls_list'):
                # No URLs available - show default option
                url_options = ["Select client website URL"]
            else:
                # URLs available - show them in dropdown
                url_options = ["Select client website URL"] + st.session_state['client_website_urls_list']
            
            client_website_url = st.selectbox(
                label="Client Website URL",
                options=url_options,
                key="client_website_url_selector",
                label_visibility="collapsed",
                disabled=not client_name_provided,
                accept_new_options=True
            )
            
            # Reset to empty string if default option is selected
            if client_website_url == "Select client website URL":
                client_website_url = ""
        
        # Each button in its own column for horizontal alignment
        with btn1_col:
            if client_website_url:
                st.link_button("🌐", client_website_url, help="Visit website")
            else:
                st.button("🌐", help="Visit website", disabled=True)
        with btn2_col:
            # Button 2: Refresh URL List
            refresh_clicked = st.button("🔄", help="Refresh website URLs list", key="refresh_urls_btn")
        
        with btn3_col:
            # Button 3: Scrape Website - Set up pending scrape instead of immediate execution
            scrape_clicked = st.button("📑", help="Get enterprise details", key="scrape_website_btn", disabled=not client_website_url)
            
            # Handle scrape button click by setting up pending operation
            if scrape_clicked and client_website_url:
                st.session_state['pending_scrape_url'] = client_website_url
                st.session_state['scraping_in_progress'] = True
                st.rerun()

        # Handle refresh action outside columns for better UX
        if refresh_clicked and client_name_provided:
            try:
                with st.spinner("Refreshing website URLs..."):
                    st.session_state['client_website_urls_list'] = get_urls_list(client_enterprise_name)
                    st.success("Website URLs refreshed!")
                    st.rerun()  # Refresh the page to show updated URLs
            except Exception as e:
                st.error(f"Error refreshing URLs: {str(e)}")

        # Handle pending scraping operation OUTSIDE of columns to prevent UI blocking
        if st.session_state.get('scraping_in_progress') and st.session_state.get('pending_scrape_url'):
            # Show full-width spinner
            with st.spinner(f"Scraping website details from {st.session_state['pending_scrape_url']}..."):
                try:
                    # Perform the scraping operation
                    website_details = get_url_details(st.session_state['pending_scrape_url'])
                    st.session_state.enterprise_details_content = website_details
                    st.session_state['last_analyzed_url'] = st.session_state['pending_scrape_url']
                    
                    # Clear pending operation
                    st.session_state['scraping_in_progress'] = False
                    st.session_state['pending_scrape_url'] = None
                    
                    st.success("Website details extracted successfully!")
                    st.rerun()  # Refresh to show updated details
                    
                except Exception as e:
                    # Clear pending operation on error
                    st.session_state['scraping_in_progress'] = False
                    st.session_state['pending_scrape_url'] = None
                    st.error(f"Error scraping website: {str(e)}")

    # Show validation warning if triggered and field is empty (optional)
    if st.session_state.show_validation and check_field_validation("Client Website URL", client_website_url, False):
        show_field_warning("Client Website URL")
    
    # Continue with col3 and col4 - these will now render properly without being blocked
    col3, col4 = st.columns([1, 1])
            
    with col3:
        st.markdown('''
        <div class="tooltip-label">
            Upload RFI Document
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add custom CSS for file uploader and animations
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
        
        /* Animation for processing file */
        .processing-file {
            animation: pulse 1.5s ease-in-out infinite;
            background: linear-gradient(90deg, #e3f2fd, #bbdefb, #e3f2fd);
            background-size: 200% 100%;
            animation: shimmer 2s linear infinite;
            border-radius: 4px;
            padding: 2px 4px;
        }
        
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .analyzing-text {
            color: #1976d2;
            font-weight: 500;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # FILE UPLOAD - Always enabled, independent of client name
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
            
            # Initialize processing state if not exists
            if 'processing_rfi' not in st.session_state:
                st.session_state['processing_rfi'] = False
            
            # Check if currently processing
            is_processing = st.session_state.get('processing_rfi', False)
            
            # Single compact row
            col_info, col_btn = st.columns([2.5, 1])
            
            with col_info:
                if is_processing:
                    # Show animated processing state
                    st.markdown(f"""
                    <div class="processing-file">
                        <span style='font-size:0.8em' class="analyzing-text">
                            🔄 {rfi_document_upload.name[:20]}{'...' if len(rfi_document_upload.name) > 20 else ''} (Analyzing...)
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Show normal file info
                    st.markdown(f"<span style='font-size:0.8em'>📄 {rfi_document_upload.name[:25]}{'...' if len(rfi_document_upload.name) > 25 else ''} ({file_size_display})</span>", 
                            unsafe_allow_html=True)
            
            with col_btn:
                # Disable button while processing
                # Different colors for different states
                button_color = "#FF6B6B" if is_processing else "#4CAF50"

                st.markdown(f"""
                <style>
                div.stButton > button:first-child {{
                    background-color: {button_color};
                    color: white;
                    border: none;
                }}
                </style>
                """, unsafe_allow_html=True)



                # Your button code
                analyze_clicked = st.button(
                    "Analyzing..." if is_processing else "Get pain points",
                    key="analyze_rfi_document_btn",
                    help="Process RFI document" if not is_processing else "Processing in progress...",
                    type="secondary" ,
                    disabled=is_processing,
                    use_container_width=True
                )
            
            # Handle analyze button click
            if analyze_clicked and not is_processing:
                if not client_enterprise_name:
                    st.error("❌ Please enter the Client Enterprise Name first")
                else:
                    # Set processing flag
                    st.session_state['processing_rfi'] = True
                    st.rerun()  # Refresh to show processing state
            
            # Show processing indicator with spinner
            if st.session_state.get('processing_rfi', False):
                # Show spinner in a container
                with st.container():
                    col_spinner, col_text = st.columns([0.5, 4])
                    with col_spinner:
                        with st.spinner(''):
                            pass
                    with col_text:
                        st.markdown("**🔍 Analyzing RFI document and extracting key insights...**")
                
                # Perform the actual processing
                try:
                    # Save the file and get the path
                    file_path = save_uploaded_file_and_get_path(rfi_document_upload)
                    st.session_state['uploaded_file_path'] = file_path
                    
                    if file_path and client_enterprise_name:
                        # Extract pain points using the file path and company name
                        st.session_state.pain_point = get_pain_points(file_path, client_enterprise_name)
                        # Automatically generate RFI pain points items
                        pain_points_data = st.session_state.pain_point
                        st.session_state['rfi_pain_points_items'] = pain_points_data
                        st.session_state['document_analyzed'] = True
                        st.session_state['processing_rfi'] = False  # Reset processing flag
                        
                        # Show success message briefly
                        st.success("✅ RFI document analyzed successfully!")
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
        
        # Initialize selected pain points in session state if not exists
        if 'selected_pain_points' not in st.session_state:
            st.session_state['selected_pain_points'] = set()
        
        # Get RFI pain points items from session state or use dummy data
        if client_name_provided and st.session_state.get('rfi_pain_points_items'):
            rfi_pain_points_items = st.session_state['rfi_pain_points_items']
        else:
            # Dummy data when no client name or no file uploaded
            rfi_pain_points_items = {
               
                "Revenue Challenges": "**Revenue Challenges** • Sales declined by 15% year-over-year despite market growth\n• Missed quarterly revenue targets by $2.3M for three consecutive quarters\n• Average deal size decreased by 22% due to increased price competition\n• Customer churn rate increased to 18%, up from 12% previous year\n• Revenue per customer dropped 8% as clients downgraded service tiers\n• New product launches generated only 60% of projected revenue\n• Seasonal revenue fluctuations creating 40% variance between peak and low periods\n• Pipeline conversion rates fell from 35% to 24% over past 12 months\n\n",
                
                "Cost and Margin Pressure": "**Cost and Margin Pressure** • Cost of Goods Sold increased by 12% due to supply chain disruptions\n• Labor costs rose 18% while productivity remained flat\n• Raw material prices up 25% with limited ability to pass costs to customers\n• Operational efficiency decreased by 14% due to outdated processes\n• Procurement costs increased 20% from supplier consolidation issues\n• Technology infrastructure costs grew 30% without proportional business benefits\n• Regulatory compliance expenses added $1.8M in unexpected annual costs\n• Facility and overhead costs up 16% while revenue remained stagnant\n\n",
                
                "Market Expansion and Customer Acquisition": "**Market Expansion and Customer Acquisition**\n\n • Win rate on new business opportunities dropped from 42% to 28%\n• Customer acquisition cost increased 35% while customer lifetime value declined\n• Expansion into new geographic markets yielding only 40% of projected results\n• Lack of local market knowledge resulting in 60% longer sales cycles\n• Digital marketing campaigns generating 50% fewer qualified leads\n• Competition from new market entrants capturing 25% of target customer segment\n• Limited brand recognition in new markets requiring 3x marketing investment\n• Difficulty penetrating enterprise accounts with average sales cycle extending to 18 months\n\n"

            }
        # Initialize content mapping in session state if not exists
        if 'pain_point_content_map' not in st.session_state:
            st.session_state['pain_point_content_map'] = {}

        # Use a single container for all pain points items
        with st.container():
            # Display pain points items with add/remove buttons
            for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                # Check if this item is selected
                is_selected = key in st.session_state['selected_pain_points']
                
                # Create a box container with +/- button and content on same horizontal level
                col_add, col_content = st.columns([0.5, 9], gap="small")
                
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
                    
                    # Change button appearance based on selection state
                    button_text = "❌" if is_selected else "➕"
                    button_help = f"Remove '{key}' from client requirements" if is_selected else f"Add '{key}' to client requirements section"
                    button_type = "secondary" 
                    
                    if st.button(button_text, 
                            key=f"toggle_rfi_pain_point_item_{i}", 
                            help=button_help,
                            type=button_type,
                            disabled=not client_name_provided):
                        
                        if is_selected:
                            # REMOVE FUNCTIONALITY
                            # Get current content from the session state
                            current_content = st.session_state.get('client_requirements_content', '')
                            
                            # Get the original content that was added for this key
                            original_content = st.session_state['pain_point_content_map'].get(key, value)
                            
                            # Remove this specific pain point section from content
                            # Try multiple removal patterns to be more robust
                            patterns_to_remove = [
                                f"\n\n{original_content}",
                                f"{original_content}\n\n",
                                original_content
                            ]
                            
                            updated_content = current_content
                            for pattern in patterns_to_remove:
                                updated_content = updated_content.replace(pattern, "")
                            
                            # Clean up any excessive newlines
                            updated_content = '\n\n'.join([section.strip() for section in updated_content.split('\n\n') if section.strip()])
                            
                            # Update the session state content variable
                            st.session_state.client_requirements_content = updated_content
                            
                            # Remove from selected items and content map
                            st.session_state['selected_pain_points'].discard(key)
                            if key in st.session_state['pain_point_content_map']:
                                del st.session_state['pain_point_content_map'][key]
                            
                            # Show removal message
                           # st.success(f"🗑️ '{key}' removed from Client Requirements!")
                            
                        else:
                            # ADD FUNCTIONALITY
                            # Get current content from the session state
                            current_content = st.session_state.get('client_requirements_content', '')
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update the session state content variable
                            st.session_state.client_requirements_content = new_content
                            
                            # Store the content in mapping for future removal
                            st.session_state['pain_point_content_map'][key] = value
                            
                            # Mark this item as selected
                            st.session_state['selected_pain_points'].add(key)
                            
                            # Show success message
                            #st.success(f"✅ '{key}' added to Client Requirements!")
                        
                        st.rerun()

                with col_content:
                    # [Same styling code as before]
                    if is_selected:
                        background_color = "#2e7d32"
                        border_color = "#4caf50"
                        text_color = "#ffffff"
                        icon = "✅"
                        box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                    else:
                        background_color = "#404040"
                        border_color = "#404040"
                        text_color = "#ffffff"
                        icon = "📋"
                        box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
                    
                    st.markdown(f"""
                    <div style="
                        padding: 12px;
                        border-radius: 6px;
                        margin: 5px 0;
                        background-color: {background_color};
                        border: 2px solid {border_color};
                        color: {text_color};
                        font-weight: 500;
                        box-shadow: {box_shadow};
                        min-height: 24px;
                        display: flex;
                        align-items: center;
                        transition: all 0.3s ease;
                    ">
                        {icon} {key}
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
                disabled=not spoc_name_provided,
                accept_new_options=True,
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
                disabled=True,
                accept_new_options=True
            )
            spoc_linkedin_profile = None
        else:
            # Default disabled state
            spoc_linkedin_profile = st.selectbox(
                label="SPOC LinkedIn Profile",
                options=["Enter SPOC name to get LinkedIn profiles"],
                key="spoc_linkedin_profile_selector",
                label_visibility="collapsed",
                disabled=not spoc_name_provided,
                accept_new_options=True
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
# Existing row with roles and priorities
    col7, col8 = st.columns([1, 1])

    with col7:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Role 
            <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)

        # Initialize session state for roles if not exists
        if 'selected_target_roles' not in st.session_state:
            st.session_state['selected_target_roles'] = []

        # Prepare role options for dropdown based on LinkedIn profile selection
        role_options = ["Select a role..."]
        
        # Get default roles from function
        target_roles_list = get_roles_list() or []
        
        # Check if a LinkedIn profile is selected
        selected_linkedin_role = None
        if (spoc_name_provided and 
            st.session_state.get('linkedin_profiles') and 
            'spoc_linkedin_profile' in locals() and 
            spoc_linkedin_profile):
            
            # Get the selected LinkedIn profile data
            selected_profile_data = st.session_state['linkedin_profiles'].get(spoc_linkedin_profile)
            if selected_profile_data:
                selected_linkedin_role = selected_profile_data.get('role')
                if selected_linkedin_role:
                    # Show LinkedIn profile role + default roles from get_roles_list()
                    role_options = ["Select a role...", selected_linkedin_role]
                    # Add default roles, avoiding duplicates
                    for role in target_roles_list:
                        if role not in role_options:
                            role_options.append(role)
        
        # If no LinkedIn profile selected, show all available roles
        if not selected_linkedin_role:
            # Add standard roles from get_roles_list()
            role_options.extend(target_roles_list)
            
            # Add LinkedIn roles if available (but no specific profile selected)
            if spoc_name_provided and st.session_state.get('linkedin_profiles'):
                for url, profile_data in st.session_state['linkedin_profiles'].items():
                    linkedin_role = profile_data.get('role')
                    if linkedin_role and linkedin_role not in role_options:
                        role_options.append(linkedin_role)

        # Determine the default/current value for the selectbox
        current_selection = "Select a role..."
        if selected_linkedin_role and selected_linkedin_role in role_options:
            # Auto-select the LinkedIn role
            current_selection = selected_linkedin_role
        elif "target_role_selector_dropdown" in st.session_state:
            # Keep the current selection if it exists in options
            current_value = st.session_state["target_role_selector_dropdown"]
            if current_value in role_options:
                current_selection = current_value

        # ROLES DROPDOWN
        new_target_role = st.selectbox(
            label="Target Role Selector", 
            options=role_options,
            index=role_options.index(current_selection) if current_selection in role_options else 0,
            key="target_role_selector_dropdown",
            label_visibility="collapsed",
            disabled=not (client_name_provided and spoc_name_provided),
            accept_new_options=True
        )
    with col8:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Business priorities
            <div class="tooltip-icon" data-tooltip="Select Business priorities of the SPOC.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get business priorities based on selected LinkedIn roles or use defaults
        if spoc_name_provided and 'selected_target_roles' in st.session_state and st.session_state['selected_target_roles']:
            try:
                # Get priorities for the selected LinkedIn roles only
                business_priorities_list = []
                for role in st.session_state['selected_target_roles']:
                    role_priorities = get_ai_business_priorities(role)
                    if role_priorities:
                        business_priorities_list.extend(role_priorities)
                
                # Remove duplicates while preserving order
                seen = set()
                unique_priorities = []
                for priority in business_priorities_list:
                    # Handle both string and dict formats for duplicate checking
                    if isinstance(priority, dict):
                        priority_title = priority.get('title', str(priority))
                    else:
                        priority_title = str(priority)
                    
                    if priority_title not in seen:
                        seen.add(priority_title)
                        unique_priorities.append(priority)
                
                business_priorities_list = unique_priorities
                
                # If no priorities found for selected roles, use defaults
                if not business_priorities_list:
                    raise ValueError("No priorities found for selected roles")
                    
            except Exception as e:
                # Handle any errors by showing default priorities
                st.warning("Unable to load role-specific priorities. Showing default options.")
                business_priorities_list = [
                    {'title': 'Revenue Growth and Market Share Expansion', 'icon': '📈'}, 
                    {'title': 'Profitability and Cost Optimization', 'icon': '💰'}, 
                    {'title': 'Digital Transformation and Innovation', 'icon': '🤖'}
                ]
        else:
            # Default priorities when no SPOC name or no selected roles
            business_priorities_list = [
                {'title': 'Revenue Growth and Market Share Expansion', 'icon': '📈'}, 
                {'title': 'Profitability and Cost Optimization', 'icon': '💰'}, 
                {'title': 'Digital Transformation and Innovation', 'icon': '🤖'}
            ]
        
        # Initialize session state for selected priorities
        if 'selected_business_priorities' not in st.session_state:
            st.session_state['selected_business_priorities'] = []
        
        # Generate checkboxes dynamically from function
        for i, priority in enumerate(business_priorities_list):
            business_priority_checkbox_key = f"business_priority_checkbox_{i}"
            
            # Handle both string and dict formats
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
            
            # Check if this priority should be pre-selected
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
    #col9, col10= st.columns([1, 1])
    
    # with col9:
    #     st.markdown('''
    #     <div class="tooltip-label">
    #         Additional Client Requirements
    #         <div class="tooltip-icon" data-tooltip="Document any additional specific requirements, constraints, expectations, compliance requirements, budget limitations, timeline constraints, or special considerations mentioned by the client that are not covered in the main requirements section.">ⓘ</div>
    #     </div>
    #     ''', unsafe_allow_html=True)
        
    #     # TEXT AREA - DISABLED if no client name
    #     client_additional_requirements = st.text_area(
    #         label="Additional Client Requirements", 
    #         placeholder="Enter client name first to enable this field" if not client_name_provided else "Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...", 
    #         height=200, 
    #         key="client_additional_requirements_textarea",
    #         label_visibility="collapsed",
    #         disabled=not client_name_provided
    #     )
    
    
    # with col10:
    #     st.markdown('''
    #     <div class="tooltip-label">
    #          Additional Specifications to be considered
    #         <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
    #     </div>
    #     ''', unsafe_allow_html=True)
        
    #     # Get AI suggestion 1 from function

    #     # Use a stable key based on client name + requirements hash
    #     requirement_key = f"{client_enterprise_name.strip()}__{hash(client_requirements.strip())}"

    #     if client_name_provided and client_requirements_provided:
    #         # Only run the AI call if not already cached
    #         if 'rfi_additional_specs_cache' not in st.session_state:
    #             st.session_state['rfi_additional_specs_cache'] = {}

    #         if requirement_key in st.session_state['rfi_additional_specs_cache']:
    #             rfi_additional_specs_content = st.session_state['rfi_additional_specs_cache'][requirement_key]
    #         else:
    #             rfi_additional_specs_content = get_ai_client_requirements(
    #                 client_requirements=client_requirements,
    #                 enterprise_details=enterprise_details
    #             )
    #             st.session_state['rfi_additional_specs_cache'][requirement_key] = rfi_additional_specs_content
    #     else:
    #         rfi_additional_specs_content = 'Enter additional client requirements and specifications if any'

        
    #     # TEXT AREA - DISABLED if no client name
    #     rfi_additional_specs = st.text_area(
    #         label="Additional Specifications", 
    #         value=rfi_additional_specs_content, 
    #         height=200, 
    #         key="rfi_additional_specs_textarea",
    #         label_visibility="collapsed",
    #         disabled=not client_requirements_provided,
    #         placeholder="Enter client name first to enable this field" if not client_name_provided else ""
    #     )
    col9, col10 = st.columns([1, 1])

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
            value=st.session_state.get('client_additional_requirements_content', '') if client_name_provided else "",
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...",
            height=200,
            key="client_additional_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Update the session state when the text area changes (only if enabled)
        if client_name_provided:
            st.session_state.client_additional_requirements_content = client_additional_requirements
        client_additional_requirements_provided = bool(client_name_provided and client_additional_requirements.strip())

    with col10:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Additional Specifications to be considered
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Initialize selected additional specs in session state if not exists
        if 'selected_additional_specs' not in st.session_state:
            st.session_state['selected_additional_specs'] = set()
        
        # Get additional specs items from session state or use dummy data
        if client_name_provided and st.session_state.get('additional_specs_items'):
            additional_specs_items = st.session_state['additional_specs_items']
        else:
            # Dummy data when no client name or no specific data
            additional_specs_items = {
                "Technical Infrastructure Requirements": "**Technical Infrastructure Requirements**\n• Cloud hosting with 99.9% uptime SLA and auto-scaling capabilities\n• Multi-region deployment for disaster recovery and performance optimization\n• Integration with existing ERP, CRM, and financial management systems\n• API-first architecture with RESTful services and webhook support\n• Database performance optimization with sub-second query response times\n• Security compliance with SOC2, ISO 27001, and industry-specific regulations\n• Load balancing and CDN implementation for global content delivery\n• Automated backup and recovery systems with point-in-time restoration\n\n",
                
                "Compliance and Security Standards": "**Compliance and Security Standards**\n• GDPR, CCPA, and regional data privacy regulation compliance\n• End-to-end encryption for data in transit and at rest\n• Multi-factor authentication and role-based access controls\n• Regular security audits and penetration testing protocols\n• Data retention and deletion policies per regulatory requirements\n• Audit trail logging for all system interactions and data changes\n• Incident response plan with 4-hour notification requirements\n• Employee background checks and security clearance verification\n\n",
                
                "Performance and Scalability Metrics": "**Performance and Scalability Metrics**\n• System response time under 2 seconds for 95% of user interactions\n• Concurrent user capacity of 10,000+ with linear scaling capability\n• Database query optimization with indexing and caching strategies\n• Mobile application performance with offline synchronization\n• Bandwidth optimization for low-connectivity environments\n• Real-time analytics and reporting with sub-minute data refresh\n• Automated performance monitoring with threshold-based alerting\n• Capacity planning with predictive scaling based on usage patterns\n\n"
            }
        
        # Initialize content mapping in session state if not exists
        if 'additional_specs_content_map' not in st.session_state:
            st.session_state['additional_specs_content_map'] = {}

        # Use a single container for all additional specs items
        with st.container():
            # Display additional specs items with add/remove buttons
            for i, (key, value) in enumerate(additional_specs_items.items()):
                # Check if this item is selected
                is_selected = key in st.session_state['selected_additional_specs']
                
                # Create a box container with +/- button and content on same horizontal level
                col_add, col_content = st.columns([0.5, 9], gap="small")
                
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
                    
                    # Change button appearance based on selection state
                    button_text = "❌" if is_selected else "➕"
                    button_help = f"Remove '{key}' from additional requirements" if is_selected else f"Add '{key}' to additional requirements section"
                    button_type = "secondary" 
                    
                    if st.button(button_text, 
                            key=f"toggle_additional_spec_item_{i}", 
                            help=button_help,
                            type=button_type,
                            disabled=not client_name_provided):
                        
                        if is_selected:
                            # REMOVE FUNCTIONALITY
                            # Get current content from the session state
                            current_content = st.session_state.get('client_additional_requirements_content', '')
                            
                            # Get the original content that was added for this key
                            original_content = st.session_state['additional_specs_content_map'].get(key, value)
                            
                            # Remove this specific additional spec section from content
                            # Try multiple removal patterns to be more robust
                            patterns_to_remove = [
                                f"\n\n{original_content}",
                                f"{original_content}\n\n",
                                original_content
                            ]
                            
                            updated_content = current_content
                            for pattern in patterns_to_remove:
                                updated_content = updated_content.replace(pattern, "")
                            
                            # Clean up any excessive newlines
                            updated_content = '\n\n'.join([section.strip() for section in updated_content.split('\n\n') if section.strip()])
                            
                            # Update the session state content variable
                            st.session_state.client_additional_requirements_content = updated_content
                            
                            # Remove from selected items and content map
                            st.session_state['selected_additional_specs'].discard(key)
                            if key in st.session_state['additional_specs_content_map']:
                                del st.session_state['additional_specs_content_map'][key]
                            
                        else:
                            # ADD FUNCTIONALITY
                            # Get current content from the session state
                            current_content = st.session_state.get('client_additional_requirements_content', '')
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update the session state content variable
                            st.session_state.client_additional_requirements_content = new_content
                            
                            # Store the content in mapping for future removal
                            st.session_state['additional_specs_content_map'][key] = value
                            
                            # Mark this item as selected
                            st.session_state['selected_additional_specs'].add(key)
                        
                        st.rerun()

                with col_content:
                    # Style the content box based on selection state
                    if is_selected:
                        background_color = "#2e7d32"
                        border_color = "#4caf50"
                        text_color = "#ffffff"
                        icon = "✅"
                        box_shadow = "0 2px 8px rgba(76, 175, 80, 0.3)"
                    else:
                        background_color = "#404040"
                        border_color = "#404040"
                        text_color = "#ffffff"
                        icon = "📋"
                        box_shadow = "0 2px 4px rgba(0,0,0,0.1)"
                    
                    st.markdown(f"""
                    <div style="
                        padding: 12px;
                        border-radius: 6px;
                        margin: 5px 0;
                        background-color: {background_color};
                        border: 2px solid {border_color};
                        color: {text_color};
                        font-weight: 500;
                        box-shadow: {box_shadow};
                        min-height: 24px;
                        display: flex;
                        align-items: center;
                        transition: all 0.3s ease;
                    ">
                        {icon} {key}
                    </div>
                    """, unsafe_allow_html=True)
    # Handle validation trigger from main app
    if 'trigger_validation' in st.session_state and st.session_state.trigger_validation:
        st.session_state.show_validation = True
        st.session_state.trigger_validation = False