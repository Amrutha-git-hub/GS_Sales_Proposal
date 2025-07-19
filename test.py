import streamlit as st


def fn1():
    print("fn1")
def fn2():
    print("fn2")


@st.dialog("‼️ Warning")
def show_warning_dialog(message,fn1,fn2):
    """Warning dialog with icon"""
    st.warning(message)
    st.error(message)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Close", key="close_warning", type="primary"):
            fn1()


show_warning_dialog("okdssd",fn1,fn2)