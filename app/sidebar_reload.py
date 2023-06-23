import streamlit as st


def show_reload():
    """Sidebar component to show reload button"""
    st.sidebar.markdown("---")
    if st.sidebar.button("Reload Session"):
        st.session_state.clear()
        st.experimental_rerun()
