import streamlit as st
from app import app


def login_page():
    """
    Displays the login form and handles authentication.
    """
    st.set_page_config(page_title="CoXPRT Login", layout="centered")
    
    # Custom CSS to style the login page
    st.markdown("""
    <style>
    .stApp {
        background-color: #e4e4e4;
    }
    .login-card {
        background-color: white;
        padding: 40px;
        border-radius: 1rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        max-width: 450px;
        margin: auto;
    }
    .login-card .text-center { text-align: center; }
    .login-card h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-top: 20px;
    }
    .login-card p.subheader {
        color: #000000;
        font-size: 1.125rem;
        font-weight: 500;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .login-card p.description {
        color: #000000;
        line-height: 1.6;
        text-align: center;
        margin-bottom: 30px;
    }
    div.stButton > button {
        background-color: #599cd4;
        color: white;
        border-radius: 0.5rem;
        padding: 10px 20px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        opacity: 0.9;
        background-color: #599cd4;
        color: white;
    }
    .login-form-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 0.5rem;
        margin-top: 20px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():

        # Logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
    "https://static.wixstatic.com/media/cb6b3d_5c8f2b020ebe48b69bc8c163cc480156~mv2.png/v1/fill/w_60,h_60,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/GrowthSutra%20Logo.png",
    width=200,  # make it bigger
)

        # Force text colors
        st.markdown(
            """
            <style>
                h1 {
                    color: black !important;
                }
                .subheader {
                    color: #333 !important;
                }
                .description {
                    color: #555 !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<h1>CoXPRT</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">AI Automated Sales Proposal Generator</p>', unsafe_allow_html=True)
        st.markdown('<p class="description">Transform your sales process with intelligent proposal automation. Generate winning, personalized sales proposals in minutes.</p>', unsafe_allow_html=True)
        
        # Show login button or form based on state
        if not st.session_state.get('show_login_form', False):
            if st.button("Login", use_container_width=True):
                st.session_state['show_login_form'] = True
                st.rerun()
        else:
            # Login Form in a styled container
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Login", use_container_width=True)
                with col2:
                    cancel = st.form_submit_button("Cancel", use_container_width=True)

                if submitted:
                    dummy_email = 'test@coxprt.com'
                    dummy_pass = 'password123'
                    if email == dummy_email and password == dummy_pass:
                        st.session_state['logged_in'] = True
                        st.session_state['show_login_form'] = False
                        st.rerun()
                    else:
                        st.error("Invalid email or password. Please try again.")
                
                if cancel:
                    st.session_state['show_login_form'] = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """
    Main function to control the application flow based on session state.
    """
    # Check if 'logged_in' is in the session state and is True
    if st.session_state.get('logged_in', False):
        app()
    else:
        # Show the login page (which now includes the initial view with just the button)
        login_page()

if __name__ == "__main__":
    main()