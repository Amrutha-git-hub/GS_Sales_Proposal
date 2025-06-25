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
from .client_dataclass import ClientData, ClientDataManager


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


def validate_client_mandatory_fields():
    """Validate client mandatory fields using dataclass"""
    client_data = ClientDataManager.get_client_data()
    return True
    return client_data.validate_mandatory_fields()


def client_tab(st):
    # Get client data from dataclass manager
    client_data = ClientDataManager.get_client_data()
    
    # Apply CSS only once
    if not client_data.css_applied:
        st.markdown(client_css, unsafe_allow_html=True)
        ClientDataManager.update_client_data(css_applied=True)
    
    # Re-apply CSS after every rerun to ensure persistence
    st.markdown(client_css, unsafe_allow_html=True)
    
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
                value=client_data.enterprise_name,
                placeholder="Enter client enterprise name...", 
                key="client_enterprise_name_input",
                label_visibility="collapsed",
                
            )
            # Update dataclass when input changes
            if client_enterprise_name != client_data.enterprise_name:
                ClientDataManager.update_client_data(enterprise_name=client_enterprise_name)
        
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
                        urls_list = get_urls_list(client_enterprise_name.strip())
                        ClientDataManager.update_client_data(
                            website_urls_list=urls_list,
                            enterprise_name=client_enterprise_name  # Update last company name
                        )
                    except Exception as e:
                        ClientDataManager.update_client_data(website_urls_list=[])
                        st.error(f"Error finding URLs: {str(e)}")
        
        # Clear URLs if company name is cleared
        if not client_enterprise_name and client_data.enterprise_name:
            ClientDataManager.update_client_data(
                website_urls_list=[],
                enterprise_name=""
            )
        
        # Show validation warning if triggered and field is empty
        if client_data.show_validation and check_field_validation("Client Enterprise Name", client_enterprise_name, True):
            show_field_warning("Client Enterprise Name")
    
    with col2:
        # Label row with inline emoji and tooltip
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Client Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the client's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create columns for dropdown and buttons
        url_col, btn1_col, btn2_col, btn3_col = st.columns([7, 1, 1, 1])
        
        with url_col:
            # URL selection logic
            client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
            
            if not client_data.website_urls_list:
                url_options = ["Select client website URL"]
            else:
                url_options = ["Select client website URL"] + client_data.website_urls_list
            
            # Set default selection
            default_index = 0
            if client_data.website_url and client_data.website_url in url_options:
                default_index = url_options.index(client_data.website_url)
            
            client_website_url = st.selectbox(
                label="Client Website URL",
                options=url_options,
                index=default_index,
                key="client_website_url_selector",
                label_visibility="collapsed",
                disabled=not client_name_provided,
                accept_new_options=True
            )
            
            # Reset to empty string if default option is selected
            if client_website_url == "Select client website URL":
                client_website_url = ""
            
            # Update dataclass when URL changes
            if client_website_url != client_data.website_url:
                ClientDataManager.update_client_data(website_url=client_website_url)
        
        # Buttons for website actions
        with btn1_col:
            if client_website_url:
                st.link_button("🌐", client_website_url, help="Visit website", use_container_width=True)
            else:
                st.button("🌐", help="Visit website", disabled=True, use_container_width=True)
        
        with btn2_col:
            refresh_clicked = st.button("🔄", help="Refresh website URLs list", key="refresh_urls_btn", 
                                      use_container_width=True, disabled=not client_website_url)
        
        with btn3_col:
            scrape_clicked = st.button("📑", help="Get enterprise details", key="scrape_website_btn", 
                                      use_container_width=True, disabled=not client_website_url)
            
            if scrape_clicked and client_website_url:
                ClientDataManager.update_client_data(
                    pending_scrape_url=client_website_url,
                    scraping_in_progress=True
                )
                st.rerun()

        # Handle refresh action
        if refresh_clicked and client_name_provided:
            try:
                with st.spinner("Refreshing website URLs..."):
                    urls_list = get_urls_list(client_enterprise_name)
                    ClientDataManager.update_client_data(website_urls_list=urls_list)
                    st.success("Website URLs refreshed!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error refreshing URLs: {str(e)}")

        # Handle pending scraping operation
        if client_data.scraping_in_progress and client_data.pending_scrape_url:
            with st.spinner(f"Scraping website details from {client_data.pending_scrape_url}..."):
                try:
                    website_details = get_url_details(client_data.pending_scrape_url)
                    ClientDataManager.update_client_data(
                        enterprise_details_content=website_details,
                        last_analyzed_url=client_data.pending_scrape_url,
                        scraping_in_progress=False,
                        pending_scrape_url=None
                    )
                    st.success("Website details extracted successfully!")
                    st.rerun()
                except Exception as e:
                    ClientDataManager.update_client_data(
                        scraping_in_progress=False,
                        pending_scrape_url=None
                    )
                    st.error(f"Error scraping website: {str(e)}")

    # Show validation warning for URL field
    if client_data.show_validation and check_field_validation("Client Website URL", client_website_url, False):
        show_field_warning("Client Website URL")
    
    # File upload and enterprise details section
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown('''
        <div class="tooltip-label">
            Upload RFI Document
            <div class="tooltip-icon" data-tooltip="Upload the Request for Information (RFI) document in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key pain points, requirements, and business objectives to help tailor your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add custom CSS for file uploader
        st.markdown("""
        <style>
        .stFileUploader > div > div > div {
            padding: 0.5rem !important;
            min-height: 2rem !important;
        }
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
        
        # FILE UPLOAD
        rfi_document_upload = st.file_uploader(
            label="Upload RFI Document", 
            type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
            key="rfi_document_uploader",
            label_visibility="collapsed"
        )
        
        # Show file info and analyze button
        if rfi_document_upload is not None:
            file_size_kb = round(rfi_document_upload.size / 1024, 1)
            file_size_display = f"{file_size_kb}KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)}MB"
            
            # Single compact row
            col_info, col_btn = st.columns([2.5, 1])
            
            with col_info:
                if client_data.processing_rfi:
                    st.markdown(f"""
                    <div class="processing-file">
                        <span style='font-size:0.8em' class="analyzing-text">
                            🔄 {rfi_document_upload.name[:20]}{'...' if len(rfi_document_upload.name) > 20 else ''} (Analyzing...)
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='font-size:0.8em'>📄 {rfi_document_upload.name[:25]}{'...' if len(rfi_document_upload.name) > 25 else ''} ({file_size_display})</span>", 
                               unsafe_allow_html=True)
            
            with col_btn:
                button_color = "#FF6B6B" if client_data.processing_rfi else "#4CAF50"
                st.markdown(f"""
                <style>
                div.stButton > button:first-child {{
                    background-color: {button_color};
                    color: white;
                    border: none;
                }}
                </style>
                """, unsafe_allow_html=True)

                analyze_clicked = st.button(
                    "Analyzing..." if client_data.processing_rfi else "Get pain points",
                    key="analyze_rfi_document_btn",
                    help="Process RFI document" if not client_data.processing_rfi else "Processing in progress...",
                    type="secondary",
                    disabled=client_data.processing_rfi,
                    use_container_width=True
                )
            
            # Handle analyze button click
            if analyze_clicked and not client_data.processing_rfi:
                if not client_enterprise_name:
                    st.error("❌ Please enter the Client Enterprise Name first")
                else:
                    ClientDataManager.update_client_data(processing_rfi=True)
                    st.rerun()
            
            # Show processing indicator
            if client_data.processing_rfi:
                with st.container():
                    col_spinner, col_text = st.columns([0.5, 4])
                    with col_spinner:
                        with st.spinner(''):
                            pass
                    with col_text:
                        st.markdown("**🔍 Analyzing RFI document and extracting key insights...**")
                
                # Perform the actual processing
                try:
                    file_path = save_uploaded_file_and_get_path(rfi_document_upload)
                    if file_path and client_enterprise_name:
                        pain_points_data = get_pain_points(file_path, client_enterprise_name)
                        ClientDataManager.update_client_data(
                            uploaded_file_path=file_path,
                            rfi_pain_points_items=pain_points_data,
                            document_analyzed=True,
                            processing_rfi=False
                        )
                        st.success("✅ RFI document analyzed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Error saving the uploaded file")
                        ClientDataManager.update_client_data(processing_rfi=False)
                except Exception as e:
                    st.error(f"❌ Error analyzing RFI document: {str(e)}")
                    ClientDataManager.update_client_data(
                        rfi_pain_points_items={},
                        document_analyzed=False,
                        processing_rfi=False
                    )

    with col4:
        st.markdown('''
        <div class="tooltip-label">
            Client Enterprise Details
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        client_name_provided = bool(client_enterprise_name and client_enterprise_name.strip())
        
        enterprise_details = st.text_area(
            label="Client Enterprise Details", 
            value=client_data.enterprise_details_content if client_name_provided else "",
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Select/Enter the client website URL to fetch enterprise details", 
            height=150, 
            key="enterprise_details_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Update dataclass when text area changes
        if client_name_provided and enterprise_details != client_data.enterprise_details_content:
            ClientDataManager.update_client_data(enterprise_details_content=enterprise_details)

    # Client Requirements and Pain Points Row
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
            value=client_data.client_requirements_content if client_name_provided else "", 
            height=200, 
            key="client_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided,
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Add your client requirements here youmay take suggestions from AI in the right as well"
        )
        
        # Update the client data when the text area changes (only if enabled)
        if client_name_provided:
            ClientDataManager.update_client_data(client_requirements_content=client_requirements)
        
        client_requirements_provided = bool(client_name_provided and client_requirements.strip())
        
    with col6:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Client Pain Points
            <div class="tooltip-icon" data-tooltip="This area displays extracted pain points from RFI documents or website analysis. You can also manually enter client's business challenges, current pain points, and organizational details that will help customize your proposal.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get RFI pain points items from client data or use dummy data
        if client_name_provided and client_data.rfi_pain_points_items:
            rfi_pain_points_items = client_data.rfi_pain_points_items
        else:
            # Dummy data when no client name or no file uploaded
            rfi_pain_points_items = {
                "Revenue Challenges": "**Revenue Challenges** • Sales declined by 15% year-over-year despite market growth\n• Missed quarterly revenue targets by $2.3M for three consecutive quarters\n• Average deal size decreased by 22% due to increased price competition\n• Customer churn rate increased to 18%, up from 12% previous year\n• Revenue per customer dropped 8% as clients downgraded service tiers\n• New product launches generated only 60% of projected revenue\n• Seasonal revenue fluctuations creating 40% variance between peak and low periods\n• Pipeline conversion rates fell from 35% to 24% over past 12 months\n\n",
                
                "Cost and Margin Pressure": "**Cost and Margin Pressure** • Cost of Goods Sold increased by 12% due to supply chain disruptions\n• Labor costs rose 18% while productivity remained flat\n• Raw material prices up 25% with limited ability to pass costs to customers\n• Operational efficiency decreased by 14% due to outdated processes\n• Procurement costs increased 20% from supplier consolidation issues\n• Technology infrastructure costs grew 30% without proportional business benefits\n• Regulatory compliance expenses added $1.8M in unexpected annual costs\n• Facility and overhead costs up 16% while revenue remained stagnant\n\n",
                
                "Market Expansion and Customer Acquisition": "**Market Expansion and Customer Acquisition**\n\n • Win rate on new business opportunities dropped from 42% to 28%\n• Customer acquisition cost increased 35% while customer lifetime value declined\n• Expansion into new geographic markets yielding only 40% of projected results\n• Lack of local market knowledge resulting in 60% longer sales cycles\n• Digital marketing campaigns generating 50% fewer qualified leads\n• Competition from new market entrants capturing 25% of target customer segment\n• Limited brand recognition in new markets requiring 3x marketing investment\n• Difficulty penetrating enterprise accounts with average sales cycle extending to 18 months\n\n"
            }

        # Use a single container for all pain points items
        with st.container():
            # Display pain points items with add/remove buttons
            for i, (key, value) in enumerate(rfi_pain_points_items.items()):
                # Check if this item is selected
                is_selected = key in client_data.selected_pain_points
                
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
                            # Get current content from the client data
                            current_content = client_data.client_requirements_content
                            
                            # Get the original content that was added for this key
                            original_content = client_data.pain_point_content_map.get(key, value)
                            
                            # Remove this specific pain point section from content
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
                            
                            # Update client data
                            client_data.selected_pain_points.discard(key)
                            if key in client_data.pain_point_content_map:
                                del client_data.pain_point_content_map[key]
                            
                            ClientDataManager.update_client_data(
                                client_requirements_content=updated_content,
                                selected_pain_points=client_data.selected_pain_points,
                                pain_point_content_map=client_data.pain_point_content_map
                            )
                            
                        else:
                            # ADD FUNCTIONALITY
                            # Get current content from client data
                            current_content = client_data.client_requirements_content
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update client data
                            client_data.selected_pain_points.add(key)
                            client_data.pain_point_content_map[key] = value
                            
                            ClientDataManager.update_client_data(
                                client_requirements_content=new_content,
                                selected_pain_points=client_data.selected_pain_points,
                                pain_point_content_map=client_data.pain_point_content_map
                            )
                        
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
                        background_color = "#f5f5f5"
                        border_color = "#404040"
                        text_color = "#000000"
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
            value=client_data.spoc_name,
            placeholder="Enter SPOC full name...", 
            key="spoc_name_input",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Update client data when SPOC name changes
        if spoc_name != client_data.spoc_name:
            ClientDataManager.update_client_data(spoc_name=spoc_name)
        
        # Automatically search for LinkedIn profiles when SPOC name changes
        if spoc_name and spoc_name.strip() and spoc_name != client_data.last_searched_spoc and client_name_provided:
            with st.spinner(f"Searching LinkedIn profiles for {spoc_name}..."):
                # Assuming search_linkedin_serpapi is available
                linkedin_profiles = search_linkedin_serpapi(spoc_name.strip())
                ClientDataManager.update_client_data(
                    linkedin_profiles=linkedin_profiles,
                    last_searched_spoc=spoc_name
                )
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
        if spoc_name_provided and client_data.linkedin_profiles:
            # Create options with profile titles for better selection
            linkedin_options = ["Select a LinkedIn profile..."]
            linkedin_url_mapping = {}  # To map display text to actual URL
            
            for url, profile_data in client_data.linkedin_profiles.items():
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
                ClientDataManager.update_client_data(spoc_linkedin_profile=spoc_linkedin_profile)
            else:
                spoc_linkedin_profile = None
                
        elif spoc_name_provided and not client_data.linkedin_profiles:
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
    if spoc_name_provided and client_data.linkedin_profiles:
        # Check if LinkedIn profile selection has changed
        profile_changed = False
        if 'spoc_linkedin_profile' in locals() and spoc_linkedin_profile:
            if client_data.current_selected_profile_url != spoc_linkedin_profile:
                ClientDataManager.update_client_data(current_selected_profile_url=spoc_linkedin_profile)
                profile_changed = True
                
            selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
            if selected_profile_data:
                st.info(f"""**Selected Profile:** {selected_profile_data['role']} - {selected_profile_data['name']}  
    **LinkedIn URL:** {spoc_linkedin_profile}""")
                
                # Update roles and priorities when profile changes
                if profile_changed:
                    # Remove previously auto-populated LinkedIn role if it exists
                    linkedin_roles_to_remove = []
                    for i, role in enumerate(client_data.selected_target_roles):
                        # Check if this role was from a previous LinkedIn profile
                        for url, profile in client_data.linkedin_profiles.items():
                            if url != spoc_linkedin_profile and profile['role'] == role:
                                linkedin_roles_to_remove.append(i)
                                break
                    
                    # Remove old LinkedIn roles
                    for idx in reversed(linkedin_roles_to_remove):
                        client_data.selected_target_roles.pop(idx)
                    
                    # Add new LinkedIn role
                    linkedin_role = selected_profile_data['role']
                    if linkedin_role and linkedin_role not in client_data.selected_target_roles:
                        client_data.selected_target_roles.append(linkedin_role)
                    
                    # Remove old LinkedIn priorities and add new ones
                    linkedin_priorities_to_remove = []
                    for priority in client_data.selected_business_priorities:
                        # Check if this priority was from a previous LinkedIn profile
                        for url, profile in client_data.linkedin_profiles.items():
                            if url != spoc_linkedin_profile and priority in profile.get('top_3_priorities', []):
                                linkedin_priorities_to_remove.append(priority)
                                break
                    
                    # Remove old LinkedIn priorities
                    for priority in linkedin_priorities_to_remove:
                        if priority in client_data.selected_business_priorities:
                            client_data.selected_business_priorities.remove(priority)
                    
                    # Add new LinkedIn priorities
                    inferred_priorities = selected_profile_data.get('top_3_priorities', [])
                    for priority in inferred_priorities:
                        if priority not in client_data.selected_business_priorities:
                            client_data.selected_business_priorities.append(priority)
                    
                    # Update client data
                    ClientDataManager.update_client_data(
                        selected_target_roles=client_data.selected_target_roles,
                        selected_business_priorities=client_data.selected_business_priorities
                    )
                    
                    # Force rerun to update the display
                    st.rerun()
        elif client_data.current_selected_profile_url is not None:
            # Profile was deselected
            ClientDataManager.update_client_data(current_selected_profile_url=None)
            profile_changed = True

    # Roles and Priorities Row
    col7, col8 = st.columns([1, 1])

    with col7:
        st.markdown('''
        <div class="tooltip-label">
            SPOC Role 
            <div class="tooltip-icon" data-tooltip="Select specific roles or positions within the client organization that your proposal should target. These are key stakeholders who will be involved in the decision-making process.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)

        # Prepare role options for dropdown based on LinkedIn profile selection
        role_options = ["Select a role..."]
        
        # Get default roles from function (assuming this function exists)
        target_roles_list = get_roles_list() or []
        
        # Check if a LinkedIn profile is selected
        selected_linkedin_role = None
        if (spoc_name_provided and 
            client_data.linkedin_profiles and 
            'spoc_linkedin_profile' in locals() and 
            spoc_linkedin_profile):
            
            # Get the selected LinkedIn profile data
            selected_profile_data = client_data.linkedin_profiles.get(spoc_linkedin_profile)
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
            if spoc_name_provided and client_data.linkedin_profiles:
                for url, profile_data in client_data.linkedin_profiles.items():
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

        # ROLES DROPDOWN - Only one role can be selected
        selected_target_role = st.selectbox(
            label="Target Role Selector", 
            options=role_options,
            index=role_options.index(current_selection) if current_selection in role_options else 0,
            key="target_role_selector_dropdown",
            label_visibility="collapsed",
            disabled=not (client_name_provided and spoc_name_provided),
            accept_new_options=True
        )

        # Update client_data with the single selected role
        if selected_target_role and selected_target_role != "Select a role...":
            # Store as a single role, not a list
            client_data.selected_target_role = selected_target_role
            ClientDataManager.update_client_data(selected_target_role=selected_target_role)
        else:
            client_data.selected_target_role = None
            ClientDataManager.update_client_data(selected_target_role=None)

    with col8:
        # Label with tooltip
        st.markdown('''
        <div class="tooltip-label">
            SPOC Business priorities
            <div class="tooltip-icon" data-tooltip="Select Business priorities of the SPOC based on their role.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)

        # Default priorities (used if role is not selected or error occurs)
        default_priorities = [
            {'title': 'Revenue Growth and Market Share Expansion', 'icon': '📈'}, 
            {'title': 'Profitability and Cost Optimization', 'icon': '💰'}, 
            {'title': 'Digital Transformation and Innovation', 'icon': '🤖'}
        ]

        # Load role-based priorities if role is selected
        business_priorities_list = default_priorities  # Start with default
        if (
            spoc_name_provided and 
            hasattr(client_data, 'selected_target_role') and 
            client_data.selected_target_role and 
            client_data.selected_target_role != "Select a role..."
        ):
            try:
                role_priorities = get_ai_business_priorities(client_data.selected_target_role)
                if role_priorities:
                    business_priorities_list = role_priorities
            except Exception:
                pass  # Silently fall back to default

        # Initialize selected_business_priorities if missing
        if not hasattr(client_data, 'selected_business_priorities'):
            client_data.selected_business_priorities = []

        # Show checkboxes for priorities
        for i, priority in enumerate(business_priorities_list):
            priority_title = priority.get('title') if isinstance(priority, dict) else str(priority)
            priority_icon = priority.get('icon', '📋') if isinstance(priority, dict) else '📋'
            display_text = f"{priority_icon} **{priority_title}**"
            
            # Determine checkbox state
            default_checked = priority_title in client_data.selected_business_priorities
            is_enabled = (
                spoc_name_provided and 
                hasattr(client_data, 'selected_target_role') and 
                client_data.selected_target_role and 
                client_data.selected_target_role != "Select a role..."
            )
            
            is_checked = st.checkbox(
                display_text,
                key=f"business_priority_checkbox_{i}",
                value=default_checked,
                disabled=not spoc_name_provided
            )

            # Update selected priorities
            if is_checked and priority_title not in client_data.selected_business_priorities:
                client_data.selected_business_priorities.append(priority_title)
                ClientDataManager.update_client_data(selected_business_priorities=client_data.selected_business_priorities)
            elif not is_checked and priority_title in client_data.selected_business_priorities:
                client_data.selected_business_priorities.remove(priority_title)
                ClientDataManager.update_client_data(selected_business_priorities=client_data.selected_business_priorities)

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
            value=client_data.client_additional_requirements_content if client_name_provided else "",
            placeholder="Enter client name first to enable this field" if not client_name_provided else "Enter specific client requirements, expectations, project scope, compliance needs, budget constraints...",
            height=200,
            key="client_additional_requirements_textarea",
            label_visibility="collapsed",
            disabled=not client_name_provided
        )
        
        # Update the dataclass when the text area changes (only if enabled)
        if client_name_provided and client_additional_requirements != client_data.client_additional_requirements_content:
            ClientDataManager.update_client_data(client_additional_requirements_content=client_additional_requirements)
            client_data = ClientDataManager.get_client_data()  # Refresh reference
        
        client_additional_requirements_provided = bool(client_name_provided and client_additional_requirements.strip())

    with col10:
        # Title with tooltip only (no buttons)
        st.markdown('''
        <div class="tooltip-label">
            Additional Specifications to be considered
            <div class="tooltip-icon" data-tooltip="AI-generated additional specifications and technical requirements based on RFI analysis. These are supplementary specs that complement the main requirements and help ensure comprehensive proposal coverage.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get additional specs items from client data or use dummy data
        if client_name_provided and client_data.additional_specs_items:
            additional_specs_items = client_data.additional_specs_items
        else:
            # Dummy data when no client name or no specific data
            additional_specs_items = {
                "Technical Infrastructure Requirements": "**Technical Infrastructure Requirements**\n• Cloud hosting with 99.9% uptime SLA and auto-scaling capabilities\n• Multi-region deployment for disaster recovery and performance optimization\n• Integration with existing ERP, CRM, and financial management systems\n• API-first architecture with RESTful services and webhook support\n• Database performance optimization with sub-second query response times\n• Security compliance with SOC2, ISO 27001, and industry-specific regulations\n• Load balancing and CDN implementation for global content delivery\n• Automated backup and recovery systems with point-in-time restoration\n\n",
                
                "Compliance and Security Standards": "**Compliance and Security Standards**\n• GDPR, CCPA, and regional data privacy regulation compliance\n• End-to-end encryption for data in transit and at rest\n• Multi-factor authentication and role-based access controls\n• Regular security audits and penetration testing protocols\n• Data retention and deletion policies per regulatory requirements\n• Audit trail logging for all system interactions and data changes\n• Incident response plan with 4-hour notification requirements\n• Employee background checks and security clearance verification\n\n",
                
                "Performance and Scalability Metrics": "**Performance and Scalability Metrics**\n• System response time under 2 seconds for 95% of user interactions\n• Concurrent user capacity of 10,000+ with linear scaling capability\n• Database query optimization with indexing and caching strategies\n• Mobile application performance with offline synchronization\n• Bandwidth optimization for low-connectivity environments\n• Real-time analytics and reporting with sub-minute data refresh\n• Automated performance monitoring with threshold-based alerting\n• Capacity planning with predictive scaling based on usage patterns\n\n"
            }

        # Use a single container for all additional specs items
        with st.container():
            # Display additional specs items with add/remove buttons
            for i, (key, value) in enumerate(additional_specs_items.items()):
                # Check if this item is selected
                is_selected = key in client_data.selected_additional_specs
                
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
                            # Get current content from the dataclass
                            current_content = client_data.client_additional_requirements_content
                            
                            # Get the original content that was added for this key
                            original_content = client_data.additional_specs_content_map.get(key, value)
                            
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
                            
                            # Update the dataclass
                            client_data.client_additional_requirements_content = updated_content
                            client_data.selected_additional_specs.discard(key)
                            if key in client_data.additional_specs_content_map:
                                del client_data.additional_specs_content_map[key]
                            
                            # Save changes to session state
                            ClientDataManager.save_client_data(client_data)
                            
                        else:
                            # ADD FUNCTIONALITY
                            # Get current content from the dataclass
                            current_content = client_data.client_additional_requirements_content
                            
                            # Append the value to the content
                            new_content = current_content + f"\n\n{value}" if current_content else value
                            
                            # Update the dataclass
                            client_data.client_additional_requirements_content = new_content
                            client_data.additional_specs_content_map[key] = value
                            client_data.selected_additional_specs.add(key)
                            
                            # Save changes to session state
                            ClientDataManager.save_client_data(client_data)
                        
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
                        background_color = "#f5f5f5"
                        border_color = "#404040"
                        text_color = "#000000"
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
    if client_data.show_validation:
        # Your validation logic here
        pass