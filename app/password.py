from os import getenv
import streamlit as st


def check_password() -> bool:
    """Component to checks if a password entered by the user is correct.
    To use this component, set the environment variable `APP_PASSWORD`.

    Returns:
        bool: `True` if the user had the correct password.
    """

    app_password = getenv("APP_PASSWORD")
    if app_password is None:
        return True

    def check_first_run_password():
        """Checks whether a password entered on the first run is correct."""

        if "first_run_password" in st.session_state:
            password_to_check = st.session_state["first_run_password"]
            if password_to_check == app_password:
                st.session_state["password_correct"] = True
                # don't store password
                del st.session_state["first_run_password"]
            else:
                st.session_state["password_correct"] = False

    def check_updated_password():
        """Checks whether an updated password is correct."""

        if "updated_password" in st.session_state:
            password_to_check = st.session_state["updated_password"]
            if password_to_check == app_password:
                st.session_state["password_correct"] = True
                # don't store password
                del st.session_state["updated_password"]
            else:
                st.session_state["password_correct"] = False

    # First run, show input for password.
    if "password_correct" not in st.session_state:
        st.text_input(
            "Password",
            type="password",
            on_change=check_first_run_password,
            key="first_run_password",
        )
        return False
    # Password incorrect, show input for updated password + error.
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password",
            type="password",
            on_change=check_updated_password,
            key="updated_password",
        )
        st.error("😕 Password incorrect")
        return False
    # Password correct.
    else:
        return True
