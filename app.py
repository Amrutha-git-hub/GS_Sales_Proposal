import streamlit as st
import time
from client import client_tab

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
        
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global styles - Full screen utilization */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

/* Remove default padding and make full width */
.block-container {
    padding: 1rem 2rem 2rem 2rem;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
}

/* Main container - Full width */
.main-container {
    width: 100%;
    min-height: 100vh;
    margin: 0;
    padding: 0;
}

/* Header styling - Full width with glassmorphism */
.main-header {
    width: 100%;
    padding: 3rem 0;
    margin-bottom: 2rem;
    background: rgba(45, 55, 72, 0.3);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1));
    z-index: -1;
}

.main-header h1 {
    color: #ffffff;
    font-size: 4rem;
    font-weight: 800;
    margin: 0;
    text-align: center;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Creative tab separators */
.tab-nav-container {
    width: 100%;
    position: relative;
    margin-bottom: 2rem;
}

.tab-separator-line {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(59, 130, 246, 0.3) 25%, 
        rgba(147, 51, 234, 0.5) 50%, 
        rgba(59, 130, 246, 0.3) 75%, 
        transparent 100%);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
}

.tab-separator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 4rem;
    position: relative;
}

.separator-diamond {
    width: 8px;
    height: 8px;
    background: linear-gradient(45deg, #3b82f6, #8b5cf6);
    transform: rotate(45deg);
    border-radius: 2px;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
    animation: pulse-diamond 2s ease-in-out infinite;
    z-index: 2;
}

.separator-line {
    width: 2px;
    height: 30px;
    background: linear-gradient(180deg, 
        rgba(59, 130, 246, 0.8) 0%, 
        rgba(147, 51, 234, 0.6) 50%, 
        rgba(59, 130, 246, 0.8) 100%);
    margin: 4px 0;
    border-radius: 1px;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
    z-index: 2;
}

@keyframes pulse-diamond {
    0%, 100% {
        transform: rotate(45deg) scale(1);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
    }
    50% {
        transform: rotate(45deg) scale(1.2);
        box-shadow: 0 0 25px rgba(147, 51, 234, 0.8);
    }
}

/* Tab styling - Improved modern design */
.stButton > button {
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
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
    transition: left 0.5s ease !important;
}

.stButton > button:hover::before {
    left: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
    background: rgba(58, 58, 58, 0.9) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Active tab styling - Vibrant gradient */
.stButton > button:focus,
.stButton > button:active {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: #ffffff !important;
    border-color: #1d4ed8 !important;
    transform: translateY(-2px) scale(1.03) !important;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.4) !important;
    font-weight: 700 !important;
}

/* Content area - Full width with modern styling */
.content-area {
    background: rgba(42, 42, 42, 0.4);
    backdrop-filter: blur(20px);
    padding: 3rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    min-height: 70vh;
    width: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.content-area::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
    z-index: -1;
}

.content-area h2 {
    color: #ffffff;
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.content-area h3 {
    color: #e2e8f0;
    font-size: 1.5rem;
    margin-bottom: 1.2rem;
    font-weight: 600;
}

.content-area p {
    color: #cbd5e0;
    font-size: 1.2rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
}

/* Full-width grid layouts for content */
.full-width-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    width: 100%;
    margin: 2rem 0;
}

.grid-item {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.grid-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    background: rgba(255, 255, 255, 0.08);
}

/* Footer styling - Full width */
.footer {
    background: rgba(42, 42, 42, 0.3);
    backdrop-filter: blur(20px);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-top: 3rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Footer button styling - Enhanced */
.footer .stButton > button {
    height: 4rem !important;
    font-weight: 700 !important;
    border-radius: 15px !important;
    border: none !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-size: 1.1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    position: relative !important;
    overflow: hidden !important;
}

.footer .stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
    transition: left 0.6s ease !important;
}

.footer .stButton > button:hover::before {
    left: 100% !important;
}

/* Refresh Button */
.footer div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #f39c12, #e67e22) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(243, 156, 18, 0.4) !important;
}

.footer div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 10px 30px rgba(243, 156, 18, 0.6) !important;
    background: linear-gradient(135deg, #e67e22, #d35400) !important;
}

/* Generate Presentation Button */
.footer div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4) !important;
}

.footer div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 10px 30px rgba(231, 76, 60, 0.6) !important;
    background: linear-gradient(135deg, #c0392b, #a93226) !important;
}

/* Input styling - Modern glassmorphism */
.stSelectbox > div > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(44, 62, 80, 0.3) !important;
    backdrop-filter: blur(10px) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div > div:focus,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3) !important;
    background: rgba(44, 62, 80, 0.5) !important;
}

/* File uploader styling */
.stFileUploader > div {
    background: rgba(44, 62, 80, 0.3) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px dashed rgba(255, 255, 255, 0.3) !important;
    border-radius: 15px !important;
    padding: 2rem !important;
    transition: all 0.3s ease !important;
}

.stFileUploader > div:hover {
    border-color: #3b82f6 !important;
    background: rgba(44, 62, 80, 0.4) !important;
}

.stFileUploader label, .stFileUploader p, .stFileUploader svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* Sidebar removal */
.css-1d391kg {
    display: none !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stToolbar {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2.5rem;
    }
    
    .content-area {
        padding: 1.5rem;
    }
    
    .stButton > button {
        height: 3rem !important;
        font-size: 0.9rem !important;
    }
}

/* Loading animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.content-area {
    animation: fadeInUp 0.6s ease-out;
}

/* Gradient text for headings */
.gradient-text {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Enhanced metrics and cards */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    background: rgba(255, 255, 255, 0.08);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #3b82f6;
    margin-bottom: 0.5rem;
}

.metric-label {
    color: #cbd5e0;
    font-size: 1.1rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown('<div class="footer">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("🔄 Refresh All Data", key="refresh_btn", use_container_width=True):
        refresh_all_data()

with col2:
    if st.button("📊 Generate Presentation", key="generate_btn", use_container_width=True):
        generate_presentation()

st.markdown('</div>', unsafe_allow_html=True)