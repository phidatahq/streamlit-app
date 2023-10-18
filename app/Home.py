import streamlit as st

from app.password import check_password

st.set_page_config(
    page_title="LLM Apps",
    page_icon=":snowman:",
)


st.title(":snowman: LLM Apps")


def main() -> None:
    st.markdown("## Select App from the sidebar:")
    st.markdown("### 1. Chat with PDFs")
    st.markdown("### 2. Chat with Websites")

    st.sidebar.success("Select App from above")


if check_password():
    main()
