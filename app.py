import streamlit as st
import time
from Client.client import client_tab,validate_client_mandatory_fields
from Seller.seller import seller_tab

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

# Tab buttons
tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

# Create tab buttons with full width
cols = st.columns(4, gap="large")
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        # Add a unique class to identify active tab
        button_key = f"tab_{i}"
        
        # Determine if tab should be clickable based on validation
        tab_enabled = True
        
        if i == 1:  # Seller Information tab
            if not validate_client_mandatory_fields():
                tab_enabled = False
        elif i == 2:  # Project Specifications tab
            if not validate_client_mandatory_fields() or not validate_seller_mandatory_fields():
                tab_enabled = False
        elif i == 3:  # Generate Proposal tab
            if not validate_client_mandatory_fields() or not validate_seller_mandatory_fields() or not validate_project_mandatory_fields():
                tab_enabled = False
        
        # Create button with conditional styling
        if tab_enabled:
            if st.button(tab_name, key=button_key, use_container_width=True):
                st.session_state.active_tab = i
                st.rerun()  # Force rerun to update styling
        else:
            # Create disabled button
            st.button(tab_name, key=button_key, use_container_width=True, disabled=True)
            
            # Show validation popup if user tries to access restricted tab
            if st.session_state.get(f"clicked_disabled_{i}", False):
                if i == 1:  # Seller tab
                    show_validation_popup("Client Information")
                elif i == 2:  # Project tab
                    if not validate_client_mandatory_fields():
                        show_validation_popup("Client Information")
                    else:
                        show_validation_popup("Seller Information")
                elif i == 3:  # Generate tab
                    if not validate_client_mandatory_fields():
                        show_validation_popup("Client Information")
                    elif not validate_seller_mandatory_fields():
                        show_validation_popup("Seller Information")
                    else:
                        show_validation_popup("Project Specifications")

# Add JavaScript to handle disabled button clicks
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Add click listeners to disabled buttons
    const buttons = document.querySelectorAll('button[disabled]');
    buttons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // You can add custom popup logic here if needed
            alert('Please complete previous sections first!');
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Enhanced CSS with disabled button styling
st.markdown(f"""
<style>
    /* Base styles for all tab buttons */
    div[data-testid="column"] button[data-testid="baseButton-secondary"] {{
        background: rgba(42, 42, 42, 0.8) !important;
        color: #ecf0f1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        height: 4rem !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    /* Disabled button styling */
    div[data-testid="column"] button[data-testid="baseButton-secondary"]:disabled {{
        background: rgba(60, 60, 60, 0.4) !important;
        color: rgba(236, 240, 241, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        cursor: not-allowed !important;
        opacity: 0.5 !important;
        transform: none !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    }}
    
    /* Hover effects for enabled inactive tabs only */
    div[data-testid="column"]:not(:nth-child({st.session_state.active_tab + 1})) button[data-testid="baseButton-secondary"]:not(:disabled):hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
        background: rgba(58, 58, 58, 0.9) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }}
    
    /* Remove hover effects for disabled buttons */
    div[data-testid="column"] button[data-testid="baseButton-secondary"]:disabled:hover {{
        transform: none !important;
        background: rgba(60, 60, 60, 0.4) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    }}
    
    /* ACTIVE TAB STYLING - Applied to current active tab */
    div[data-testid="column"]:nth-child({st.session_state.active_tab + 1}) button[data-testid="baseButton-secondary"]:not(:disabled) {{
        background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
        color: #ffffff !important;
        border-color: #7c3aed !important;
        font-weight: 800 !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.5) !important;
        animation: activeTabPulse 2s ease-in-out infinite !important;
    }}
    
    /* Shimmer effect for active tab */
    div[data-testid="column"]:nth-child({st.session_state.active_tab + 1}) button[data-testid="baseButton-secondary"]:not(:disabled)::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        animation: shimmer 2s ease-in-out infinite !important;
    }}
    
    /* Animations */
    @keyframes activeTabPulse {{
        0%, 100% {{
            box-shadow: 0 12px 40px rgba(139, 92, 246, 0.5) !important;
        }}
        50% {{
            box-shadow: 0 15px 50px rgba(139, 92, 246, 0.7) !important;
        }}
    }}
    
    @keyframes shimmer {{
        0% {{ left: -100% !important; }}
        100% {{ left: 100% !important; }}
    }}
    
    /* Text shadow for active tab */
    div[data-testid="column"]:nth-child({st.session_state.active_tab + 1}) button[data-testid="baseButton-secondary"]:not(:disabled) div {{
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* Lock icon for disabled tabs */
    div[data-testid="column"] button[data-testid="baseButton-secondary"]:disabled::after {{
        content: "🔒" !important;
        position: absolute !important;
        top: 50% !important;
        right: 15px !important;
        transform: translateY(-50%) !important;
        font-size: 1rem !important;
        opacity: 0.6 !important;
    }}
</style>
""", unsafe_allow_html=True)

# Content area with validation-aware tab switching
if st.session_state.active_tab == 0:
    client_tab(st)

elif st.session_state.active_tab == 1:
    # Double-check validation before showing seller tab
    if validate_client_mandatory_fields():
        seller_tab()
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
        st.markdown('<h2 class="gradient-text">👥 Project Specifications</h2>', unsafe_allow_html=True)
        st.markdown("Define your project requirements and specifications.")
        
        col1, col2, col3 = st.columns([2, 2, 2], gap="large")
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 class="gradient-text">Recent Clients</h3>
                <p>• Acme Corporation</p>
                <p>• TechStart Inc</p>
                <p>• Global Solutions Ltd</p>
                <p>• Innovation Labs</p>
                <p>• Digital Dynamics</p>
                <p>• Future Systems Co</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">47</div>
                <div class="metric-label">Total Proposals</div>
                <p style="color: #10b981; margin-top: 1rem;">+12% this month</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">73%</div>
                <div class="metric-label">Success Rate</div>
                <p style="color: #10b981; margin-top: 1rem;">+5% improvement</p>
            </div>
            """, unsafe_allow_html=True)

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
        st.markdown('<h2 class="gradient-text">📊 Generate Proposal</h2>', unsafe_allow_html=True)
        st.markdown("Review and generate your final proposal.")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4, gap="large")
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">$125K</div>
                <div class="metric-label">This Month</div>
                <p style="color: #10b981; margin-top: 1rem;">+15% growth</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">23</div>
                <div class="metric-label">Proposals Sent</div>
                <p style="color: #10b981; margin-top: 1rem;">+3 from last month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">68%</div>
                <div class="metric-label">Conversion Rate</div>
                <p style="color: #10b981; margin-top: 1rem;">+12% improvement</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">$18.5K</div>
                <div class="metric-label">Average Value</div>
                <p style="color: #10b981; margin-top: 1rem;">+8% increase</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 3rem 0;"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="grid-item">
            <h3 class="gradient-text">📈 Performance Trends</h3>
            <p>Your proposal success rate has improved by 12% this quarter, with the highest performance in software development projects. The average deal size has increased significantly, and client satisfaction scores are at an all-time high.</p>
            <p>Key insights: Enterprise clients show 85% higher conversion rates, and proposals with detailed technical specifications convert 40% better than generic templates.</p>
        </div>
        """, unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True):
        refresh_all_data()

with col2:
    if st.button("📊 Generate Presentation", key="generate_btn", use_container_width=True):
        generate_presentation()

st.markdown('</div>', unsafe_allow_html=True)