import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import time
from Client.client import client_tab, validate_client_mandatory_fields
from Seller.seller import seller_tab
from ProjectSpecification_tab.project_spec import proj_specification_tab
from Proposal_writing_tab.proposal_generator import generate_tab
from Client.client_dataclass import ClientTabState
from Seller.seller import SellerTabState
import os
from datetime import datetime
import logging
import uuid
import random
from main_css import add_professional_css,app_css,button_css,button_css_2,content_area_css,css_styles,header_css,sticky_header_css

from dotenv import load_dotenv
load_dotenv()
from config import load_env_variables
load_env_variables()

import time
from datetime import datetime, timedelta
from Common_Utils.common_utils import set_global_message


def app():

    def generate_session_id():
        """Generate a unique session ID for the user"""
        return str(uuid.uuid4())

    def get_or_set_session_cookie():
        """Persist session_id using browser cookie across refreshes."""
        # Try to read the session_id from cookie
        if "session_id" in st.session_state:
            return st.session_state.session_id

        # Streamlit's way to access cookies via experimental API
        if "session_cookie" in st.experimental_get_query_params():
            session_id = st.experimental_get_query_params()["session_cookie"][0]
        else:
            # If not found, generate a new one
            session_id = str(uuid.uuid4())
            st.experimental_set_query_params(session_cookie=session_id)

        st.session_state.session_id = session_id
        return session_id

    def setup_logging():
        """Setup logging configuration for client module with session-based logging."""
        try:
            # Initialize session ID if not exists
            if 'session_id' not in st.session_state:
                st.session_state.session_id = get_or_set_session_cookie()

            # Check if logger is already initialized
            if 'logger_initialized' in st.session_state and st.session_state.logger_initialized:
                return logging.getLogger('client_module')

            logs_dir = "logs"
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)

            # Check if log filename already exists in session
            if 'log_filename' not in st.session_state:
                st.session_state.log_filename = f'client_logs_session_{st.session_state.session_id}.log'

            log_filepath = os.path.join(logs_dir, st.session_state.log_filename)

            # Configure logger
            logger = logging.getLogger('client_module')
            logger.setLevel(logging.DEBUG)

            # Remove existing handlers to avoid duplicates
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Only create file handler if file doesn't already exist
            if not os.path.exists(log_filepath):
                open(log_filepath, 'a').close()  # Create empty file if needed

            file_handler = logging.FileHandler(log_filepath)
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                f'%(asctime)s - %(name)s - %(levelname)s - Session:{st.session_state.session_id} - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            st.session_state.logger_initialized = True
            logger.info(f"New session started with ID: {st.session_state.session_id}")

            return logger

        except Exception as e:
            st.error(f"Error setting up logging: {str(e)}")
            return logging.getLogger('client_module')

    # Initialize session state variables
    if 'client_data_from_tab' not in st.session_state:
        st.session_state.client_data_from_tab = None

    if 'seller_data_from_tab' not in st.session_state:
        st.session_state.seller_data_from_tab = None

    if 'project_specs_from_tab' not in st.session_state:
        st.session_state.project_specs_from_tab = None

    # Initialize locked tabs state
    if 'locked_tabs' not in st.session_state:
        st.session_state.locked_tabs = set()

    # Initialize highest reached tab
    if 'highest_reached_tab' not in st.session_state:
        st.session_state.highest_reached_tab = 0

    def get_sample_extracted_text():
        return """Key Requirements Extracted:

    • Project Type: Enterprise Software Development
    • Timeline: 6-8 months
    • Budget Range: $150,000 - $200,000
    • Team Size: 5-7 developers
    • Technologies: React, Node.js, PostgreSQL
    • Deployment: AWS Cloud Infrastructure
    • Security: SOC 2 compliance required
    • Integration: Salesforce, HubSpot APIs
    • Support: 24/7 monitoring and maintenance

    Additional Notes:
    - Client prefers agile methodology
    - Weekly progress reports required
    - UAT phase: 4 weeks
    - Go-live date: Q3 2024"""

    # @st.dialog("⚠️ Validation Error")
    def show_validation_popup(missing_tab_name, missing_fields=None):
        """Show validation error popup using st.dialog"""
        set_global_message("Please fill all the necessary field first")
        
        # st.error(f"Please complete all mandatory fields in the **{missing_tab_name}** tab first!")
        
        # if missing_fields:
        #     st.warning(f"**Missing Required Fields:** {missing_fields}")
        
        # # Single OK button
        # if st.button("Got it!", key=f"validation_ok_{missing_tab_name.replace(' ', '_')}", use_container_width=True, type="primary"):
        #     # Clear validation popup state and rerun
        #     st.rerun()

    def trigger_validation_popup(missing_tab_name, missing_fields=None):
        """Trigger validation popup by setting session state"""
        validation_key = f"show_validation_popup_{missing_tab_name.replace(' ', '_')}"
        st.session_state[validation_key] = {
            'tab_name': missing_tab_name,
            'missing_fields': missing_fields
        }
        st.rerun()

    def handle_validation_popups():
        """Handle validation popups display - call this at the top of your main app"""
        tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
        
        for tab_name in tab_names:
            validation_key = f"show_validation_popup_{tab_name.replace(' ', '_')}"
            if validation_key in st.session_state and st.session_state[validation_key]:
                popup_data = st.session_state[validation_key]
                # Clear the validation state before showing popup
                del st.session_state[validation_key]
                # Show the popup
                show_validation_popup(popup_data['tab_name'], popup_data.get('missing_fields'))
                break  # Only show one popup at a time

    def refresh_all_data():
        """Clear all session state and form data"""
        # Get current session ID and logger status before clearing
        current_session_id = st.session_state.get('session_id', None)
        logger_initialized = st.session_state.get('logger_initialized', False)
        
        # Clear all session state variables
        for key in list(st.session_state.keys()):
            if key in st.session_state:
                del st.session_state[key]
        
        # Clear locked tabs and reset navigation
        st.session_state.locked_tabs = set()
        st.session_state.highest_reached_tab = 0
        st.session_state.active_tab = 0
        
        # Clear confirmation states
        confirmation_keys = [key for key in st.session_state.keys() if key.startswith('show_confirmation_')]
        for key in confirmation_keys:
            del st.session_state[key]
        
        # Clear any other dynamic keys (role and priority related)
        keys_to_remove = []
        for key in st.session_state.keys():
            if (key.startswith('role_edit_input_') or 
                key.startswith('remove_role_btn_') or 
                key.startswith('priority_checkbox_')):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Preserve session ID and logger status
        if current_session_id:
            st.session_state.session_id = current_session_id
            st.session_state.logger_initialized = logger_initialized
        
        st.success("All data has been cleared!")
        st.rerun()

    def validate_seller_mandatory_fields():
        """Validate seller mandatory fields"""
        seller = st.session_state.seller_data_from_tab

        # Ensure both fields are non-empty after stripping whitespace
        return seller is not None and bool(seller.seller_enterprise_name.strip()) and bool(seller.seller_requirements_content.strip())

    def validate_project_mandatory_fields():
        """Validate project specification mandatory fields"""
        # Add your project validation logic here
        # For now, returning True as placeholder
        return True

    def get_validation_function(tab_index):
        """Get validation function for a specific tab"""
        if tab_index == 0:
            return validate_client_mandatory_fields
        elif tab_index == 1:
            return validate_seller_mandatory_fields
        elif tab_index == 2:
            return validate_project_mandatory_fields
        else:
            return lambda: True

    def is_tab_accessible(tab_index):
        """Check if a tab is accessible - allow backward navigation to visited tabs"""
        current_tab = st.session_state.active_tab
        
        # Always allow access to tab 0 (Client Information)
        if tab_index == 0:
            return True
        
        # Allow backward navigation to any tab that's been reached before
        highest_reached = st.session_state.get('highest_reached_tab', 0)
        if tab_index <= highest_reached:
            return True
        
        # For forward navigation, check validation requirements
        if tab_index == 1:
            return validate_client_mandatory_fields()
        elif tab_index == 2:
            return validate_client_mandatory_fields() and validate_seller_mandatory_fields()
        elif tab_index == 3:
            return (validate_client_mandatory_fields() and 
                    validate_seller_mandatory_fields() and 
                    validate_project_mandatory_fields())
        
        return False

    def should_show_lock_confirmation(target_tab_index):
        """Determine if lock confirmation should be shown"""
        current_tab = st.session_state.active_tab
        
        # Only show confirmation for forward navigation
        if target_tab_index <= current_tab:
            return False
        
        # Don't show confirmation if current tab is already locked
        if current_tab in st.session_state.locked_tabs:
            return False
        
        # Don't show confirmation for the last tab
        if current_tab >= 3:
            return False
        
        # Check if current tab has required data filled
        validation_func = get_validation_function(current_tab)
        if not validation_func():
            return False
        
        return True

    def navigate_to_tab(target_tab_index):
        """Navigate to a specific tab with proper validation"""
        current_tab = st.session_state.active_tab
        
        # If clicking on the same tab, do nothing
        if target_tab_index == current_tab:
            return
        
        # Check if tab is accessible
        if not is_tab_accessible(target_tab_index):
            # Show validation error for the blocking requirement
            if target_tab_index == 1 and not validate_client_mandatory_fields():
                trigger_validation_popup("Client Information", "Please fill all required client fields")
                return
            elif target_tab_index == 2:
                if not validate_client_mandatory_fields():
                    trigger_validation_popup("Client Information", "Please fill all required client fields")
                    return
                elif not validate_seller_mandatory_fields():
                    trigger_validation_popup("Seller Information", "Please fill all required seller fields")
                    return
            elif target_tab_index == 3:
                if not validate_client_mandatory_fields():
                    trigger_validation_popup("Client Information", "Please fill all required client fields")
                    return
                elif not validate_seller_mandatory_fields():
                    trigger_validation_popup("Seller Information", "Please fill all required seller fields")
                    return
                elif not validate_project_mandatory_fields():
                    trigger_validation_popup("Project Specifications", "Please fill all required project fields")
                    return
        
        # For backward navigation, just navigate
        if target_tab_index < current_tab:
            st.session_state.active_tab = target_tab_index
            st.rerun()
            return
        
        # For forward navigation, check if we need lock confirmation
        if should_show_lock_confirmation(target_tab_index):
            confirmation_key = f"show_confirmation_{current_tab}"
            st.session_state[confirmation_key] = True
            st.session_state['target_tab_after_lock'] = target_tab_index
            st.rerun()
            return
        
        # Direct navigation (no confirmation needed)
        st.session_state.active_tab = target_tab_index
        st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, target_tab_index)
        st.rerun()

    @st.dialog("‼️ Confirm Tab Lock")
    def show_lock_confirmation_popup(tab_index):
        """Show confirmation dialog for locking a tab using st.dialog"""
        
        tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
        
        # Warning message
        st.error(
            f"Lock **{tab_names[tab_index] if tab_index < len(tab_names) else f'Tab {tab_index + 1}'}** ?\n\n"
            f"You won't be able to modify this tab once locked."
        )
        
        # Two buttons layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Back", key=f"cancel_lock_{tab_index}", type="secondary", use_container_width=True):
                # Clear all confirmation states
                confirmation_key = f"show_confirmation_{tab_index}"
                if confirmation_key in st.session_state:
                    del st.session_state[confirmation_key]
                if 'target_tab_after_lock' in st.session_state:
                    del st.session_state['target_tab_after_lock']
                st.rerun()
        
        with col2:
            if st.button("Lock & Continue", key=f"confirm_lock_{tab_index}", type="secondary", use_container_width=True):
                # Initialize locked_tabs if it doesn't exist
                if 'locked_tabs' not in st.session_state:
                    st.session_state.locked_tabs = set()
                
                # Lock the current tab
                st.session_state.locked_tabs.add(tab_index)
                
                # Get target tab
                target_tab = st.session_state.get('target_tab_after_lock', tab_index + 1)
                
                # Clear all confirmation states FIRST
                confirmation_key = f"show_confirmation_{tab_index}"
                if confirmation_key in st.session_state:
                    del st.session_state[confirmation_key]
                if 'target_tab_after_lock' in st.session_state:
                    del st.session_state['target_tab_after_lock']
                
                # Set navigation states
                st.session_state.active_tab = target_tab
                st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, target_tab)
                
                # Force close dialog and navigate
                st.rerun()

    # Updated navigation button functions
    def navigate_to_next_tab():
        """Navigate to the next tab with validation and locking"""
        current_tab = st.session_state.active_tab
        
        if current_tab >= 3:  # Already on last tab
            return
        
        navigate_to_tab(current_tab + 1)

    def navigate_to_previous_tab():
        """Navigate to the previous tab - always allowed"""
        current_tab = st.session_state.active_tab
        
        if current_tab > 0:
            st.session_state.active_tab = current_tab - 1
            st.rerun()

    def get_button_text(direction, current_tab):
        """Get button text with tab names"""
        tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
        
        if direction == "next":
            if current_tab < 3:
                return f"Next: {tab_names[current_tab + 1]} ➡️"
            else:
                return "Next ➡️"
        else:  # previous
            if current_tab > 0:
                return f"⬅️ Previous: {tab_names[current_tab - 1]}"
            else:
                return "⬅️ Previous"

    def is_tab_locked(tab_index):
        """Check if a tab is locked"""
        return tab_index in st.session_state.locked_tabs

    # NOTE: Add this line at the very top of your main script (before any other Streamlit commands):


    # Initialize session ID and logger at the very beginning
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_session_id()

    if 'logger_initialized' not in st.session_state:
        st.session_state.logger_initialized = False

    # Setup logging once at the beginning
    logger = setup_logging()
            

    st.markdown(app_css, unsafe_allow_html=True)
    st.markdown(content_area_css, unsafe_allow_html=True)
    st.markdown(sticky_header_css, unsafe_allow_html=True)

    # Add title - place this after your CSS but before the tab buttons
    st.markdown(header_css, unsafe_allow_html=True)
    st.markdown(button_css_2, unsafe_allow_html=True)
    st.markdown(button_css, unsafe_allow_html=True)

    # Initialize session state for active tab - ENSURE CLIENT TAB IS DEFAULT
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0

    # Handle validation popups FIRST - before any other UI elements
    handle_validation_popups()

    current_tab = st.session_state.active_tab
    confirmation_key = f"show_confirmation_{current_tab}"

    if confirmation_key in st.session_state and st.session_state[confirmation_key]:
        show_lock_confirmation_popup(current_tab)

    tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

    # Create tab buttons with stylable containers for #e3e6e5 active state
    cols = st.columns(4, gap="large")

    for i, tab_name in enumerate(tab_names):
        with cols[i]:
            is_active = (i == st.session_state.active_tab)
            
            # Determine if tab should be clickable based on accessibility
            tab_enabled = is_tab_accessible(i)
            
            # Add lock indicator to tab name if locked
            display_name = tab_name
            if is_tab_locked(i):
                display_name = f"🔒 {tab_name}"
            
            # Use stylable_container to make active tab #599cd4
            if is_active and tab_enabled:
                with stylable_container(
                    f"active_tab_{i}",
                    css_styles="""
                    button {
                        background-color: #599cd4 !important;
                        color: white !important;
                        border: 2px solid #ececec !important;
                        font-weight: bold !important;
                        box-shadow: 0 4px 8px rgba(89, 156, 212, 0.3) !important;
                    }
                    button:focus {
                        background-color: #599cd4 !important;
                        color: blue !important;
                        outline: none !important;
                    }
                    """,
                ):
                    if st.button(display_name, key=f"tab_{i}", use_container_width=True, type="primary"):
                        navigate_to_tab(i)
            elif tab_enabled:
                with stylable_container(
                    f"inactive_tab_{i}",
                    css_styles="""
                    button {
                        background-color: #6c757d !important;
                        color: white !important;
                        border: 1px solid #ececec !important;
                    }
                    """,
                ):
                    if st.button(display_name, key=f"tab_{i}", use_container_width=True, type="primary"):
                        navigate_to_tab(i)
            else:
                # Disabled tabs with no hover effects
                with stylable_container(
                    f"disabled_tab_{i}",
                    css_styles="""
                    button {
                        background-color: #6c757d !important;
                        color: white !important;
                        border: 1px solid #ececec !important;
                        cursor: not-allowed !important;
                        opacity: 1 !important;
                    }
                    """,
                ):
                    st.button(display_name, key=f"tab_{i}", use_container_width=True, disabled=True, type="primary")

    # Set is_active flag for current tab
    st.session_state.is_active = True

    # Show lock status message for locked tabs
    if is_tab_locked(current_tab):
        st.info(f"🔒 This tab is locked. You cannot modify the data in this tab.")

    # Content area with validation-aware tab switching
    if st.session_state.active_tab == 0:
        # Pass locked status to the tab
        st.session_state.client_data_from_tab = client_tab(st, logger, is_locked=is_tab_locked(0))

    elif st.session_state.active_tab == 1:
        # Double-check validation before showing seller tab
        if validate_client_mandatory_fields():
            st.session_state.seller_data_from_tab = seller_tab(is_locked=is_tab_locked(1))
        else:
            st.session_state.active_tab = 0  # Force back to client tab
            trigger_validation_popup("Client Information", "Please complete all required client fields")
            st.rerun()

    elif st.session_state.active_tab == 2:
        # Check both client and seller validations
        if not validate_client_mandatory_fields():
            st.session_state.active_tab = 0
            trigger_validation_popup("Client Information", "Please complete all required client fields")
            st.rerun()
        elif not validate_seller_mandatory_fields():
            st.session_state.active_tab = 1
            trigger_validation_popup("Seller Information", "Please complete all required seller fields")
            st.rerun()
        else:
            # Only call proj_specification_tab if no confirmation dialog is active
            confirmation_active = any(key.startswith('show_confirmation_') and st.session_state.get(key, False) 
                                    for key in st.session_state.keys())
            if not confirmation_active:
                st.session_state.project_specs_from_tab = proj_specification_tab(
                    st.session_state.client_data_from_tab, 
                    st.session_state.seller_data_from_tab,
                    is_locked=is_tab_locked(2)
                )

    else:  # Generate Proposal Tab
        # Check all validations
        if not validate_client_mandatory_fields():
            st.session_state.active_tab = 0
            trigger_validation_popup("Client Information", "Please complete all required client fields")
            st.rerun()
        elif not validate_seller_mandatory_fields():
            st.session_state.active_tab = 1
            trigger_validation_popup("Seller Information", "Please complete all required seller fields")
            st.rerun()
        elif not validate_project_mandatory_fields():
            st.session_state.active_tab = 2
            trigger_validation_popup("Project Specifications", "Please complete all required project fields")
            st.rerun()
        else:
            generate_tab(
                st.session_state.client_data_from_tab,
                st.session_state.seller_data_from_tab,
                st.session_state.project_specs_from_tab
            )

    # Bottom navigation buttons with enhanced styling
    col1, col2, col3 = st.columns(3, gap="medium")

    # Previous Button
    with col1:
        is_first_tab = (st.session_state.active_tab == 0)
        prev_button_text = get_button_text("previous", st.session_state.active_tab)
        
        if is_first_tab:
            with stylable_container(
                "prev_button_disabled",
                css_styles="""
                button {
                    background-color: #6c757d !important;
                    color: black !important;
                    border: 1px solid #dee2e6 !important;
                    cursor: not-allowed !important;
                    opacity: 0.6 !important;
                    font-weight: bold !important;
                }
                """,
            ):
                st.button(prev_button_text, key="prev_btn", use_container_width=True, disabled=True, type="primary")
        else:
            with stylable_container(
                "prev_button",
                css_styles="""
                button {
                    background-color:#6c757d !important;
                    color: black !important;
                    border: 1px solid #5a6268 !important;
                    font-weight: bold !important;
                    transition: all 0.3s ease !important;
                }
                button:hover {
                    background-color: #6c757d !important;
                    color: black !important;
                    transform: translateY(-1px) !important;
                }
                button:active {
                    background-color: #6c757dc !important;
                    border: 2px solid #ececec !important;
                    transform: translateY(0px) !important;
                    box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
                }
                """,
            ):
                if st.button(prev_button_text, key="prev_btn", use_container_width=True, type="primary"):
                    navigate_to_previous_tab()

    # Refresh Button
    with col2:
        with stylable_container(
            "refresh_button",
            css_styles="""
            button {
                background-color: #6c757d !important;
                color: black !important;
                border: 1px solid #5a6268 !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            button:hover {
                background-color: #6c757d !important;
                color: black !important;
                transform: translateY(-1px) !important;
            }
            button:active {
                background-color:#6c757d !important;
                border: 2px solid #ececec !important;
                transform: translateY(0px) !important;
                box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
            }
            """,
        ):
            if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True, type="primary"):
                refresh_all_data()

    # Next Button
    with col3:
        is_last_tab = (st.session_state.active_tab == 3)
        next_button_text = get_button_text("next", st.session_state.active_tab)
        
        if is_last_tab:
            with stylable_container(
                "next_button_disabled",
                css_styles="""
                button {
                    background-color:#6c757d !important;
                    color: black !important;
                    border: 1px solid #dee2e6 !important;
                    cursor: not-allowed !important;
                    opacity: 0.6 !important;
                    font-weight: bold !important;
                }
                """,
            ):
                st.button(next_button_text, key="next_btn", use_container_width=True, disabled=True, type="primary")
        else:
            with stylable_container(
                "next_button",
                css_styles="""
                button {
                    background-color: #6c757d!important;
                    color: black !important;
                    border: 1px solid #5a6268 !important;
                    font-weight: bold !important;
                    transition: all 0.3s ease !important;
                }
                button:active {
                    background-color: #6c757d !important;
                    border: 2px solid #ececec !important;
                    transform: translateY(0px) !important;
                    box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
                }
                """,
            ):
                if st.button(next_button_text, key="next_btn", use_container_width=True, type="primary"):
                    navigate_to_next_tab()