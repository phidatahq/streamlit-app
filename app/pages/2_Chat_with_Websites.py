from typing import List

import streamlit as st
from phi.conversation import Conversation
from phi.knowledge.website import WebsiteKnowledgeBase

from app.openai_key import get_openai_key
from app.password import check_password
from app.reload import reload_button
from app.user_name import get_user_name
from llm.conversations.website_auto import get_website_auto_conversation
from llm.conversations.website_rag import get_website_rag_conversation
from utils.log import logger


st.title(":snowman: Chat with Websites")


def restart_conversation():
    st.session_state["website_conversation"] = None
    st.session_state["website_conversation_id"] = None
    st.rerun()


def main() -> None:
    # Get users OpenAI API key
    get_openai_key()

    # Get user name
    user_name = get_user_name()
    if user_name:
        st.sidebar.info(f":technologist: User: {user_name}")
    else:
        st.write(":technologist: Please enter a username")
        return

    # Get conversation type
    website_conversation_type = st.sidebar.selectbox("Conversation Type", options=["RAG", "Autonomous"])
    # Set conversation_type in session state
    if "website_conversation_type" not in st.session_state:
        st.session_state["website_conversation_type"] = website_conversation_type
    # Restart the conversation if conversation_type has changed
    elif st.session_state["website_conversation_type"] != website_conversation_type:
        st.session_state["website_conversation_type"] = website_conversation_type
        restart_conversation()

    # Get the conversation
    website_conversation: Conversation
    if "website_conversation" not in st.session_state or st.session_state["website_conversation"] is None:
        if st.session_state["website_conversation_type"] == "Autonomous":
            logger.info("---*--- Creating Autonomous Conversation ---*---")
            website_conversation = get_website_auto_conversation(
                user_name=user_name,
                debug_mode=True,
            )
        else:
            logger.info("---*--- Creating RAG Conversation ---*---")
            website_conversation = get_website_rag_conversation(
                user_name=user_name,
                debug_mode=True,
            )
        st.session_state["website_conversation"] = website_conversation
    else:
        website_conversation = st.session_state["website_conversation"]

    # Start conversation and save conversation id in session state
    st.session_state["website_conversation_id"] = website_conversation.start()

    # Check if knowlege base exists
    if website_conversation.knowledge_base and (
        "website_knowledge_base_loaded" not in st.session_state
        or not st.session_state["website_knowledge_base_loaded"]
    ):
        if not website_conversation.knowledge_base.exists():
            loading_container = st.sidebar.info("🧠 Loading knowledge base")
            website_conversation.knowledge_base.load()
            st.session_state["website_knowledge_base_loaded"] = True
            st.sidebar.success("Knowledge Base loaded")
            loading_container.empty()

    # Load messages for existing conversation
    user_chat_history = website_conversation.memory.get_chat_history()
    if len(user_chat_history) > 0:
        logger.debug("Loading chat history")
        st.session_state["messages"] = user_chat_history
    else:
        logger.debug("No chat history found")
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me anything..."}]

    # Prompt for user input
    if prompt := st.chat_input():
        st.session_state["messages"].append({"role": "user", "content": prompt})

    # Display existing chat messages
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is from a user, generate a new response
    last_message = st.session_state["messages"][-1]
    if last_message.get("role", "") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in website_conversation.chat(question):
                response += delta
                resp_container.markdown(response)

            st.session_state["messages"].append({"role": "assistant", "content": response})

    if st.sidebar.button("New Conversation"):
        restart_conversation()

    if website_conversation.knowledge_base:
        if st.sidebar.button("Update Knowledge Base"):
            website_conversation.knowledge_base.load(recreate=False)
            st.session_state["knowledge_base_exists"] = True
            st.sidebar.success("Knowledge base updated")

        if st.sidebar.button("Recreate Knowledge Base"):
            website_conversation.knowledge_base.load(recreate=True)
            st.session_state["knowledge_base_exists"] = True
            st.sidebar.success("Knowledge base recreated")

    if st.sidebar.button("Auto Rename"):
        website_conversation.auto_rename()

    # Add websites to knowledge base
    website_knowledge_base: WebsiteKnowledgeBase = website_conversation.knowledge_base  # type: ignore
    if website_knowledge_base:
        website_url = st.sidebar.text_input("Add Website to Knowledge Base")
        if website_url != "":
            if website_url not in website_knowledge_base.urls:
                website_knowledge_base.urls.append(website_url)
                loading_container = st.sidebar.info(f"🧠 Loading {website_url}")
                website_knowledge_base.load()
                st.session_state["website_knowledge_base_loaded"] = True
                loading_container.empty()

    if website_conversation.storage:
        all_website_conversation_ids: List[str] = website_conversation.storage.get_all_conversation_ids(
            user_name=user_name
        )
        new_website_conversation_id = st.sidebar.selectbox(
            "Conversation ID", options=all_website_conversation_ids
        )
        if st.session_state["website_conversation_id"] != new_website_conversation_id:
            logger.debug(f"Loading conversation {new_website_conversation_id}")
            if st.session_state["website_conversation_type"] == "Autonomous":
                logger.info("---*--- Loading as Autonomous Conversation ---*---")
                st.session_state["website_conversation"] = get_website_auto_conversation(
                    user_name=user_name,
                    conversation_id=new_website_conversation_id,
                    debug_mode=True,
                )
            else:
                logger.info("---*--- Loading as RAG Conversation ---*---")
                st.session_state["website_conversation"] = get_website_rag_conversation(
                    user_name=user_name,
                    conversation_id=new_website_conversation_id,
                    debug_mode=True,
                )
            st.rerun()

    website_conversation_name = website_conversation.name
    if website_conversation_name:
        st.sidebar.write(f":thread: {website_conversation_name}")

    # Show reload button
    reload_button()


if check_password():
    main()
