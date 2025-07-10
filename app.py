import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import time
from Client.client import client_tab,validate_client_mandatory_fields
from Seller.seller import seller_tab
from ProjectSpecification.project_spec import proj_specification_tab
from Generate_proposal.proposal_generator import generate_tab
from Client.client_dataclass import ClientData
from Seller.seller import SellerTabState
import os
from datetime import datetime
import logging
import uuid
import random

def generate_session_id():
    """Generate a unique session ID for the user"""
    return str(uuid.uuid4())

import os
import logging
from datetime import datetime
import streamlit as st

def generate_session_id():
    """Placeholder session ID generator."""
    print("---------")
    return datetime.now().strftime('%Y%m%d%H%M%S%f')  # Replace with your actual logic


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
            st.session_state.session_id =get_or_set_session_cookie()

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

def show_validation_popup(missing_tab_name, missing_fields=None):
    """Show validation error popup with professional styling"""
    
    # Create professional popup modal
    with stylable_container(
        f"validation_popup_{missing_tab_name.replace(' ', '_')}",
        css_styles="""
        div[data-testid="stBlock"] {
            position: fixed !important;
            top: 20% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 9999 !important;
            background: white !important;
            border: 1px solid #ddd !important;
            border-radius: 12px !important;
            padding: 30px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
            width: 450px !important;
            max-width: 90vw !important;
            border-top: 4px solid #f56565 !important;
        }
        div[data-testid="stBlock"]:before {
            content: '' !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.4) !important;
            z-index: -1 !important;
        }
        """,
    ):
        # Header with icon and title
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="background: #fed7d7; border-radius: 50%; width: 60px; height: 60px; 
                           display: flex; align-items: center; justify-content: center; 
                           margin: 0 auto 15px auto; border: 2px solid #fc8181;">
                    <span style="font-size: 24px; color: #f56565;">⚠️</span>
                </div>
                <h3 style="color: #2d3748; margin: 0; font-size: 20px; font-weight: 600;">
                    Validation Error
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Error message
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 25px;">
                <p style="font-size: 15px; color: #e53e3e; line-height: 1.6; margin-bottom: 10px; font-weight: 500;">
                    Please complete all mandatory fields in the <strong>"{missing_tab_name}"</strong> tab first!
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Show missing fields if provided
        if missing_fields:
            st.markdown(
                f"""
                <div style="background: #fef5e7; border: 1px solid #f6ad55; border-radius: 8px; 
                           padding: 15px; margin-bottom: 20px;">
                    <p style="font-size: 14px; color: #c05621; margin: 0; font-weight: 500;">
                        <strong>Missing Required Fields:</strong>
                    </p>
                    <p style="font-size: 14px; color: #9c4221; margin: 5px 0 0 0; line-height: 1.4;">
                        {missing_fields}
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Action button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with stylable_container(
                f"validation_ok_btn_{missing_tab_name.replace(' ', '_')}",
                css_styles="""
                button {
                    background-color: #f56565 !important;
                    color: white !important;
                    border: 1px solid #f56565 !important;
                    border-radius: 6px !important;
                    padding: 10px 20px !important;
                    font-weight: 600 !important;
                    width: 100% !important;
                    transition: all 0.2s ease !important;
                    font-size: 15px !important;
                }
                button:hover {
                    background-color: #e53e3e !important;
                    border-color: #e53e3e !important;
                    transform: translateY(-1px) !important;
                    box-shadow: 0 4px 8px rgba(245, 101, 101, 0.3) !important;
                }
                """,
            ):
                if st.button("Got it!", key=f"validation_ok_{missing_tab_name.replace(' ', '_')}"):
                    # Clear validation popup state
                    validation_key = f"show_validation_popup_{missing_tab_name.replace(' ', '_')}"
                    if validation_key in st.session_state:
                        del st.session_state[validation_key]
                    st.rerun()
    
    return True

# Updated function to trigger validation popup
def trigger_validation_popup(missing_tab_name, missing_fields=None):
    """Trigger validation popup by setting session state"""
    validation_key = f"show_validation_popup_{missing_tab_name.replace(' ', '_')}"
    st.session_state[validation_key] = {
        'tab_name': missing_tab_name,
        'missing_fields': missing_fields
    }

# Updated navigation functions that use the new popup system
def navigate_to_next_tab():
    """Navigate to the next tab with validation and locking"""
    current_tab = st.session_state.active_tab
    
    # Get validation function for current tab
    validation_func = get_validation_function(current_tab)
    
    if not validation_func():
        tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
        trigger_validation_popup(tab_names[current_tab])
        return
    
    # If tab is already locked, just navigate
    if current_tab in st.session_state.locked_tabs:
        if current_tab < 3:
            st.session_state.active_tab = current_tab + 1
            st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, st.session_state.active_tab)
            st.rerun()
        return
    
    # If this is the last tab, don't show confirmation
    if current_tab >= 3:
        return
    
    # Show confirmation dialog
    confirmation_key = f"show_confirmation_{current_tab}"
    st.session_state[confirmation_key] = True
    st.rerun()

# Add this to your main app logic, right after the confirmation dialog handling
def handle_validation_popups():
    """Handle validation popups display"""
    tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
    
    for tab_name in tab_names:
        validation_key = f"show_validation_popup_{tab_name.replace(' ', '_')}"
        if validation_key in st.session_state and st.session_state[validation_key]:
            popup_data = st.session_state[validation_key]
            show_validation_popup(popup_data['tab_name'], popup_data.get('missing_fields'))
            st.stop()  # Stop execution to show only the popup

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
    # Add your seller validation logic here
    # For now, returning True as placeholder
    return True

def validate_project_mandatory_fields():
    """Validate project specification mandatory fields"""
    # Add your project validation logic here
    # For now, returning True as placeholder
    return True

def show_validation_popup(missing_tab_name, missing_fields=None):
    """Show validation error popup"""
    toast = st.toast(f"⚠️ Please complete all mandatory fields in {missing_tab_name} tab first!")

    # Inject JavaScript to auto-dismiss the toast after 3 seconds (3000 ms)
    # st.markdown("""
    #     <script>
    #     setTimeout(function() {
    #         let toasts = window.parent.document.querySelectorAll('div[data-testid="stToast"]');
    #         if (toasts.length > 0) {
    #             toasts[0].style.display = 'none';
    #         }
    #     }, 10000);
    #     </script>
    # """, unsafe_allow_html=True)
    if missing_fields:
        st.error(f"Missing required fields: {missing_fields}")

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
    """Check if a tab is accessible based on validation"""
    if tab_index == 0:
        return True
    elif tab_index == 1:
        return validate_client_mandatory_fields()
    elif tab_index == 2:
        return validate_client_mandatory_fields() and validate_seller_mandatory_fields()
    elif tab_index == 3:
        return (validate_client_mandatory_fields() and 
                validate_seller_mandatory_fields() and 
                validate_project_mandatory_fields())
    return False
def show_lock_confirmation_popup(tab_index):
    """Show compact popup-style confirmation dialog for locking a tab"""
    tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
    st.markdown("")
    st.markdown("")
    st.markdown("")
    # Create compact popup modal
    with stylable_container(
        f"confirmation_popup_{tab_index}",
        css_styles="""
        div[data-testid="stBlock"] {
            position: fixed !important;
            top: 75% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 9999 !important;
            background: white !important;
            border: 2px solid #e74c3c !important;
            border-radius: 8px !important;
            padding: 20px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            width: 60px !important;
            height: 180px !important;
            max-width: 90vw !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
        }
        div[data-testid="stBlock"]:before {
            content: '' !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.4) !important;
            z-index: -1 !important;
        }
        """,
    ):
        # Text message
        st.markdown(
    """
    <div style="
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f8f9fa;
        width:40%;
        text-align: center;
        margin: 0 auto;
    ">
        <h4 style="color: #e74c3c; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">
            ⚠️ Confirm Tab Lock
        </h4>
        <p style="font-size: 14px; color: #4a5568; line-height: 1.4; margin: 0 0 15px 0;">
            Lock <strong>tab</strong>?<br>
            <span style="color: #718096; font-size: 13px;">You won't be able to modify this tab once locked.</span>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Action buttons in the same container, positioned right under the box
    col1, col2 = st.columns(2, gap="small")

    with col1:
        with stylable_container(
            f"cancel_btn_{tab_index}",
            css_styles="""
            button {
                background-color: #f7fafc !important;
                color: #4a5568 !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 6px !important;
                padding: 8px 16px !important;
                font-weight: 500 !important;
                width: 40% !important;
                font-size: 14px !important;
                height: 40px !important;
                margin-left: auto !important;
display: block !important;
                
            }
            button:hover {
                background-color: #edf2f7 !important;
                border-color: #cbd5e0 !important;
            }
            """,
        ):
            if st.button("Cancel", key=f"cancel_lock_{tab_index}"):
                # Clear confirmation state
                if f"show_confirmation_{tab_index}" in st.session_state:
                    del st.session_state[f"show_confirmation_{tab_index}"]
                st.rerun()

    with col2:
        with stylable_container(
            f"confirm_btn_{tab_index}",
            css_styles="""
            button {
                background-color: #e74c3c !important;
                color: white !important;
                border: 1px solid #e74c3c !important;
                border-radius: 6px !important;
                padding: 8px 16px !important;
                font-weight: 500 !important;
                width: 40% !important;
                font-size: 14px !important;
                height: 40px !important;
            }
            button:hover {
                background-color: #c53030 !important;
                border-color: #c53030 !important;
            }
            """,
        ):
            if st.button("Lock & Continue", key=f"confirm_lock_{tab_index}"):
                # Clear confirmation state
                if f"show_confirmation_{tab_index}" in st.session_state:
                    del st.session_state[f"show_confirmation_{tab_index}"]
                # Lock the current tab
                st.session_state.locked_tabs.add(tab_index)
                # Move to next tab
                st.session_state.active_tab = tab_index + 1
                st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, st.session_state.active_tab)
                st.rerun()

    return True

def navigate_to_next_tab():
    """Navigate to the next tab with validation and locking"""
    current_tab = st.session_state.active_tab
    
    # Get validation function for current tab
    validation_func = get_validation_function(current_tab)
    
    if not validation_func():
        tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
        show_validation_popup(tab_names[current_tab])
        return
    
    # If tab is already locked, just navigate
    if current_tab in st.session_state.locked_tabs:
        if current_tab < 3:
            st.session_state.active_tab = current_tab + 1
            st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, st.session_state.active_tab)
            st.rerun()
        return
    
    # If this is the last tab, don't show confirmation
    if current_tab >= 3:
        return
    
    # Show confirmation dialog
    confirmation_key = f"show_confirmation_{current_tab}"
    st.session_state[confirmation_key] = True
    st.rerun()

def navigate_to_previous_tab():
    """Navigate to the previous tab"""
    if st.session_state.active_tab > 0:
        st.session_state.active_tab -= 1
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
st.set_page_config(page_title="CoXPRT", page_icon="Images/gs_logo.png", layout="wide")

# Initialize session ID and logger at the very beginning
if 'session_id' not in st.session_state:
    st.session_state.session_id = generate_session_id()

if 'logger_initialized' not in st.session_state:
    st.session_state.logger_initialized = False

# Setup logging once at the beginning
logger = setup_logging()
        
from main_css import *
st.markdown(app_css, unsafe_allow_html=True)

# Initialize session state for active tab - ENSURE CLIENT TAB IS DEFAULT
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Tab buttons
# Replace the tab button creation section in your app.py with this updated version:

# Tab buttons
tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

# Create tab buttons with stylable containers for #599cd4 active state
cols = st.columns(4, gap="large")
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        is_active = (i == st.session_state.active_tab)
        
        # Determine if tab should be clickable based on validation
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
                    border: 2px solid #4a8bc2 !important;
                    font-weight: bold !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 8px rgba(89, 156, 212, 0.3) !important;
                }
                button:hover {
                    background-color: #4a8bc2 !important;
                    color: white !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 12px rgba(89, 156, 212, 0.4) !important;
                }
                button:focus {
                    background-color: #3b7ab0 !important;
                    color: white !important;
                    outline: none !important;
                }
                """,
            ):
                if st.button(display_name, key=f"tab_{i}", use_container_width=True,disabled = False):
                    st.session_state.active_tab = i
                    st.rerun()
        elif tab_enabled:
            with stylable_container(
                f"inactive_tab_{i}",
                css_styles="""
                button {
                    background-color: #6c757d !important;
                    color: white !important;
                    border: 1px solid #5a6268 !important;
                    transition: all 0.3s ease !important;
                }
                button:hover {
                    background-color: #5a6268 !important;
                    color: white !important;
                    transform: translateY(-1px) !important;
                }
                """,
            ):
                if st.button(display_name, key=f"tab_{i}", use_container_width=True,disabled=False):
                    st.session_state.active_tab = i
                    st.rerun()
        else:
            # Normal styling for disabled tabs (no whitish effect)
            with stylable_container(
                f"disabled_tab_{i}",
                css_styles="""
                button {
                    background-color: #6c757d !important;
                    color: white !important;
                    border: 1px solid #5a6268 !important;
                    cursor: not-allowed !important;
                    opacity: 1 !important;
                }
                button:hover {
                    background-color: #6c757d !important;
                    color: white !important;
                    transform: none !important;
                }
                """,
            ):
                st.button(display_name, key=f"tab_{i}", use_container_width=True, disabled=False)

# Handle confirmation dialogs - POPUP STYLE
current_tab = st.session_state.active_tab
confirmation_key = f"show_confirmation_{current_tab}"

if confirmation_key in st.session_state and st.session_state[confirmation_key]:
    show_lock_confirmation_popup(current_tab)
    st.stop()  # Stop execution to show only the popup

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
        show_validation_popup("Client Information")
        st.rerun()

elif st.session_state.active_tab == 2:
    # Check both client and seller validations
    if not validate_client_mandatory_fields():
        st.session_state.active_tab = 0  # Force back to client tab
        show_validation_popup("Client Information")
        st.rerun()
    elif not validate_seller_mandatory_fields():
        st.session_state.active_tab = 1  # Force back to seller tab
        show_validation_popup("Seller Information")
        st.rerun()
    else:
        print(st.session_state.client_data_from_tab, st.session_state.seller_data_from_tab)
        st.session_state.project_specs_from_tab = proj_specification_tab(
            st.session_state.client_data_from_tab, 
            st.session_state.seller_data_from_tab,
            is_locked=is_tab_locked(2)
        )

else:  # Generate Proposal Tab
    # Check all validations
    if not validate_client_mandatory_fields():
        st.session_state.active_tab = 0
        show_validation_popup("Client Information")
        st.rerun()
    elif not validate_seller_mandatory_fields():
        st.session_state.active_tab = 1
        show_validation_popup("Seller Information")
        st.rerun()
    elif not validate_project_mandatory_fields():
        st.session_state.active_tab = 2
        show_validation_popup("Project Specifications")
        st.rerun()
    else:
        generate_tab(
            st.session_state.client_data_from_tab,
            st.session_state.seller_data_from_tab,
            st.session_state.project_specs_from_tab
        )

# Bottom navigation buttons with enhanced styling
col1, col2, col3 = st.columns(3, gap="large")

# Previous Button
with col1:
    is_first_tab = (st.session_state.active_tab == 0)
    prev_button_text = get_button_text("previous", st.session_state.active_tab)
    
    if is_first_tab:
        with stylable_container(
            "prev_button_disabled",
            css_styles="""
            button {
                background-color: #e9ecef !important;
                color: #6c757d !important;
                border: 1px solid #dee2e6 !important;
                cursor: not-allowed !important;
                opacity: 0.6 !important;
                font-weight: bold !important;
            }
            """,
        ):
            st.button(prev_button_text, key="prev_btn", use_container_width=True, disabled=True)
    else:
        with stylable_container(
            "prev_button",
            css_styles="""
            button {
                background-color: #6c757d !important;
                color: white !important;
                border: 1px solid #5a6268 !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            button:hover {
                background-color: #5a6268 !important;
                color: white !important;
                transform: translateY(-1px) !important;
            }
            button:active {
                background-color: #599cd4 !important;
                border: 2px solid #4a8bc2 !important;
                transform: translateY(0px) !important;
                box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
            }
            """,
        ):
            if st.button(prev_button_text, key="prev_btn", use_container_width=True):
                navigate_to_previous_tab()

# Refresh Button
with col2:
    with stylable_container(
        "refresh_button",
        css_styles="""
        button {
            background-color: #6c757d !important;
            color: white !important;
            border: 1px solid #5a6268 !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        button:hover {
            background-color: #5a6268 !important;
            color: white !important;
            transform: translateY(-1px) !important;
        }
        button:active {
            background-color: #599cd4 !important;
            border: 2px solid #4a8bc2 !important;
            transform: translateY(0px) !important;
            box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
        }
        """,
    ):
        if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True):
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
                background-color: #e9ecef !important;
                color: #6c757d !important;
                border: 1px solid #dee2e6 !important;
                cursor: not-allowed !important;
                opacity: 0.6 !important;
                font-weight: bold !important;
            }
            """,
        ):
            st.button(next_button_text, key="next_btn", use_container_width=True, disabled=True)
    else:
        with stylable_container(
            "next_button",
            css_styles="""
            button {
                background-color: #6c757d !important;
                color: white !important;
                border: 1px solid #5a6268 !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            button:hover {
                background-color: #5a6268 !important;
                color: white !important;
                transform: translateY(-1px) !important;
            }
            button:active {
                background-color: #599cd4 !important;
                border: 2px solid #4a8bc2 !important;
                transform: translateY(0px) !important;
                box-shadow: 0 2px 4px rgba(89, 156, 212, 0.4) !important;
            }
            """,
        ):
            if st.button(next_button_text, key="next_btn", use_container_width=True):
                navigate_to_next_tab()