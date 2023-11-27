from typing import List

import streamlit as st
from phi.conversation import Conversation
from phi.document import Document
from phi.document.reader.pdf import PDFReader

from app.openai_key import get_openai_key
from app.password import check_password
from app.reload import reload_button
from app.user_name import get_user_name
from llm.conversations.pdf_auto import get_pdf_auto_conversation
from llm.conversations.pdf_rag import get_pdf_rag_conversation
from utils.log import logger


st.title(":snowman: Chat with PDFs")
st.markdown('<a href="https://github.com/phidatahq/phidata"><h4>by phidata</h4></a>', unsafe_allow_html=True)


def restart_conversation():
    st.session_state["pdf_conversation"] = None
    st.session_state["pdf_conversation_id"] = None
    st.session_state["file_uploader_key"] += 1
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
    pdf_conversation_type = st.sidebar.selectbox("Conversation Type", options=["RAG", "Autonomous"])
    # Set conversation_type in session state
    if "pdf_conversation_type" not in st.session_state:
        st.session_state["pdf_conversation_type"] = pdf_conversation_type
    # Restart the conversation if conversation_type has changed
    elif st.session_state["pdf_conversation_type"] != pdf_conversation_type:
        st.session_state["pdf_conversation_type"] = pdf_conversation_type
        restart_conversation()

    # Get the conversation
    pdf_conversation: Conversation
    if "pdf_conversation" not in st.session_state or st.session_state["pdf_conversation"] is None:
        if st.session_state["pdf_conversation_type"] == "Autonomous":
            logger.info("---*--- Creating Autonomous Conversation ---*---")
            pdf_conversation = get_pdf_auto_conversation(
                user_name=user_name,
                debug_mode=True,
            )
        else:
            logger.info("---*--- Creating RAG Conversation ---*---")
            pdf_conversation = get_pdf_rag_conversation(
                user_name=user_name,
                debug_mode=True,
            )
        st.session_state["pdf_conversation"] = pdf_conversation
    else:
        pdf_conversation = st.session_state["pdf_conversation"]

    # Start conversation and save conversation id in session state
    st.session_state["pdf_conversation_id"] = pdf_conversation.start()

    # Check if knowlege base exists
    if pdf_conversation.knowledge_base and (
        "pdf_knowledge_base_loaded" not in st.session_state
        or not st.session_state["pdf_knowledge_base_loaded"]
    ):
        if not pdf_conversation.knowledge_base.exists():
            logger.info("Knowledge base does not exist")
            loading_container = st.sidebar.info("🧠 Loading knowledge base")
            pdf_conversation.knowledge_base.load()
            st.session_state["pdf_knowledge_base_loaded"] = True
            st.sidebar.success("Knowledge base loaded")
            loading_container.empty()

    # Load messages for existing conversation
    user_chat_history = pdf_conversation.memory.get_chat_history()
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
    if last_message.get("role") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in pdf_conversation.chat(question):
                response += delta
                resp_container.markdown(response)

            st.session_state["messages"].append({"role": "assistant", "content": response})

    if st.sidebar.button("New Conversation"):
        restart_conversation()

    if pdf_conversation.knowledge_base:
        if st.sidebar.button("Update Knowledge Base"):
            pdf_conversation.knowledge_base.load(recreate=False)
            st.session_state["pdf_knowledge_base_loaded"] = True
            st.sidebar.success("Knowledge base updated")

        if st.sidebar.button("Recreate Knowledge Base"):
            pdf_conversation.knowledge_base.load(recreate=True)
            st.session_state["pdf_knowledge_base_loaded"] = True
            st.sidebar.success("Knowledge base recreated")

    if st.sidebar.button("Auto Rename"):
        pdf_conversation.auto_rename()

    # Upload PDF
    if pdf_conversation.knowledge_base:
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

        uploaded_file = st.sidebar.file_uploader(
            "Upload PDF",
            type="pdf",
            key=st.session_state["file_uploader_key"],
        )
        if uploaded_file is not None:
            alert = st.sidebar.info("Processing PDF...", icon="ℹ️")
            pdf_name = uploaded_file.name.split(".")[0]
            if f"{pdf_name}_uploaded" not in st.session_state:
                reader = PDFReader()
                pdf_documents: List[Document] = reader.read(uploaded_file)
                if pdf_documents:
                    pdf_conversation.knowledge_base.load_documents(pdf_documents)
                else:
                    st.sidebar.error("Could not read PDF")
                st.session_state[f"{pdf_name}_uploaded"] = True
            alert.empty()

    if pdf_conversation.storage:
        all_pdf_conversation_ids: List[str] = pdf_conversation.storage.get_all_conversation_ids(
            user_name=user_name
        )
        new_pdf_conversation_id = st.sidebar.selectbox("Conversation ID", options=all_pdf_conversation_ids)
        if st.session_state["pdf_conversation_id"] != new_pdf_conversation_id:
            logger.debug(f"Loading conversation {new_pdf_conversation_id}")
            if st.session_state["pdf_conversation_type"] == "Autonomous":
                logger.info("---*--- Loading as Autonomous Conversation ---*---")
                st.session_state["pdf_conversation"] = get_pdf_auto_conversation(
                    user_name=user_name,
                    conversation_id=new_pdf_conversation_id,
                    debug_mode=True,
                )
            else:
                logger.info("---*--- Loading as RAG Conversation ---*---")
                st.session_state["pdf_conversation"] = get_pdf_rag_conversation(
                    user_name=user_name,
                    conversation_id=new_pdf_conversation_id,
                    debug_mode=True,
                )
            st.rerun()

    pdf_conversation_name = pdf_conversation.name
    if pdf_conversation_name:
        st.sidebar.write(f":thread: {pdf_conversation_name}")

    # Show reload button
    reload_button()


if check_password():
    main()
