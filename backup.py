import streamlit as st



def client_tab1():
# Page configuration
st.set_page_config(
    page_title="Sales Proposal Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 3rem;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: #f8f9fa;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.02em;
    }
    
    /* Tab styling */
    .tab-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 3rem;
        flex-wrap: wrap;
    }
    
    .tab-button {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        color: #ecf0f1;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        min-width: 180px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .tab-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        background: linear-gradient(145deg, #34495e, #2c3e50);
    }
    
    .tab-button.active {
        background: linear-gradient(145deg, #e74c3c, #c0392b);
        transform: translateY(-1px);
        box-shadow: 0 5px 18px rgba(231, 76, 60, 0.4);
    }
    
    /* Content area */
    .content-area {
        background: rgba(0, 0, 0, 0.05);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 3rem;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: 400px;
    }
    
    .content-area h2 {
        color: #f8f9fa;
        font-size: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .content-area p {
        color: #ecf0f1;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        background: rgba(0, 0, 0, 0.2);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-buttons {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    
    .footer-button {
        background: linear-gradient(145deg, #27ae60, #2ecc71);
        color: #2c3e50;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(39, 174, 96, 0.3);
        min-width: 120px;
    }
    
    .footer-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
        background: linear-gradient(145deg, #2ecc71, #27ae60);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom input styling */
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: #f8f9fa;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Header
st.markdown("""
<div class="main-header">
    <h1>Sales Proposal Generator</h1>
</div>
""", unsafe_allow_html=True)

# Tab buttons
tab_names = ["Proposal Builder", "Template Library", "Client Database", "Analytics Dashboard"]

# Create tab buttons
cols = st.columns(4)
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = i

# Add custom styling for active tab
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-child({st.session_state.active_tab + 1}) button {{
        background: linear-gradient(145deg, #e74c3c, #c0392b) !important;
        color: #f8f9fa !important;
        font-weight: 700 !important;
    }}
</style>
""", unsafe_allow_html=True)

# # Content area based on active tab
# st.markdown('<div class="content-area">', unsafe_allow_html=True)

if st.session_state.active_tab == 0:
    st.markdown("## 📝 Proposal Builder")
    st.markdown("Create professional sales proposals with our intuitive builder.")
    
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", placeholder="Enter client name...")
        project_type = st.selectbox("Project Type", ["Software Development", "Consulting", "Marketing", "Design"])
        budget_range = st.selectbox("Budget Range", ["$5K - $10K", "$10K - $25K", "$25K - $50K", "$50K+"])
    
    with col2:
        timeline = st.selectbox("Timeline", ["1-2 weeks", "1 month", "2-3 months", "3+ months"])
        priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Urgent"])
        
    st.text_area("Project Description", placeholder="Describe the project requirements...", height=100)
    
    if st.button("Generate Proposal", type="primary"):
        st.success("🎉 Proposal generated successfully!")

elif st.session_state.active_tab == 1:
    st.markdown("## 📄 Template Library")
    st.markdown("Browse and customize our collection of proven proposal templates.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Software Development")
        st.markdown("- Web Application Template")
        st.markdown("- Mobile App Template")
        st.markdown("- API Development Template")
    
    with col2:
        st.markdown("### Consulting Services")
        st.markdown("- Business Strategy Template")
        st.markdown("- Process Optimization Template")
        st.markdown("- Digital Transformation Template")
    
    with col3:
        st.markdown("### Marketing & Design")
        st.markdown("- Brand Identity Template")
        st.markdown("- Digital Marketing Template")
        st.markdown("- Website Design Template")

elif st.session_state.active_tab == 2:
    st.markdown("## 👥 Client Database")
    st.markdown("Manage your client relationships and proposal history.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Recent Clients")
        clients = ["Acme Corp", "TechStart Inc", "Global Solutions", "Innovation Labs"]
        for client in clients:
            st.markdown(f"• {client}")
    
    with col2:
        st.markdown("### Proposal Statistics")
        st.metric("Total Proposals", "47", "+12%")
        st.metric("Success Rate", "73%", "+5%")
        st.metric("Average Value", "$18,500", "+8%")

else:  # Analytics Dashboard
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("Track your proposal performance and business metrics.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("This Month", "$125,000", "+15%")
    
    with col2:
        st.metric("Proposals Sent", "23", "+3")
    
    with col3:
        st.metric("Conversion Rate", "68%", "+12%")
    
    st.markdown("### 📈 Performance Trends")
    st.markdown("Your proposal success rate has improved by 12% this quarter, with the highest performance in software development projects.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-buttons">
        <button class="footer-button" onclick="alert('Support contacted!')">Support</button>
        <button class="footer-button" onclick="alert('Settings opened!')">Settings</button>
        <button class="footer-button" onclick="alert('About page opened!')">About</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Add some JavaScript for footer button functionality
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Add any additional JavaScript functionality here
});
</script>
""", unsafe_allow_html=True)