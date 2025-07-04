from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import streamlit as st
import logging
from Seller.seller_css import seller_css
from Seller.seller_utils import *
from Search.Linkedin.linkedin_serp import *
from Recommendation.recommendation_utils import *
from Common_Utils.ai_suggestion_utils import *

# Configure logger
logger = logging.getLogger(__name__)

@dataclass
class SellerTabState:
    """Dataclass to manage all seller tab state with persistence across tab switches."""
    
    # Basic seller information
    seller_enterprise_name: str = ""
    seller_website_url: str = ""
    seller_website_urls_list: List[str] = field(default_factory=list)
    last_seller_company_name: str = ""
    last_analyzed_seller_url: Optional[str] = None
    
    # Content fields
    enterprise_logo :str = ""
    seller_enterprise_details_content: str = ""
    seller_requirements_content: str = ""
    
    # Document handling
    seller_uploaded_file_path: Optional[str] = None
    seller_uploaded_files_paths: Dict[str, str] = field(default_factory=dict)
    seller_services_by_file: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    seller_services_items: Dict[str, Any] = field(default_factory=dict)
    seller_document_analyzed: bool = False
    
    # Processing states
    show_validation: bool = False
    url_search_in_progress: bool = False
    url_search_company: str = ""
    seller_scraping_in_progress: bool = False
    seller_pending_scrape_url: Optional[str] = None
    processing_all_seller_documents: bool = False
    
    # LinkedIn related
    seller_linkedin_profiles: Dict[str, Any] = field(default_factory=dict)
    last_searched_seller_spoc: str = ""
    
    # RFI and pain points
    seller_rfi_pain_points_items: Dict[str, Any] = field(default_factory=dict)
    
    # Service selection states
    selected_services_offered: Dict[str, bool] = field(default_factory=dict)
    services_content_map: Dict[str, str] = field(default_factory=dict)
    selected_additional_capabilities: Dict[str, bool] = field(default_factory=dict)
    capabilities_content_map: Dict[str, str] = field(default_factory=dict)
    
    def to_session_state(self) -> None:
        """Save all dataclass fields to Streamlit session state."""
        try:
            for field_name, field_value in self.__dict__.items():
                st.session_state[field_name] = field_value
            logger.debug("Seller tab state saved to session state")
        except Exception as e:
            logger.error(f"Error saving seller state to session: {str(e)}")
    
    @classmethod
    def from_session_state(cls) -> 'SellerTabState':
        """Load seller tab state from Streamlit session state."""
        try:
            # Get all field names from the dataclass
            field_names = {f.name for f in cls.__dataclass_fields__.values()}
            
            # Create kwargs dict with values from session state or defaults
            kwargs = {}
            for field_name in field_names:
                if field_name in st.session_state:
                    kwargs[field_name] = st.session_state[field_name]
            
            instance = cls(**kwargs)
            logger.debug("Seller tab state loaded from session state")
            return instance
            
        except Exception as e:
            logger.error(f"Error loading seller state from session: {str(e)}")
            return cls()  # Return default instance on error
    
    def update_field(self, field_name: str, value: Any) -> None:
        """Update a specific field and sync to session state."""
        try:
            if hasattr(self, field_name):
                setattr(self, field_name, value)
                st.session_state[field_name] = value
                logger.debug(f"Updated seller state field: {field_name}")
            else:
                logger.warning(f"Attempted to update non-existent field: {field_name}")
        except Exception as e:
            logger.error(f"Error updating field {field_name}: {str(e)}")
    
    def clear_url_data(self) -> None:
        """Clear URL-related data when company name changes."""
        try:
            self.seller_website_urls_list = []
            self.last_seller_company_name = ""
            self.url_search_in_progress = False
            self.url_search_company = ""
            self.to_session_state()
            logger.debug("URL data cleared")
        except Exception as e:
            logger.error(f"Error clearing URL data: {str(e)}")
    
    def reset_processing_states(self) -> None:
        """Reset all processing-related states."""
        try:
            self.url_search_in_progress = False
            self.seller_scraping_in_progress = False
            self.processing_all_seller_documents = False
            self.seller_pending_scrape_url = None
            self.url_search_company = ""
            self.to_session_state()
            logger.debug("Processing states reset")
        except Exception as e:
            logger.error(f"Error resetting processing states: {str(e)}")
    
    def add_processed_file(self, file_key: str, filename: str, services: Dict[str, Any], file_path: str) -> None:
        """Add a processed file to the state."""
        try:
            self.seller_services_by_file[file_key] = {
                'filename': filename,
                'services': services,
                'file_path': file_path
            }
            
            # Update services items
            if isinstance(services, dict):
                self.seller_services_items.update(services)
            
            self.seller_document_analyzed = True
            self.to_session_state()
            logger.debug(f"Added processed file: {filename}")
        except Exception as e:
            logger.error(f"Error adding processed file: {str(e)}")
    
    def is_file_processed(self, file_key: str) -> bool:
        """Check if a file has been processed."""
        return file_key in self.seller_services_by_file
    
    def get_processed_files_count(self) -> int:
        """Get count of processed files."""
        return len(self.seller_services_by_file)
    
    def validate_required_fields(self) -> Dict[str, bool]:
        """Validate required fields and return validation results."""
        validation_results = {
            'seller_enterprise_name': bool(self.seller_enterprise_name and self.seller_enterprise_name.strip()),
            'seller_website_url': bool(self.seller_website_url and self.seller_website_url.strip()),
            'seller_enterprise_details_content': bool(self.seller_enterprise_details_content and self.seller_enterprise_details_content.strip())
        }
        return validation_results


def seller_tab():
    """Main seller tab function with dataclass-based state management."""
    try:
        logger.info("Starting seller_tab function")
        
        # Load or create seller state
        seller_state = SellerTabState.from_session_state()
        
        # Re-apply CSS after every rerun to ensure persistence
        try:
            st.markdown(seller_css, unsafe_allow_html=True)
            logger.debug("CSS applied successfully")
        except Exception as e:
            logger.error(f"Error applying CSS: {str(e)}")
            st.error("Error loading page styles")
        
        # Render main UI components
        _render_top_section(seller_state)
        _render_document_upload_section(seller_state)
        _render_enterprise_details_section(seller_state)
        
        logger.info("Seller tab rendered successfully")
        
    except Exception as e:
        logger.error(f"Critical error in seller_tab: {str(e)}", exc_info=True)
        st.error("A critical error occurred while loading the seller tab. Please refresh the page.")
    return seller_state

def _render_top_section(seller_state: SellerTabState):
    """Render the top section with seller name and URL inputs."""
    try:
        logger.debug("Rendering top section")
        
        # Top section with seller name and URLs
        col1, col2 = st.columns([1, 1])
        
        with col1:
            _render_seller_name_input(seller_state)
        
        with col2:
            _render_website_url_section(seller_state)
            
        logger.debug("Top section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering top section: {str(e)}", exc_info=True)
        st.error("Error loading seller information section")


def _render_seller_name_input(seller_state: SellerTabState):
    """Render seller name input with find URLs functionality."""
    try:
        logger.debug("Rendering seller name input")
        
        st.markdown("""
            <div class="tooltip-label">
                Seller Enterprise Name <span style="color:red;">*</span>
                <div class="tooltip-icon" data-tooltip="Enter the full legal name of the seller organization. This is the primary identifier for the seller in all documentation and communications. This field is mandatory for creating the seller profile.">ⓘ</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create a sub-column layout for name input and find URLs button
        name_col, button_col = st.columns([3, 1])
        
        with name_col:
            seller_enterprise_name = st.text_input(
                label="Seller Enterprise Name", 
                placeholder="Enter seller enterprise name...", 
                value=seller_state.seller_enterprise_name,
                key="seller_enterprise_name_input",
                label_visibility="collapsed"
            )
            
            # Update state if changed
            if seller_enterprise_name != seller_state.seller_enterprise_name:
                seller_state.update_field('seller_enterprise_name', seller_enterprise_name)
        
        with button_col:
            _handle_find_urls_button(seller_state, seller_enterprise_name)
        
        # Common area for spinner/status - displayed under both input and button
        _display_url_search_status(seller_state, seller_enterprise_name)
        
        # Clear URLs if company name is cleared
        _handle_company_name_changes(seller_state, seller_enterprise_name)
        
        # Show validation warning if triggered and field is empty
        if seller_state.show_validation and check_field_validation("Seller Enterprise Name", seller_enterprise_name, True):
            show_field_warning("Seller Enterprise Name")
            
        logger.debug("Seller name input rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering seller name input: {str(e)}", exc_info=True)
        st.error("Error loading seller name input")


def _handle_find_urls_button(seller_state: SellerTabState, seller_enterprise_name: str):
    """Handle find URLs button functionality."""
    try:
        # Find URLs button - only enabled when seller name has more than 2 characters
        find_urls_disabled = not (seller_enterprise_name and len(seller_enterprise_name.strip()) > 2)
        
        if st.button("🔍 Find Website",
                    disabled=find_urls_disabled or seller_state.url_search_in_progress,
                    help="Find website URLs for this company",
                    key="find_seller_urls_button"):
            
            logger.info(f"Finding URLs for company: {seller_enterprise_name.strip()}")
            
            # Set search in progress flag
            seller_state.update_field('url_search_in_progress', True)
            seller_state.update_field('url_search_company', seller_enterprise_name.strip())
            st.rerun()
                    
    except Exception as e:
        logger.error(f"Error in find URLs button handler: {str(e)}", exc_info=True)
        st.error("Error with URL search functionality")


def _handle_company_name_changes(seller_state: SellerTabState, seller_enterprise_name: str):
    """Handle changes in company name and clear URLs if needed."""
    try:
        if not seller_enterprise_name and seller_state.last_seller_company_name:
            seller_state.clear_url_data()
            logger.debug("Cleared URLs due to empty company name")
            
    except Exception as e:
        logger.error(f"Error handling company name changes: {str(e)}", exc_info=True)


def _display_url_search_status(seller_state: SellerTabState, seller_enterprise_name: str):
    """Display URL search status in a common area under name input and button."""
    try:
        # Check if URL search is in progress
        if seller_state.url_search_in_progress:
            search_company = seller_state.url_search_company or seller_enterprise_name
            
            # Display spinner in common area
            with st.spinner(f"🔍 Finding websites for '{search_company}'..."):
                try:
                    urls_list = get_urls_list(search_company)
                    seller_state.update_field('seller_website_urls_list', urls_list)
                    seller_state.update_field('last_seller_company_name', search_company)
                    
                    # Clear search state
                    seller_state.update_field('url_search_in_progress', False)
                    seller_state.update_field('url_search_company', '')
                    
                    logger.info(f"Successfully found {len(urls_list)} URLs for {search_company}")
                    
                    # Show success message in the common area
                    if urls_list:
                        st.success(f"✅ Found {len(urls_list)} website(s) for {search_company}")
                    else:
                        st.warning(f"⚠️ No websites found for {search_company}")
                    
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error finding URLs for {search_company}: {str(e)}", exc_info=True)
                    seller_state.update_field('seller_website_urls_list', [])
                    seller_state.update_field('url_search_in_progress', False)
                    seller_state.update_field('url_search_company', '')
                    st.error(f"❌ Error finding URLs: {str(e)}")
        
        # Show current status if URLs exist
        elif seller_state.seller_website_urls_list and seller_state.last_seller_company_name:
            url_count = len(seller_state.seller_website_urls_list)
            company_name = seller_state.last_seller_company_name
            #st.info(f"ℹ️ {url_count} website(s) available for {company_name}")
            
    except Exception as e:
        logger.error(f"Error displaying URL search status: {str(e)}", exc_info=True)


def _render_website_url_section(seller_state: SellerTabState):
    """Render website URL selection and action buttons."""
    try:
        logger.debug("Rendering website URL section")
        
        # Label row with inline emoji and tooltip
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Seller Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the seller's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help understand the seller's capabilities and offerings.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create columns for dropdown and buttons
        url_col, btn1_col, btn2_col, btn3_col = st.columns([7, 1, 1, 1])
        
        with url_col:
            seller_website_url = _render_url_dropdown(seller_state)
        
        # Render action buttons
        with btn1_col:
            _render_visit_website_button(seller_website_url)
        with btn2_col:
            _render_refresh_urls_button(seller_state, seller_website_url)
        with btn3_col:
            _render_scrape_website_button(seller_state, seller_website_url)
        
        # Handle pending scraping operation
        _handle_pending_scraping(seller_state)
        
        # Show validation warning if needed
        if seller_state.show_validation and check_field_validation("Seller Website URL", seller_website_url, False):
            show_field_warning("Seller Website URL")
            
        logger.debug("Website URL section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering website URL section: {str(e)}", exc_info=True)
        st.error("Error loading website URL section")


def _render_url_dropdown(seller_state: SellerTabState):
    """Render URL dropdown selection."""
    try:
        seller_name_provided = bool(seller_state.seller_enterprise_name and seller_state.seller_enterprise_name.strip())
        
        if not seller_state.seller_website_urls_list:
            url_options = ["Select seller website URL"]
        else:
            url_options = ["Select seller website URL"] + seller_state.seller_website_urls_list
        
        # Set initial index based on current URL
        initial_index = 0
        if seller_state.seller_website_url and seller_state.seller_website_url in url_options:
            initial_index = url_options.index(seller_state.seller_website_url)
        
        seller_website_url = st.selectbox(
            label="Seller Website URL",
            options=url_options,
            index=initial_index,
            key="seller_website_url_selector",
            label_visibility="collapsed",
            disabled=not seller_name_provided,
            accept_new_options=True
        )
        
        # Reset to empty string if default option is selected
        if seller_website_url == "Select seller website URL":
            seller_website_url = ""
        
        # Update state if URL changed
        if seller_website_url != seller_state.seller_website_url:
            seller_state.update_field('seller_website_url', seller_website_url)
            
        return seller_website_url
        
    except Exception as e:
        logger.error(f"Error rendering URL dropdown: {str(e)}", exc_info=True)
        return ""


def _render_visit_website_button(seller_website_url: str):
    """Render visit website button."""
    try:
        if seller_website_url:
            st.link_button("🌐", seller_website_url, help="Visit website", use_container_width=True)
        else:
            st.button("🌐", help="Visit website", disabled=True, use_container_width=True)
            
    except Exception as e:
        logger.error(f"Error rendering visit website button: {str(e)}", exc_info=True)


def _render_refresh_urls_button(seller_state: SellerTabState, seller_website_url: str):
    """Render refresh URLs button and handle refresh action."""
    try:
        refresh_clicked = st.button("🔄", help="Refresh website URLs list", 
                                  key="refresh_seller_urls_btn", use_container_width=True, 
                                  disabled=not seller_website_url)
        
        if refresh_clicked:
            _handle_refresh_urls(seller_state)
            
    except Exception as e:
        logger.error(f"Error with refresh URLs button: {str(e)}", exc_info=True)


def _handle_refresh_urls(seller_state: SellerTabState):
    """Handle URL refresh functionality."""
    try:
        seller_name_provided = bool(seller_state.seller_enterprise_name and seller_state.seller_enterprise_name.strip())
        
        if seller_name_provided:
            logger.info(f"Refreshing URLs for: {seller_state.seller_enterprise_name}")
            
            with st.spinner("Refreshing website URLs..."):
                try:
                    urls_list = get_urls_list(seller_state.seller_enterprise_name)
                    seller_state.update_field('seller_website_urls_list', urls_list)
                    st.success("Website URLs refreshed!")
                    st.rerun()
                    
                    logger.info(f"Successfully refreshed {len(urls_list)} URLs")
                    
                except Exception as e:
                    logger.error(f"Error refreshing URLs: {str(e)}", exc_info=True)
                    st.error(f"Error refreshing URLs: {str(e)}")
                    
    except Exception as e:
        logger.error(f"Error in refresh URLs handler: {str(e)}", exc_info=True)


def _render_scrape_website_button(seller_state: SellerTabState, seller_website_url: str):
    """Render scrape website button."""
    try:
        scrape_clicked = st.button("📑", help="Get enterprise details", 
                                 key="scrape_seller_website_btn", use_container_width=True, 
                                 disabled=not seller_website_url)
        
        if scrape_clicked and seller_website_url:
            logger.info(f"Initiating website scraping for: {seller_website_url}")
            seller_state.update_field('seller_pending_scrape_url', seller_website_url)
            seller_state.update_field('seller_scraping_in_progress', True)
            st.rerun()
            
    except Exception as e:
        logger.error(f"Error with scrape website button: {str(e)}", exc_info=True)


def _handle_pending_scraping(seller_state: SellerTabState):
    """Handle pending website scraping operation."""
    try:
        if seller_state.seller_scraping_in_progress and seller_state.seller_pending_scrape_url:
            scrape_url = seller_state.seller_pending_scrape_url
            logger.info(f"Processing pending scrape for: {scrape_url}")
            
            with st.spinner(f"Scraping website details from {scrape_url}..."):
                try:
                    # Get both website details and logo from the URL
                    scrape_result = get_url_details(scrape_url)
                    
                    # Handle different return formats from get_url_details
                    if isinstance(scrape_result, dict):
                        # If get_url_details returns a dictionary with separate fields
                        website_details = scrape_result.get('website_details', '')
                        logo_url = scrape_result.get('logo', '')
                    elif isinstance(scrape_result, tuple) and len(scrape_result) >= 2:
                        # If get_url_details returns a tuple (website_details, logo)
                        website_details, logo_url = scrape_result[0], scrape_result[1]
                    else:
                        # If get_url_details returns only website details (backward compatibility)
                        website_details = str(scrape_result)
                        logo_url = ''
                    
                    # Update seller state with website details
                    seller_state.update_field('seller_enterprise_details_content', website_details)
                    seller_state.update_field('last_analyzed_seller_url', scrape_url)
                    
                    # Update seller state with logo if available
                    if logo_url:
                        seller_state.update_field('enterprise_logo', logo_url)
                        logger.info(f"Logo found and saved: {logo_url}")
                    
                    # Clear pending operation
                    seller_state.update_field('seller_scraping_in_progress', False)
                    seller_state.update_field('seller_pending_scrape_url', None)
                    
                    # Show success message with logo info
                    if logo_url:
                        st.success("Website details and logo extracted successfully!")
                    else:
                        st.success("Website details extracted successfully!")
                    
                    logger.info(f"Successfully scraped website: {scrape_url}")
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error scraping website {scrape_url}: {str(e)}", exc_info=True)
                    # Clear pending operation on error
                    seller_state.update_field('seller_scraping_in_progress', False)
                    seller_state.update_field('seller_pending_scrape_url', None)
                    st.error(f"Error scraping website: {str(e)}")
                    
    except Exception as e:
        logger.error(f"Error handling pending scraping: {str(e)}", exc_info=True)



def _render_document_upload_section(seller_state: SellerTabState):
    """Render document upload section with comprehensive error handling."""
    try:
        logger.debug("Rendering document upload section")
        
        st.markdown('''
        <div class="tooltip-label">
            Upload Seller Document
            <div class="tooltip-icon" data-tooltip="Upload seller-related documents such as company profiles, service catalogs, capabilities documents, or proposals in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key capabilities, services, and business strengths to help understand the seller's offerings.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add custom CSS
        _add_document_upload_css()
        
        # FILE UPLOAD
        seller_documents_upload = st.file_uploader(
            label="Upload Seller Documents", 
            type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
            key="seller_documents_uploader",
            label_visibility="collapsed",
            accept_multiple_files=True
        )
        
        if seller_documents_upload and len(seller_documents_upload) > 0:
            _handle_uploaded_documents(seller_state, seller_documents_upload)
            
        logger.debug("Document upload section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering document upload section: {str(e)}", exc_info=True)
        st.error("Error loading document upload section")


def _add_document_upload_css():
    """Add CSS for document upload section."""
    try:
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
        
    except Exception as e:
        logger.error(f"Error adding document upload CSS: {str(e)}", exc_info=True)


def _handle_uploaded_documents(seller_state: SellerTabState, seller_documents_upload):
    """Handle uploaded documents display and processing."""
    try:
        logger.debug(f"Handling {len(seller_documents_upload)} uploaded documents")
        
        st.markdown("**Uploaded Documents:**")
        
        # Display all uploaded files
        _display_uploaded_files(seller_state, seller_documents_upload)
        
        # Single button to process all files
        st.markdown("---")
        _render_process_all_button(seller_state, seller_documents_upload)
        
        # Handle processing when button is clicked
        if seller_state.processing_all_seller_documents:
            _process_all_documents(seller_state, seller_documents_upload)
            
        logger.debug("Uploaded documents handled successfully")
        
    except Exception as e:
        logger.error(f"Error handling uploaded documents: {str(e)}", exc_info=True)
        st.error("Error processing uploaded documents")


def _display_uploaded_files(seller_state: SellerTabState, seller_documents_upload):
    """Display information about uploaded files."""
    try:
        for idx, uploaded_file in enumerate(seller_documents_upload):
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            
            # Calculate file size display
            file_size_kb = round(uploaded_file.size / 1024, 1)
            file_size_display = f"{file_size_kb}KB" if file_size_kb < 1024 else f"{round(file_size_kb/1024, 1)}MB"
            
            # Check processing status
            is_processed = seller_state.is_file_processed(file_key)
            is_processing = seller_state.processing_all_seller_documents
            
            if is_processing:
                st.markdown(f"""
                <div class="processing-file">
                    <span style='font-size:0.8em' class="analyzing-text">
                        🔄 {uploaded_file.name[:25]}{'...' if len(uploaded_file.name) > 25 else ''} (Analyzing...)
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                status_icon = "✅" if is_processed else "📄"
                st.markdown(f"<span style='font-size:0.8em'>{status_icon} {uploaded_file.name[:30]}{'...' if len(uploaded_file.name) > 30 else ''} ({file_size_display})</span>", 
                        unsafe_allow_html=True)
                        
    except Exception as e:
        logger.error(f"Error displaying uploaded files: {str(e)}", exc_info=True)

def _render_process_all_button(seller_state: SellerTabState, seller_documents_upload):
    """Render button to process all documents."""
    try:
        all_processed = all(
            f"{file.name}_{file.size}" in seller_state.seller_services_by_file
            for file in seller_documents_upload
        )
        
        is_processing = seller_state.processing_all_seller_documents
        
        if all_processed:
            button_color = "#28a745"
            button_text = "All Documents Processed"
            button_disabled = True
        elif is_processing:
            button_color = "#FF6B6B"
            button_text = "Analyzing All Documents..."
            button_disabled = True
        else:
            button_color = "#4CAF50"
            button_text = f"Get Services from All Documents ({len(seller_documents_upload)} files)"
            button_disabled = False

        st.markdown(f"""
        <style>
        div.stButton > button:first-child {{
            background-color: {button_color};
            color: white;
            border: none;
            font-weight: bold;
        }}
        </style>
        """, unsafe_allow_html=True)

        if st.button(
            button_text,
            key="analyze_all_seller_documents_btn",
            help="Process all seller documents" if not button_disabled else "All documents processed" if all_processed else "Processing in progress...",
            type="secondary",
            disabled=button_disabled,
            use_container_width=True
        ):
            if not seller_state.seller_enterprise_name:
                st.error("❌ Please enter the Seller Enterprise Name first")
                logger.warning("Analyze all clicked without seller enterprise name")
            else:
                seller_state.update_field('processing_all_seller_documents', True)
                logger.info("Started processing all seller documents")
                st.rerun()

    except Exception as e:
        logger.error(f"Error rendering process all button: {str(e)}", exc_info=True)


def _process_all_documents(seller_state: SellerTabState, seller_documents_upload):
    """Process all uploaded documents."""
    try:
        logger.info(f"Processing {len(seller_documents_upload)} documents")
        st.markdown("**🔍 Processing all documents and extracting services...**")

        processed_count = 0
        total_files = len(seller_documents_upload)

        for idx, uploaded_file in enumerate(seller_documents_upload):
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            progress_text = f"Processing {uploaded_file.name} ({idx + 1}/{total_files})..."

            with st.spinner(progress_text):
                try:
                    file_path = save_uploaded_file_and_get_path(uploaded_file)
                    seller_state.seller_uploaded_files_paths[file_key] = file_path

                    if file_path and seller_state.seller_enterprise_name:
                        services = get_seller_services(file_path, seller_state.seller_enterprise_name)
                        seller_state.add_processed_file(file_key, uploaded_file.name, services, file_path)
                        st.success(f"✅ {uploaded_file.name} processed successfully!")
                        logger.info(f"Successfully processed: {uploaded_file.name}")
                        processed_count += 1
                    else:
                        st.error(f"❌ Error saving {uploaded_file.name}")
                        logger.error(f"File path invalid for {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    logger.error(f"Error processing file {uploaded_file.name}: {str(e)}", exc_info=True)

        seller_state.update_field('processing_all_seller_documents', False)

        if processed_count == total_files:
            st.success(f"🎉 All {total_files} documents processed successfully!")
        elif processed_count > 0:
            st.warning(f"⚠️ {processed_count} out of {total_files} documents processed.")
        else:
            st.error("❌ No documents could be processed.")

        logger.info(f"Document processing completed: {processed_count}/{total_files}")
        st.rerun()

    except Exception as e:
        seller_state.update_field('processing_all_seller_documents', False)
        logger.error(f"Error processing documents: {str(e)}", exc_info=True)
        st.error("Error occurred while processing documents")
def _render_enterprise_details_section(seller_state: SellerTabState):
    """Render the enterprise details section."""
    try:
        logger.debug("Rendering enterprise details section")

        seller_enterprise_details, provided = render_three_column_selector_unified(
            column_ratio=(2, 2, 2),
            column_gap="large",
            
            left_title="Seller Services to be provided",
            left_tooltip="Define your enterprise details, services offered, company capabilities, core competencies, and business portfolio. This information helps clients understand your organizational strengths and service offerings.",
            left_required=True,
            textarea_height=200,
            textarea_placeholder="Click to get the AI suggested Enterprise services",
            textarea_session_key="seller_enterprise_content",
            textarea_widget_key="seller_enterprise_textarea",
            
            unified_section_title="Available Services",
            unified_section_tooltip="Select from available services and capabilities that represent your enterprise offerings. These can include technical services, consulting, products, or specialized business solutions.",
            
            middle_selected_items_key="selected_services_offered",
            middle_content_map_key="services_content_map",
            right_selected_items_key="selected_additional_capabilities",
            right_content_map_key="capabilities_content_map",

            default_data=None,
            split_ratio=(3, 3),

            client_enabled_condition=True,
            client_name_provided=bool(seller_state.seller_enterprise_name),

            button_column_width=2.5,
            content_column_width=6.5,
            show_success_messages=False,
            text_color="#0000000",
            title_font_size="18px",
            title_color="#000000",
            title_margin_bottom="10px",
            selected_color="#d2ebfb"
        )

        # Update state
        if seller_enterprise_details != seller_state.seller_enterprise_details_content:
            seller_state.update_field("seller_enterprise_details_content", seller_enterprise_details)

        logger.debug("Enterprise details section rendered successfully")

    except Exception as e:
        logger.error(f"Error rendering enterprise details section: {str(e)}", exc_info=True)
        st.error("Error loading enterprise details section")
    
