import streamlit as st

def add_professional_css():
    """Add professional CSS styling - MADE MORE COMPACT"""
    st.markdown("""
    <style>
    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
        background: #1a1a1a;
    }
    
    /* Header styling - more compact */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        text-align: center;
        color: #f0f0f0;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 600;
        color: #f0f0f0;
    }
    
    .main-header p {
        margin: 0.2rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
        color: #f0f0f0;
    }
    
    /* Section styling - much more compact */
    .form-section {
        padding: 0.8rem 1rem;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.8rem;
        border: 1px solid #444;
        background: #2d2d2d;
    }
    
    .section-title {
        color: #e0e0e0;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        padding-bottom: 0.2rem;
        border-bottom: 2px solid #3498db;
    }
    
    /* Form field styling - MADE SMALLER */
    .field-label {
        color: #d0d0d0;
        font-weight: 600;
        margin-bottom: 0.2rem;
        display: block;
        font-size: 0.85rem;
    }
    
    .required-asterisk {
        color: #e74c3c;
        font-weight: bold;
        margin-left: 3px;
    }
    
    /* Input field improvements - MUCH MORE COMPACT */
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #555;
        padding: 0.4rem 0.6rem;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
        height: 2.2rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 4px;
        border: 1px solid #555;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
        min-height: 2.2rem;
    }
    
    .stSelectbox > div > div > div:focus-within {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 4px;
        border: 1px solid #555;
        padding: 0.4rem 0.6rem;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        background: #3a3a3a;
        color: #e0e0e0;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
        background: #404040;
    }
    
    /* File uploader styling - more compact */
    .stFileUploader > div {
        border: 2px dashed #666;
        border-radius: 6px;
        padding: 0.8rem;
        text-align: center;
        transition: all 0.3s ease;
        background: #333;
        color: #d0d0d0;
    }
    
    .stFileUploader > div:hover {
        border-color: #3498db;
        background: #404040;
    }
    
    /* Button styling - more compact */
    .stButton > button {
        border-radius: 4px;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        transition: all 0.3s ease;
        font-size: 0.85rem;
        height: 2.2rem;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3498db, #2980b9);
        border: none;
        color: #f0f0f0;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2980b9, #21618c);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="secondary"] {
        border: 2px solid #666;
        color: #d0d0d0;
        background: #3a3a3a;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #555;
        border-color: #777;
    }
    
    /* Link button styling - more compact */
    .external-link-btn {
        background: #27ae60;
        border: none;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        display: inline-block;
        font-size: 0.75rem;
        color: #f0f0f0;
        height: 2.2rem;
        line-height: 1.6rem;
    }
    
    .external-link-btn:hover {
        background: #219a52;
        transform: translateY(-1px);
        text-decoration: none;
        color: #f0f0f0;
    }
    
    /* Validation styling - more compact */
    .validation-success {
        color: #27ae60;
        font-size: 0.75rem;
        margin-top: 0.2rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .validation-error {
        color: #e74c3c;
        font-size: 0.75rem;
        margin-top: 0.2rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Progress styling - more compact */
    .progress-container {
        padding: 0.8rem;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
        border: 1px solid #444;
        background: #2d2d2d;
        color: #e0e0e0;
    }
    
    /* Info styling - more compact */
    .info-container {
        background: #333;
        border-left: 4px solid #3498db;
        padding: 0.6rem;
        border-radius: 0 4px 4px 0;
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #d0d0d0;
    }
    
    /* Reduce spacing between elements - CRITICAL FOR COMPACTNESS */
    .element-container {
        margin-bottom: 0.3rem !important;
    }
    
    .stColumns > div {
        padding: 0 0.3rem;
    }
    
    /* Compact sidebar */
    .css-1d391kg {
        padding-top: 0.8rem;
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* General dark theme colors */
    .stApp {
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Streamlit element colors */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Hide default streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* COMPACT column-container for suggestions */
    .column-container {
        margin: 0.5rem 0;
    }
    
    .left-column, .right-column {
        padding: 0.6rem;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
        border: 1px solid #444;
        background: #2d2d2d;
        height: 100%;
    }
    
    .column-header {
        color: #e0e0e0;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        padding-bottom: 0.2rem;
        border-bottom: 2px solid #3498db;
    }
    
    .column-content {
        height: calc(100% - 2rem);
    }
    
    .suggestion-container {
        background: #3a3a3a;
        border: 1px solid #555;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .suggestion-container:hover {
        background: #454545;
        border-color: #666;
    }
    
    .suggestion-title {
        font-size: 0.8rem;
        font-weight: 500;
        color: #e0e0e0;
    }
    
    .suggestion-added {
        background: #2d4a2d !important;
        border-color: #4a7c59 !important;
    }
    
    .warning-container, .info-container {
        padding: 0.6rem;
        border-radius: 4px;
        margin: 0.3rem 0;
        font-size: 0.85rem;
    }
    
    .warning-container {
        background: #4a3d2d;
        border: 1px solid #7c6539;
        color: #f39c12;
    }
    
    .action-buttons {
        margin-top: 0.8rem;
        padding-top: 0.6rem;
        border-top: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)