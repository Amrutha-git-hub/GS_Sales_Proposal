import streamlit as st
import time
from Client.client import client_tab

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

# Initialize session state for active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Tab buttons
tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

# Create tab buttons with full width
cols = st.columns(4, gap="large")
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = i

# Dynamic styling for active tab
st.markdown(f"""
<style>
    /* Active tab styling for the new column layout */
    div[data-testid="column"]:nth-child({(st.session_state.active_tab * 2) + 1}) button {{
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
        font-weight: 800 !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 10px 40px rgba(59, 130, 246, 0.4) !important;
    }}
    
    /* Add glowing effect to active tab separator */
    div[data-testid="column"]:nth-child({(st.session_state.active_tab * 2) + 2}) .separator-diamond,
    div[data-testid="column"]:nth-child({(st.session_state.active_tab * 2)}) .separator-diamond {{
        animation: glow-diamond 1.5s ease-in-out infinite !important;
    }}
    
    @keyframes glow-diamond {{
        0%, 100% {{
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.8);
        }}
        50% {{
            box-shadow: 0 0 30px rgba(147, 51, 234, 1);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# # Content area with full width container
# st.markdown('<div class="content-area">', unsafe_allow_html=True)

if st.session_state.active_tab == 0:
    client_tab()

elif st.session_state.active_tab == 1:
    st.markdown('<h2 class="gradient-text">📄 Template Library</h2>', unsafe_allow_html=True)
    st.markdown("Browse and customize our collection of proven proposal templates.")
    
    # Full-width grid layout for templates
    st.markdown("""
    <div class="full-width-grid">
        <div class="grid-item">
            <h3 class="gradient-text">Software Development</h3>
            <p>• Web Application Template</p>
            <p>• Mobile App Template</p>
            <p>• API Development Template</p>
            <p>• Cloud Infrastructure Template</p>
        </div>
        <div class="grid-item">
            <h3 class="gradient-text">Consulting Services</h3>
            <p>• Business Strategy Template</p>
            <p>• Process Optimization Template</p>
            <p>• Digital Transformation Template</p>
            <p>• Technology Audit Template</p>
        </div>
        <div class="grid-item">
            <h3 class="gradient-text">Marketing & Design</h3>
            <p>• Brand Identity Template</p>
            <p>• Digital Marketing Template</p>
            <p>• Website Design Template</p>
            <p>• Social Media Strategy Template</p>
        </div>
        <div class="grid-item">
            <h3 class="gradient-text">Enterprise Solutions</h3>
            <p>• ERP Implementation Template</p>
            <p>• Data Analytics Template</p>
            <p>• Security Assessment Template</p>
            <p>• Integration Services Template</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.active_tab == 2:
    st.markdown('<h2 class="gradient-text">👥 Client Database</h2>', unsafe_allow_html=True)
    st.markdown("Manage your client relationships and proposal history.")
    
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

else:  # Analytics Dashboard
    st.markdown('<h2 class="gradient-text">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("Track your proposal performance and business metrics.")
    
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
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True):
        refresh_all_data()

with col2:
    if st.button("📊 Generate Presentation", key="generate_btn", use_container_width=True):
        generate_presentation()

st.markdown('</div>', unsafe_allow_html=True)