from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import streamlit as st
import logging
from Seller.seller_css import *
from Seller.seller_utils import *
from Search.Linkedin.linkedin_serp import *
from Recommendation.recommendation_utils import *
from Common_Utils.ai_suggestion_utils import *
from WebScraper.webscraper_without_ai import get_url_details_without_ai
from Common_Utils.common_utils import *
from Common_Utils.common_utils import set_global_message

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
            set_global_message("Failed to save seller state. Please try again.", "error")
    
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
            set_global_message("Failed to load seller state. Using default values.", "error")
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
                set_global_message(f"Invalid field update attempted: {field_name}", "error")
        except Exception as e:
            logger.error(f"Error updating field {field_name}: {str(e)}")
            set_global_message(f"Failed to update field {field_name}. Please try again.", "error")
    
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
            set_global_message("Failed to clear URL data. Please refresh the page.", "error")
    
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
            set_global_message("Failed to reset processing states. Please refresh the page.", "error")
    
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
            set_global_message(f"Failed to process file {filename}. Please try again.", "error")
    
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


def seller_tab(is_locked):
    """Main seller tab function with proper state synchronization."""
    try:
        # Add CSS
        
        st.markdown(button_css, unsafe_allow_html=True)
        st.markdown(content_area_css, unsafe_allow_html=True)
        st.markdown(seller_css, unsafe_allow_html=True)

        logger.info("Starting seller_tab function")
        
        # Load or create seller state
        seller_state = SellerTabState.from_session_state()
        
        # KEY FIX: Check if seller name is provided to determine field enablement
        seller_name_provided = bool(seller_state.seller_enterprise_name and seller_state.seller_enterprise_name.strip())
        fields_locked = is_locked or not seller_name_provided
        
        # Render main UI components without fragments for proper synchronization
        _render_top_section(seller_state, is_locked, seller_name_provided)
        _render_document_upload_section(seller_state, fields_locked)
        _render_enterprise_details_section(seller_state, fields_locked)
        
        logger.info("Seller tab rendered successfully")
        
    except Exception as e:
        logger.error(f"Critical error in seller_tab: {str(e)}", exc_info=True)
        set_global_message("An error occurred while loading the seller tab. Please refresh the page and try again.", "error")
    
    return seller_state

@st.fragment
def _render_top_section(seller_state: SellerTabState, is_locked: bool, seller_name_provided: bool):
    """Render the top section with seller name and URL inputs."""
    try:
        logger.debug("Rendering top section")
        
        # Top section with seller name and URLs
        col1, col2 = st.columns([1, 1])
        
        with col1:
            _render_seller_name_input(seller_state, is_locked)
        
        with col2:
            _render_website_url_section(seller_state, is_locked, seller_name_provided)
            
        logger.debug("Top section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering top section: {str(e)}", exc_info=True)
        set_global_message("An error occurred while loading the seller information section. Please try again.", "error")



def _render_seller_name_input(seller_state: SellerTabState, is_locked: bool):
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
            # Remove the on_change callback that was causing reruns
            seller_enterprise_name = st.text_input(
                label="Seller Enterprise Name", 
                placeholder="Enter seller enterprise name...", 
                value=seller_state.seller_enterprise_name,
                key="seller_enterprise_name_input",
                label_visibility="collapsed",
                disabled=is_locked
                # REMOVED: on_change callback that was causing reruns
            )
            
            # Update state if changed (only if not locked) - NO RERUN
            if not is_locked and seller_enterprise_name != seller_state.seller_enterprise_name:
                seller_state.update_field('seller_enterprise_name', seller_enterprise_name)
                # REMOVED: st.rerun() call that was causing screen flash
        
        with button_col:
            _handle_find_urls_button(seller_state, seller_enterprise_name, is_locked)
        
        # Common area for spinner/status
        _display_url_search_status(seller_state, seller_enterprise_name)
        
        # Clear URLs if company name is cleared
        _handle_company_name_changes(seller_state, seller_enterprise_name)
        
        # Show validation warning if triggered and field is empty
        if seller_state.show_validation and check_field_validation("Seller Enterprise Name", seller_enterprise_name, True):
            show_field_warning("Seller Enterprise Name")
            
        logger.debug("Seller name input rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering seller name input: {str(e)}", exc_info=True)
        set_global_message("An error occurred while loading the seller name input. Please try again.", "error")



 
def _handle_find_urls_button(seller_state: SellerTabState, seller_enterprise_name: str, is_locked: bool):
    """Handle find URLs button functionality."""
    try:
        find_urls_disabled = is_locked or not (seller_enterprise_name and len(seller_enterprise_name.strip()) > 2)
        
        if st.button("🔍 Find Website",
                    disabled=find_urls_disabled or seller_state.url_search_in_progress,
                    help="Find website URLs for this company",
                    key="find_seller_urls_button"):
            
            if not is_locked:
                logger.info(f"Finding URLs for company: {seller_enterprise_name.strip()}")
                
                seller_state.update_field('url_search_in_progress', True)
                seller_state.update_field('url_search_company', seller_enterprise_name.strip())
                # Keep this rerun as it's needed for the URL search functionality
                st.rerun()
                    
    except Exception as e:
        logger.error(f"Error in find URLs button handler: {str(e)}", exc_info=True)
        set_global_message("An error occurred with the URL search functionality. Please try again.", "error")

def _handle_company_name_changes(seller_state: SellerTabState, seller_enterprise_name: str):
    """Handle changes in company name and clear URLs if needed."""
    try:
        if not seller_enterprise_name and seller_state.last_seller_company_name:
            seller_state.clear_url_data()
            logger.debug("Cleared URLs due to empty company name")
            
    except Exception as e:
        logger.error(f"Error handling company name changes: {str(e)}", exc_info=True)
        set_global_message("Failed to handle company name changes. Please refresh the page.", "error")


def _display_url_search_status(seller_state: SellerTabState, seller_enterprise_name: str):
    """Display URL search status."""
    try:
        if seller_state.url_search_in_progress:
            search_company = seller_state.url_search_company or seller_enterprise_name
            
            with st.spinner(f"🔍 Finding websites for '{search_company}'..."):
                try:
                    urls_list = get_urls_list(search_company)
                    seller_state.update_field('seller_website_urls_list', urls_list)
                    seller_state.update_field('last_seller_company_name', search_company)
                    
                    seller_state.update_field('url_search_in_progress', False)
                    seller_state.update_field('url_search_company', '')
                    
                    logger.info(f"Successfully found {len(urls_list)} URLs for {search_company}")
                    
                    if urls_list:
                        set_global_message(f"✅ Found {len(urls_list)} website(s) for {search_company}","success")
                    else:
                        set_global_message(f"⚠️ No websites found for {search_company}","error")
                    

                    
                except Exception as e:
                    logger.error(f"Error finding URLs for {search_company}: {str(e)}", exc_info=True)
                    seller_state.update_field('seller_website_urls_list', [])
                    seller_state.update_field('url_search_in_progress', False)
                    seller_state.update_field('url_search_company', '')
                    set_global_message("An error occurred while finding website URLs. Please try again.", "error")
            
    except Exception as e:
        logger.error(f"Error displaying URL search status: {str(e)}", exc_info=True)
        set_global_message("An error occurred while displaying URL search status. Please try again.", "error")


def _render_website_url_section(seller_state: SellerTabState, is_locked: bool, seller_name_provided: bool):
    """Render website URL selection and action buttons."""
    try:
        logger.debug("Rendering website URL section")
        
        st.markdown('''
        <div class="tooltip-label" style="display: flex; align-items: center; gap: 8px;">
            <span>Seller Website URL</span>
            <div class="tooltip-icon" data-tooltip="Enter or select the seller's official website URL. The system will automatically analyze the website to extract company information, services, and business details to help understand the seller's capabilities and offerings.">ⓘ</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Create columns for dropdown and buttons
        url_col, btn1_col, btn2_col = st.columns([7, 1, 2])
        
        with url_col:
            seller_website_url = _render_url_dropdown(seller_state, is_locked, seller_name_provided)
        
        with btn1_col:
            _render_refresh_urls_button(seller_state, is_locked, seller_name_provided)
        with btn2_col:
            _render_scrape_website_button(seller_state, seller_website_url, is_locked, seller_name_provided)
        
        # Show redirect link when website is selected
        if seller_website_url:
            st.markdown(
                f'<div style="text-align: left; margin-top: -7px;">'
                f'🌐 <a href="{seller_website_url}" target="_blank" style="color: #0066cc; text-decoration: none; font-size: 17px;">Visit Website</a>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Handle pending scraping operation
        _handle_pending_scraping(seller_state)
        
        # Show validation warning if needed
        if seller_state.show_validation and check_field_validation("Seller Website URL", seller_website_url, False):
            show_field_warning("Seller Website URL")
            
        logger.debug("Website URL section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering website URL section: {str(e)}", exc_info=True)
        set_global_message("An error occurred while loading the website URL section. Please try again.", "error")


def _render_url_dropdown(seller_state: SellerTabState, is_locked: bool, seller_name_provided: bool):
    """Render URL dropdown selection."""
    try:
        if not seller_state.seller_website_urls_list:
            url_options = ["Select seller website URL"]
        else:
            url_options = ["Select seller website URL"] + seller_state.seller_website_urls_list
        
        initial_index = 0
        if seller_state.seller_website_url and seller_state.seller_website_url in url_options:
            initial_index = url_options.index(seller_state.seller_website_url)
        
        seller_website_url = st.selectbox(
            label="Seller Website URL",
            options=url_options,
            index=initial_index,
            label_visibility="collapsed",
            disabled=is_locked or not seller_name_provided,
            accept_new_options=not is_locked and seller_name_provided
        )
        
        if seller_website_url == "Select seller website URL":
            seller_website_url = ""
        
        # Update state if URL changed
        if not is_locked and seller_website_url != seller_state.seller_website_url:
            seller_state.update_field('seller_website_url', seller_website_url)
            
        return seller_website_url
        
    except Exception as e:
        logger.error(f"Error rendering URL dropdown: {str(e)}", exc_info=True)
        set_global_message("Failed to render URL dropdown. Please try again.", "error")
        return ""


def _render_refresh_urls_button(seller_state: SellerTabState, is_locked: bool, seller_name_provided: bool):
    """Render refresh URLs button."""
    try:
        refresh_clicked = st.button("🔄", help="Refresh website URLs list", 
                                  key="refresh_seller_urls_btn", use_container_width=True, 
                                  disabled=is_locked or not seller_name_provided)
        
        if refresh_clicked and not is_locked and seller_name_provided:
            _handle_refresh_urls(seller_state)
            
    except Exception as e:
        logger.error(f"Error with refresh URLs button: {str(e)}", exc_info=True)
        set_global_message("An error occurred with the refresh URLs functionality. Please try again.", "error")


def _render_scrape_website_button(seller_state: SellerTabState, seller_website_url: str, is_locked: bool, seller_name_provided: bool):
    """Render scrape website button."""
    try:
        scrape_clicked = st.button("📑 Get Details", help="Get enterprise details", 
                                 key="scrape_seller_website_btn", use_container_width=True,
                                 disabled=is_locked or not seller_website_url or not seller_name_provided)
        
        if scrape_clicked and seller_website_url and not is_locked and seller_name_provided:
            logger.info(f"Initiating website scraping for: {seller_website_url}")
            seller_state.update_field('seller_pending_scrape_url', seller_website_url)
            seller_state.update_field('seller_scraping_in_progress', True)
            st.rerun()
            
    except Exception as e:
        logger.error(f"Error with scrape website button: {str(e)}", exc_info=True)
        set_global_message("An error occurred with the website scraping functionality. Please try again.", "error")


def _handle_refresh_urls(seller_state: SellerTabState):
    """Handle URL refresh functionality."""
    try:
        logger.info(f"Refreshing URLs for: {seller_state.seller_enterprise_name}")
        
        with st.spinner("Refreshing website URLs..."):
            try:
                urls_list = get_urls_list(seller_state.seller_enterprise_name)
                seller_state.update_field('seller_website_urls_list', urls_list)
                set_global_message("Website URLs refreshed!","success")
                
                logger.info(f"Successfully refreshed {len(urls_list)} URLs")
                
            except Exception as e:
                logger.error(f"Error refreshing URLs: {str(e)}", exc_info=True)
                set_global_message("An error occurred while refreshing website URLs. Please try again.", "error")
                
    except Exception as e:
        logger.error(f"Error in refresh URLs handler: {str(e)}", exc_info=True)
        set_global_message("Failed to refresh URLs. Please try again.", "error")


def _handle_pending_scraping(seller_state: SellerTabState):
    """Handle pending website scraping operation."""
    try:
        if seller_state.seller_scraping_in_progress and seller_state.seller_pending_scrape_url:
            scrape_url = seller_state.seller_pending_scrape_url
            logger.info(f"Processing pending scrape for: {scrape_url}")
            
            with st.spinner(f"🔍 Fetching website details from {scrape_url}..."):
                try:
                    scrape_result = get_url_details_without_ai(scrape_url)
                    
                    website_name = scrape_result.name
                    logo_url = scrape_result.logo
                    description = scrape_result.description
                    services = scrape_result.services
                    
                    # Format the website details with description and services in bullet points
                    website_details = f"Company: {website_name}\n\n"
                    
                    if description:
                        website_details += f"Description:\n{description}\n\n"
                    
                    if services:
                        website_details += "Services:\n"
                        for service in services:
                            website_details += f"• {service}\n"
                    
                    
                    seller_state.update_field('seller_enterprise_details_content', website_details)
                    seller_state.update_field('last_analyzed_seller_url', scrape_url)
                    
                    if logo_url:
                        seller_state.update_field('enterprise_logo', logo_url)
                        logger.info(f"Logo found and saved: {logo_url}")
                    
                    seller_state.update_field('seller_scraping_in_progress', False)
                    seller_state.update_field('seller_pending_scrape_url', None)
                    
                    logger.info(f"Successfully scraped website: {scrape_url}")
                    
                    
                except Exception as e:
                    logger.error(f"Error scraping website {scrape_url}: {str(e)}", exc_info=True)
                    seller_state.update_field('seller_scraping_in_progress', False)
                    seller_state.update_field('seller_pending_scrape_url', None)
                    set_global_message("An error occurred while scraping website details. Please try again.", "error")
                    
    except Exception as e:
        logger.error(f"Error handling pending scraping: {str(e)}", exc_info=True)
        set_global_message("Failed to handle website scraping. Please try again.", "error")



@st.fragment
def _render_document_upload_section(seller_state: SellerTabState, is_locked: bool):
    """Render document upload section with comprehensive error handling."""
    try:
        logger.debug("Rendering document upload section")
        
        # Add custom CSS
        _add_document_upload_css()
        
        # Create two columns - left for upload, right for scraped data
        upload_col, data_col = st.columns([1, 1])
        
        with upload_col:
            st.markdown('''
            <div class="tooltip-label">
                Upload Seller Documents
                <div class="tooltip-icon" data-tooltip="Upload seller-related documents such as company profiles, service catalogs, capabilities documents, or proposals in PDF, DOCX, TXT, or CSV format. The system will automatically analyze and extract key capabilities, services, and business strengths to help understand the seller's offerings.">ⓘ</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # FILE UPLOAD - disable when locked
            
            seller_documents_upload = st.file_uploader(
                label="Upload Seller Documents", 
                type=['pdf', 'docx', 'txt', 'csv', 'png', 'jpg', 'jpeg'], 
                key="seller_documents_uploader",
                label_visibility="collapsed",
                accept_multiple_files=True
            )
            
            if seller_documents_upload and len(seller_documents_upload) > 0:
                _handle_uploaded_documents(seller_state, seller_documents_upload, is_locked)

        
        with data_col:
            st.markdown('''
            <div class="tooltip-label">
                Seller Enterprise data
                <div class="tooltip-icon" data-tooltip="This field displays the enterprise details and information extracted from the seller's website when you click the 'Get Details' button. The data includes company information, services, and business details automatically scraped from the provided website URL.">ⓘ</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Display scraped data in a text area
            scraped_data_display = st.text_area(
                label="Scraped Website Data",
                value=seller_state.seller_enterprise_details_content,
                height=200,
                placeholder="Enter or get the Details from the seller enterprise website",
                key="scraped_data_display",
                label_visibility="collapsed",
                disabled=is_locked or not bool(seller_state.seller_enterprise_name and seller_state.seller_enterprise_name.strip())  # ADD is_locked condition
            )
            
            # Show additional info if data is available
            # if seller_state.seller_enterprise_details_content:
            #     if seller_state.last_analyzed_seller_url:
            #         #st.info(f"📊 Data scraped from: {seller_state.last_analyzed_seller_url}")
            #         pass
                
            #     # Add a button to clear the scraped data - disable when locked
            #     if not is_locked and st.button("🗑️ Clear Scraped Data", key="clear_scraped_data_btn", help="Clear the scraped website data"):
            #         seller_state.update_field('seller_enterprise_details_content', '')
            #         seller_state.update_field('last_analyzed_seller_url', None)
            #         seller_state.update_field('enterprise_logo', '')
            #         st.rerun()
                
        logger.debug("Document upload section rendered successfully")
        
    except Exception as e:
        logger.error(f"Error rendering document upload section: {str(e)}", exc_info=True)
        set_global_message("Unable to load document upload section. Please refresh the page and try again.", "error")

def _add_document_upload_css():
    """Add CSS for document upload section."""
    try:
        st.markdown(file_upload_css, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error adding document upload CSS: {str(e)}", exc_info=True)


def _handle_uploaded_documents(seller_state: SellerTabState, seller_documents_upload, is_locked: bool):
    """Handle uploaded documents display and processing."""
    try:
        logger.debug(f"Handling {len(seller_documents_upload)} uploaded documents")
    
        _render_process_all_button(seller_state, seller_documents_upload, is_locked)  # Pass is_locked
        
        # Handle processing when button is clicked (only if not locked)
        if seller_state.processing_all_seller_documents and not is_locked:
            _process_all_documents(seller_state, seller_documents_upload)
            
        logger.debug("Uploaded documents handled successfully")
        
    except Exception as e:
        logger.error(f"Error handling uploaded documents: {str(e)}", exc_info=True)
        set_global_message("Unable to process uploaded documents. Please try uploading again.", "error")

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

def _render_process_all_button(seller_state: SellerTabState, seller_documents_upload, is_locked: bool):
    """Render button to process all documents."""
    try:
        all_processed = all(
            f"{file.name}_{file.size}" in seller_state.seller_services_by_file
            for file in seller_documents_upload
        )
        
        is_processing = seller_state.processing_all_seller_documents
        
        if is_locked:
            button_color = "#6c757d"
            button_text = "🔒 Processing Disabled"
            button_disabled = True
        elif all_processed:
            button_color = "#28a745"
            button_text = "All Documents Processed"
            button_disabled = True
        elif is_processing:
            button_color = "#FF6B6B"
            button_text = "Analyzing All Documents..."
            button_disabled = True
        else:
            button_color = "#4CAF50"
            button_text = f"Process documents"
            button_disabled = False


        if st.button(
            button_text,
            key="analyze_all_seller_documents_btn",
            help="Processing disabled" if is_locked else "Process all seller documents" if not button_disabled else "All documents processed" if all_processed else "Processing in progress...",
            type="secondary",
            disabled=button_disabled,
            use_container_width=True
        ):
            if not is_locked:  # Only proceed if not locked
                if not seller_state.seller_enterprise_name:
                    set_global_message("Please enter the seller enterprise name before processing documents.", "error")
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
                        #st.success(f"✅ {uploaded_file.name} processed successfully!")
                        logger.info(f"Successfully processed: {uploaded_file.name}")
                        processed_count += 1
                    else:
                        set_global_message(f"Unable to save or process {uploaded_file.name}. Please try again.", "error")
                        logger.error(f"File path invalid for {uploaded_file.name}")
                except Exception as e:
                    set_global_message(f"Failed to process {uploaded_file.name}. Please check the file format and try again.", "error")
                    logger.error(f"Error processing file {uploaded_file.name}: {str(e)}", exc_info=True)

        seller_state.update_field('processing_all_seller_documents', False)

        if processed_count == total_files:
            #st.success(f"🎉 All {total_files} documents processed successfully!")
            pass
        elif processed_count > 0:
            st.warning(f"⚠️ {processed_count} out of {total_files} documents processed.")
        else:
            set_global_message("No documents could be processed. Please check your files and try again.", "error")

        logger.info(f"Document processing completed: {processed_count}/{total_files}")


    except Exception as e:
        seller_state.update_field('processing_all_seller_documents', False)
        logger.error(f"Error processing documents: {str(e)}", exc_info=True)
        set_global_message("Document processing failed. Please try again or contact support.", "error")

@st.fragment
def _render_enterprise_details_section(seller_state: SellerTabState, is_locked: bool):
    """Render the enterprise details section."""
    try:
        logger.debug("Rendering enterprise details section")

        seller_requirements_content, provided = render_three_column_selector_unified(
            column_ratio=(2, 2, 2),
            column_gap="small",
            

            left_title="Seller Services to be provided",
            left_tooltip="Define your enterprise details, services offered, company capabilities, core competencies, and business portfolio. This information helps clients understand your organizational strengths and service offerings.",
            left_required=True,
            textarea_height=200,
            textarea_placeholder="Click to get the AI suggested Enterprise services",
            textarea_session_key="seller_requirements_content",  # This should match the field name
            textarea_widget_key="seller_requirements_textarea",
            
            
            unified_section_title="Seller Services",
            unified_section_tooltip="Select from available services and capabilities that represent your enterprise offerings. These can include technical services, consulting, products, or specialized business solutions.",
            
            middle_selected_items_key="selected_services_offered",
            middle_content_map_key="services_content_map",
            right_selected_items_key="selected_additional_capabilities",
            right_content_map_key="capabilities_content_map",

            default_data=None,
            split_ratio=(3, 3),

            client_enabled_condition=not is_locked,
            client_name_provided=bool(seller_state.seller_enterprise_name) and not is_locked,
            button_column_width=2.5,
            content_column_width=6.5,
            show_success_messages=False,
            text_color="#0000000",
            title_font_size="18px",
            title_color="#000000",
            title_margin_bottom="10px",
            selected_color="#d2ebfb",
            unselected_border_color="#ececec"
        )

        # FIXED: Update the correct state field - seller_requirements_content instead of seller_enterprise_details_content
        if not is_locked and seller_requirements_content != seller_state.seller_requirements_content:
            seller_state.update_field("seller_requirements_content", seller_requirements_content)

        logger.debug("Enterprise details section rendered successfully")

    except Exception as e:
        logger.error(f"Error rendering enterprise details section: {str(e)}", exc_info=True)
        set_global_message("Unable to load enterprise details section. Please refresh the page and try again.", "error")