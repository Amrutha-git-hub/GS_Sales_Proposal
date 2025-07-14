import streamlit as st

@st.dialog("Confirm Tab Lock", width="small")
def show_lock_confirmation_popup(tab_index):
    """Show confirmation dialog for locking a tab using st.dialog"""
    tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
    
    # Ensure tab_index is an integer
    if isinstance(tab_index, str):
        tab_index = int(tab_index)
    
    # Custom CSS for the dialog content
    st.markdown("""
    <style>
    .dialog-content {
        text-align: center;
        padding: 30px 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .dialog-icon {
        font-size: 64px;
        margin-bottom: 25px;
        display: block;
        width: 100%;
        text-align: center;
    }
    
    .dialog-message {
        font-size: 18px;
        color: #2d3748;
        margin-bottom: 15px;
        text-align: center;
        line-height: 1.5;
    }
    
    .dialog-sub-message {
        font-size: 14px;
        color: #718096;
        margin-bottom: 30px;
        text-align: center;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dialog-icon">⚠️</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dialog-message">Are you sure you want to lock the <strong>{tab_names[tab_index]}</strong> tab?</div>', unsafe_allow_html=True)
    st.markdown('<div class="dialog-sub-message">You won\'t be able to modify this tab once it\'s locked.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create button columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cancel", key=f"cancel_lock_{tab_index}", use_container_width=True):
            # Clear confirmation state and close dialog
            if f"show_confirmation_{tab_index}" in st.session_state:
                del st.session_state[f"show_confirmation_{tab_index}"]
            st.rerun()
    
    with col2:
        if st.button("Lock & Continue", key=f"confirm_lock_{tab_index}", type="primary", use_container_width=True):
            # Clear confirmation state
            if f"show_confirmation_{tab_index}" in st.session_state:
                del st.session_state[f"show_confirmation_{tab_index}"]
            
            # Lock the current tab
            if not hasattr(st.session_state, 'locked_tabs'):
                st.session_state.locked_tabs = set()
            st.session_state.locked_tabs.add(tab_index)
            
            # Move to next tab
            st.session_state.active_tab = tab_index + 1
            if not hasattr(st.session_state, 'highest_reached_tab'):
                st.session_state.highest_reached_tab = 0
            st.session_state.highest_reached_tab = max(st.session_state.highest_reached_tab, st.session_state.active_tab)
            
            st.rerun()

# Example usage in your main app
def main():
    st.title("Tab Lock Example")
    
    # Initialize session state
    if 'show_confirmation_1' not in st.session_state:
        st.session_state.show_confirmation_1 = False
    
    # Button to trigger the dialog
    if st.button("Show Lock Confirmation"):
        st.session_state.show_confirmation_1 = True
        st.rerun()
    
    # Show dialog if triggered
    if st.session_state.get('show_confirmation_1', False):
        show_lock_confirmation_popup(1)

# Run the example
if __name__ == "__main__":
    main()