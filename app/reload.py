import streamlit as st


def reload_button():
    """Sidebar component to show reload button"""

    st.sidebar.markdown("---")
    if st.sidebar.button("Reload Session"):
        st.session_state.clear()
        st.rerun()
