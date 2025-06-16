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
        
st.markdown("""
<style>/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styles */
.stApp {
    background: #1a1a1a;
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
    background: #2d3748 ;
    border-radius: 15px;
    border: 1px solid #3a3a3a;
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
    background: #1a1a1a;
    color: #ecf0f1;
    border: 1px solid #3a3a3a;
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
    background: #2a2a2a;
    border-color: #4a5568;
}

.tab-button.active {
    background: #2d3748;
    transform: translateY(-1px);
    box-shadow: 0 5px 18px rgba(45, 55, 72, 0.4);
    border-color: #4a5568;
}

/* Content area */
.content-area {
    background: #2a2a2a;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    border: 1px solid #3a3a3a;
    min-height: 600px;
}

.content-area h2 {
    color: #f8f9fa;
    font-size: 2rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.content-area h3 {
    color: #f8f9fa;
    font-size: 1.3rem;
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
    background: #2a2a2a;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-top: 3rem;
    border: 1px solid #3a3a3a;
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

.refresh-button {
    background: linear-gradient(145deg, #f39c12, #e67e22);
    color: #2c3e50;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 3px 10px rgba(243, 156, 18, 0.3);
    min-width: 120px;
}

.refresh-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4);
    background: linear-gradient(145deg, #e67e22, #f39c12);
}

.generate-button {
    background: linear-gradient(145deg, #e74c3c, #c0392b);
    color: #f8f9fa;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 3px 10px rgba(231, 76, 60, 0.3);
    min-width: 120px;
}

.generate-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
    background: linear-gradient(145deg, #c0392b, #e74c3c);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom input styling */
.stSelectbox > div > div > div {
    background-color: #2c3e50;
    color: #f8f9fa;
    border: 1px solid #4a5568;
}

.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background-color: #2c3e50;
    color: #f8f9fa;
    border: 1px solid #4a5568;
}

/* File uploader styling */
.stFileUploader > div {
    background-color: #2c3e50;
    border: 2px dashed #4a5568;
    border-radius: 10px;
    padding: 1rem;
}

.stFileUploader label, .stFileUploader p, .stFileUploader svg {
    color: #f8f9fa !important;
    fill: #f8f9fa !important;
}

/* Custom divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    margin: 2rem 0;
}

/* Mandatory field styling */
.mandatory-field {
    border: 2px solid #e74c3c !important;
    background-color: #2c1810 !important;
}

.field-warning {
    color: #e74c3c;
    font-size: 0.9rem;
    margin-top: 0.25rem;
    font-weight: 500;
}

/* Fixed Tab Button Styling - All tabs dark, active tab blue */
.stButton > button {
    background: #2a2a2a !important;
    color: #ecf0f1 !important;
    border: 1px solid #3a3a3a !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    height: 3rem !important;
    border-radius: 10px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    background: #3a3a3a !important;
    border-color: #4a5568 !important;
}

/* Active tab styling - Blue color */
.stButton > button:focus,
.stButton > button:active {
    background: linear-gradient(145deg, #3b82f6, #2563eb) !important;
    color: #ffffff !important;
    border-color: #1d4ed8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(59, 130, 246, 0.4) !important;
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
tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]

# Create tab buttons
cols = st.columns(4)
for i, tab_name in enumerate(tab_names):
    with cols[i]:
        if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
            st.session_state.active_tab = i

# Dynamic styling for active tab - Blue color when active
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-child({st.session_state.active_tab + 1}) button {{
        background: linear-gradient(145deg, #3b82f6, #2563eb) !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
        font-weight: 700 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 18px rgba(59, 130, 246, 0.4) !important;
    }}
</style>
""", unsafe_allow_html=True)


if st.session_state.active_tab == 0:
    client_tab()

elif st.session_state.active_tab == 1:
    st.markdown("## 📄 Template Library")
    # st.markdown("Browse and customize our collection of proven proposal templates.")
    
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     st.markdown("### Software Development")
    #     st.markdown("- Web Application Template")
    #     st.markdown("- Mobile App Template")
    #     st.markdown("- API Development Template")
    
    # with col2:
    #     st.markdown("### Consulting Services")
    #     st.markdown("- Business Strategy Template")
    #     st.markdown("- Process Optimization Template")
    #     st.markdown("- Digital Transformation Template")
    
    # with col3:
    #     st.markdown("### Marketing & Design")
    #     st.markdown("- Brand Identity Template")
    #     st.markdown("- Digital Marketing Template")
    #     st.markdown("- Website Design Template")

elif st.session_state.active_tab == 2:
    st.markdown("## 👥 Client Database")
    # st.markdown("Manage your client relationships and proposal history.")
    
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.markdown("### Recent Clients")
    #     clients = ["Acme Corp", "TechStart Inc", "Global Solutions", "Innovation Labs"]
    #     for client in clients:
    #         st.markdown(f"• {client}")
    
    # with col2:
    #     st.markdown("### Proposal Statistics")
    #     st.metric("Total Proposals", "47", "+12%")
    #     st.metric("Success Rate", "73%", "+5%")
    #     st.metric("Average Value", "$18,500", "+8%")

else:  # Analytics Dashboard
    st.markdown("## 📊 Analytics ")
    # st.markdown("Track your proposal performance and business metrics.")
    
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     st.metric("This Month", "$125,000", "+15%")
    
    # with col2:
    #     st.metric("Proposals Sent", "23", "+3")
    
    # with col3:
    #     st.metric("Conversion Rate", "68%", "+12%")
    
    # st.markdown("### 📈 Performance Trends")
    # st.markdown("Your proposal success rate has improved by 12% this quarter, with the highest performance in software development projects.")

# Footer with updated buttons


# Footer buttons styling - keeping original colors for footer buttons
st.markdown("""
<style>
    /* Footer button styling - separate from tab buttons */
    .footer .stButton > button {
        height: 3rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-size: 0.9rem !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    
    /* Refresh Button */
    .footer div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(145deg, #f39c12, #e67e22) !important;
        color: #2c3e50 !important;
        box-shadow: 0 3px 10px rgba(243, 156, 18, 0.3) !important;
    }
    
    .footer div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4) !important;
        background: linear-gradient(145deg, #e67e22, #f39c12) !important;
    }
    
    /* Generate Presentation Button */
    .footer div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(145deg, #e74c3c, #c0392b) !important;
        color: #f8f9fa !important;
        box-shadow: 0 3px 10px rgba(231, 76, 60, 0.3) !important;
    }
    
    .footer div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4) !important;
        background: linear-gradient(145deg, #c0392b, #e74c3c) !important;
    }
    
    /* Settings and About Buttons */
    .footer div[data-testid="column"]:nth-child(3) .stButton > button,
    .footer div[data-testid="column"]:nth-child(4) .stButton > button {
        background: linear-gradient(145deg, #27ae60, #2ecc71) !important;
        color: #2c3e50 !important;
        box-shadow: 0 3px 10px rgba(39, 174, 96, 0.3) !important;
    }
    
    .footer div[data-testid="column"]:nth-child(3) .stButton > button:hover,
    .footer div[data-testid="column"]:nth-child(4) .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4) !important;
        background: linear-gradient(145deg, #2ecc71, #27ae60) !important;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Refresh", key="refresh_btn", use_container_width=True):
        refresh_all_data()

with col2:
    if st.button("📊 Generate Presentation", key="generate_btn", use_container_width=True):
        generate_presentation()
