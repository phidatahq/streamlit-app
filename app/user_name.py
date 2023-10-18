from typing import Optional

import streamlit as st


def get_user_name() -> Optional[str]:
    """Sidebar component to get username"""

    # Get user_name from user if not in session state
    if "user_name" not in st.session_state:
        username_input_container = st.sidebar.empty()
        username = username_input_container.text_input(":technologist: Enter username")
        if username != "":
            st.session_state["user_name"] = username
            username_input_container.empty()

    # Get user_name from session state
    user_name = st.session_state.get("user_name")
    return user_name
