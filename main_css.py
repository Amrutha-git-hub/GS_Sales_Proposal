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
    
    /* REMOVED CONFLICTING BUTTON STYLES - Let app.py handle tab buttons */
    
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


app_css = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global styles - 75% screen width with equal margins */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

/* Container with 75% width and centered positioning */
.block-container {
    padding: 1rem 0 2rem 0;
    max-width: 75% !important;
    width: 75% !important;
    margin: 0 auto !important;
    left: 12.5% !important;
    right: 12.5% !important;
}

/* Main container - 75% width centered */
.main-container {
    width: 100%;
    min-height: 100vh;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Header styling - Full width within container */
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

/* Content area - Full width within the 75% container */
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

/* Full-width grid layouts for content within the 75% container */
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

/* Footer styling - Full width within container */
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
    .block-container {
        max-width: 95% !important;
        width: 95% !important;
        left: 2.5% !important;
        right: 2.5% !important;
    }
    
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
"""