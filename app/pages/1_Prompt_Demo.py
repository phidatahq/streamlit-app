from typing import List

import openai
import streamlit as st

from app.get_openai_key import get_openai_key
from app.sidebar_reload import show_reload
from llm.schemas import Message
from llm.settings import llm_settings


def sidebar():
    """Sidebar component"""

    # Step 1: Get OpenAI API key
    openai_key = get_openai_key()
    if openai_key is None or openai_key == "" or openai_key == "sk-***":
        st.write("🔑  OpenAI API key not set")

    st.sidebar.markdown("## Status")
    if (
        "OPENAI_API_KEY" in st.session_state
        and st.session_state["OPENAI_API_KEY"] != ""
    ):
        st.sidebar.markdown("🔑  OpenAI API key set")

    # Show reload button
    show_reload()


def main() -> None:
    """Main App"""

    prompt = st.text_input(
        "Ask LLM a question",
        placeholder="Write a story about an AI named Phi.",
        key="input",
    )

    if prompt:
        # -*- Create a System Prompt
        system_prompt = (
            "You are a helpful assistant that helps customers answer questions."
        )

        # -*- Add the System Prompt to the conversation
        messages: List = []
        system_message = Message(role="system", content=system_prompt)
        messages.append(system_message.message())

        # -*- Add the user query to the conversation
        user_message = Message(role="user", content=prompt)
        messages.append(user_message.message())

        # -*- Generate completion
        completion_result = openai.ChatCompletion.create(
            model=llm_settings.chat_gpt,
            messages=messages,
            max_tokens=llm_settings.default_max_tokens,
            temperature=llm_settings.default_temperature,
        )
        result = completion_result["choices"][0]["message"]["content"]

        # -*- Write result
        st.write(result)


st.set_page_config(page_title="LLM Prompt Demo", page_icon="🔎", layout="wide")
st.markdown("## Build a prompt product using your own data")

sidebar()
main()
