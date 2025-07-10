from app import *

def show_lock_confirmation_popup(tab_index):
    """Show a compact and elegant confirmation dialog for locking a tab"""
    tab_names = ["Client Information", "Seller Information", "Project Specifications", "Generate Proposal"]
    
    with stylable_container(
        f"confirmation_popup_{tab_index}",
        css_styles="""
        div[data-testid="stBlock"] {
            position: fixed !important;
            top: 25% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            z-index: 9999 !important;
            background: #fff5f5 !important;
            border: 1px solid #e74c3c !important;
            border-radius: 10px !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2) !important;
            width: 460px !important;
            height: 180px !important;
            padding: 20px 25px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
        }
        div[data-testid="stBlock"]:before {
            content: '' !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.4) !important;
            z-index: -1 !important;
        }
        """,
    ):
        # Message Header
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="margin: 0; font-size: 16px; font-weight: 600; color: #c53030;">
                    ⚠️ Lock <span style="color: black;">"{tab_names[tab_index]}"</span> tab?
                </p>
                <p style="font-size: 13px; color: #4a5568; margin-top: 8px;">
                    You won't be able to edit it after locking.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Buttons inside same container
        with stylable_container(
            f"button_row_{tab_index}",
            css_styles="""
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                justify-content: space-between !important;
                margin-top: 10px !important;
            }
            button {
                padding: 8px 18px !important;
                font-size: 14px !important;
                border-radius: 6px !important;
                font-weight: 500 !important;
                width: 48% !important;
            }
            button:first-child {
                background-color: #f7fafc !important;
                color: #4a5568 !important;
                border: 1px solid #cbd5e0 !important;
            }
            button:first-child:hover {
                background-color: #edf2f7 !important;
                transform: translateY(-1px) !important;
            }
            button:last-child {
                background-color: #e74c3c !important;
                color: white !important;
                border: 1px solid #e74c3c !important;
            }
            button:last-child:hover {
                background-color: #c53030 !important;
                border-color: #c53030 !important;
                transform: translateY(-1px) !important;
            }
            """,
        ):
            col1, col2 = st.columns(2, gap="small")

            with col1:
                if st.button("Cancel", key=f"cancel_lock_{tab_index}"):
                    if f"show_confirmation_{tab_index}" in st.session_state:
                        del st.session_state[f"show_confirmation_{tab_index}"]
                    st.rerun()

            with col2:
                if st.button("Lock & Continue", key=f"confirm_lock_{tab_index}"):
                    if f"show_confirmation_{tab_index}" in st.session_state:
                        del st.session_state[f"show_confirmation_{tab_index}"]
                    st.session_state.locked_tabs.add(tab_index)
                    st.session_state.active_tab = tab_index + 1
                    st.session_state.highest_reached_tab = max(
                        st.session_state.highest_reached_tab, st.session_state.active_tab
                    )
                    st.rerun()

    return True
show_lock_confirmation_popup()