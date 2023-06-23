import streamlit as st

st.set_page_config(
    page_title="LLM Apps",
    page_icon="🚝",
)

st.markdown("### Select a Demo from the sidebar:")
st.markdown("1. Prompt Demo: Build a prompt product using your own data")
st.markdown("2. Chat with PDF: Build a chat product using your own data")

st.sidebar.success("Select a demo from above")
