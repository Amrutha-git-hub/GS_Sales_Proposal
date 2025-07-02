import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import time
from Client.client import client_tab,validate_client_mandatory_fields
from Seller.seller import seller_tab
from ProjectSpecification.project_spec import proj_specification_tab
from Generate_proposal.proposal_generator import generate_tab
from Client.client import setup_logging
from Client.client_dataclass import ClientData
from Seller.seller import SellerTabState

if 'client_data_from_tab' not in st.session_state:
    st.session_state.client_data_from_tab = None

if 'seller_data_from_tab' not in st.session_state:
    st.session_state.seller_data_from_tab = None

if 'project_specs_from_tab' not in st.session_state:
    st.session_state.project_specs_from_tab = None



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

def refresh_all_data():
    """Clear all session state and form data"""
    # Clear all session state variables
    keys_to_clear = [
        'client_name_input', 'url_selector', 'pain_points', 'pain_points_extracted',
        'pain_points_placeholder', 'editable_content_area', 'pain_points_summary',
        'selected_roles', 'selected_priorities', 'problem_statement'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
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
    st.error(f"⚠️ Please complete all mandatory fields in {missing_tab_name} tab first!")
    if missing_fields:
        st.error(f"Missing required fields: {missing_fields}")

def validate_mandatory_fields():
    """Validate mandatory fields and return validation results"""
    errors = []
    
    # Check client name
    client_name = st.session_state.get('client_name_input', '').strip()
    if not client_name:
        errors.append("Client Name")
    
    # Check problem statement
    problem_statement = st.session_state.get('problem_statement', '').strip()
    if not problem_statement:
        errors.append("Problem Statement")
    
    return errors

def generate_presentation():
    """Generate presentation after validating mandatory fields"""
    validation_errors = validate_mandatory_fields()
    
    if validation_errors:
        # Trigger validation display in client tab
        st.session_state.trigger_validation = True
        st.session_state.show_validation = True
        
        # Show error message
        st.error("⚠️ Please fill in all mandatory fields before generating presentation!")
        
        # Show specific missing fields
        missing_fields = ", ".join(validation_errors)
        st.error(f"Missing required fields: {missing_fields}")
        
        # Force rerun to show validation warnings
        st.rerun()
        return False
    else:
        st.success("✅ All mandatory fields are filled! Generating presentation...")
        with st.spinner("Generating presentation..."):
            import time
            time.sleep(2)  # Simulate processing time
        st.success("🎉 Presentation generated successfully!")
        
        # You can add your actual presentation generation logic here
        # For example:
        # - Create PowerPoint slides
        # - Generate PDF report
        # - Send to external API
        # - Save to database
        
        return True

# NOTE: Add this line at the very top of your main script (before any other Streamlit commands):
# st.set_page_config(page_title="Sales Proposal Generator", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
        
from main_css import *
st.markdown(app_css, unsafe_allow_html=True)

# Initialize session state for active tab - ENSURE CLIENT TAB IS DEFAULT
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

st.info("START OF THE PROJECT")

# Tab buttons
tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

# Create tab buttons with stylable containers for green active state
cols = st.columns(4, gap="large")
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        is_active = (i == st.session_state.active_tab)
        
        # Determine if tab should be clickable based on validation
        tab_enabled = True
        if i == 1 and not validate_client_mandatory_fields():
            tab_enabled = False
        elif i == 2 and (not validate_client_mandatory_fields() or not validate_seller_mandatory_fields()):
            tab_enabled = False
        elif i == 3 and (not validate_client_mandatory_fields() or not validate_seller_mandatory_fields() or not validate_project_mandatory_fields()):
            tab_enabled = False
        
        # Use stylable_container to make active tab green
        if is_active and tab_enabled:
            with stylable_container(
                f"active_tab_{i}",
                css_styles="""
                button {
                    background-color: #28a745 !important;
                    color: white !important;
                    border: 2px solid #1e7e34 !important;
                    font-weight: bold !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3) !important;
                }
                button:hover {
                    background-color: #218838 !important;
                    color: white !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 12px rgba(40, 167, 69, 0.4) !important;
                }
                button:focus {
                    background-color: #1e7e34 !important;
                    color: white !important;
                    outline: none !important;
                }
                """,
            ):
                if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
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
                if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
                    st.session_state.active_tab = i
                    st.rerun()
        else:
            # Disabled tab styling
            with stylable_container(
                f"disabled_tab_{i}",
                css_styles="""
                button {
                    background-color: #e9ecef !important;
                    color: #6c757d !important;
                    border: 1px solid #dee2e6 !important;
                    cursor: not-allowed !important;
                    opacity: 0.6 !important;
                }
                """,
            ):
                st.button(tab_name, key=f"tab_{i}", use_container_width=True, disabled=True)

# Set is_active flag for current tab
st.session_state.is_active = True

# Content area with validation-aware tab switching
if st.session_state.active_tab == 0:
    logger = setup_logging()
    st.session_state.client_data_from_tab = client_tab(st,logger)

elif st.session_state.active_tab == 1:
    # Double-check validation before showing seller tab
    if validate_client_mandatory_fields():
        st.session_state.seller_data_from_tab = seller_tab()
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
        print(st.session_state.client_data_from_tab,st.session_state.seller_data_from_tab)
        st.session_state.project_specs_from_tab=  proj_specification_tab(st.session_state.client_data_from_tab,st.session_state.seller_data_from_tab)

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
       generate_tab(st.session_state.client_data_from_tab,st.session_state.seller_data_from_tab,st.session_state.project_specs_from_tab)

# Bottom action buttons with enhanced styling
col1, col2 = st.columns(2, gap="large")

with col1:
    with stylable_container(
        "refresh_button",
        css_styles="""
        button {
            background-color: #17a2b8 !important;
            color: white !important;
            border: 2px solid #138496 !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        button:hover {
            background-color: #138496 !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(23, 162, 184, 0.3) !important;
        }
        """,
    ):
        if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True):
            refresh_all_data()

with col2:
    with stylable_container(
        "generate_button",
        css_styles="""
        button {
            background-color: #dc3545 !important;
            color: white !important;
            border: 2px solid #c82333 !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        button:hover {
            background-color: #c82333 !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3) !important;
        }
        """,
    ):
        if st.button("📊 Generate Presentation", key="generate_btn", use_container_width=True):
            generate_presentation()