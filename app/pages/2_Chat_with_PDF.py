from typing import List

import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant

from app.get_openai_key import get_openai_key
from app.sidebar_reload import show_reload
from llm.schemas import Message
from llm.settings import llm_settings

# -*- List of pdfs in knowledge base
pdfs = {
    "Airbnb 2020 10K": "data/Airbnb_2020_10k.pdf",
}


def sidebar() -> None:
    """Sidebar component"""

    # Get the data source
    input_data_source = st.sidebar.radio(
        label="## Select Data Source", options=["PDF", "Upload"]
    )
    if input_data_source is not None:
        st.session_state["input_data_source"] = input_data_source

    if input_data_source == "PDF":
        pdf_location = st.sidebar.selectbox("Select PDF", pdfs.keys())
        if pdf_location is not None and pdf_location in pdfs:
            st.session_state["pdf_location"] = pdfs[pdf_location]

    if input_data_source == "Upload":
        uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
        if uploaded_file is not None:
            st.session_state["uploaded_file"] = uploaded_file

    # Button to read the PDF
    if st.sidebar.button("Read PDF"):
        input_data_source = st.session_state.get("input_data_source", None)

        if input_data_source == "PDF":
            from langchain.document_loaders import PyPDFLoader

            pdf_location = st.session_state["pdf_location"]
            # Load the PDF
            if pdf_location is not None:
                loader = PyPDFLoader(str(pdf_location))
                loaded_pdf: List[Document] = loader.load()
                if loaded_pdf is not None:
                    st.session_state["loaded_pdf"] = loaded_pdf
                    st.session_state["pdf_loaded"] = True
                    st.sidebar.write(f"🦆 PDF: {pdf_location}")

                # Chunk the loaded PDF
                if loaded_pdf is not None:
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=500, chunk_overlap=0
                    )
                    chunked_pdf_documents = text_splitter.split_documents(loaded_pdf)
                    st.session_state["chunked_pdf_documents"] = chunked_pdf_documents
                    st.session_state["pdf_chunked"] = True
                    st.sidebar.write(
                        f"Chunked PDF length: {len(chunked_pdf_documents)}"
                    )

        if input_data_source == "Upload":
            from pypdf import PdfReader

            uploaded_file = st.session_state["uploaded_file"]
            # Load the PDF
            if uploaded_file is not None:
                pdf_reader = PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()

                if pdf_text is not None:
                    st.session_state["pdf_text"] = pdf_text
                    st.session_state["pdf_loaded"] = True
                    st.sidebar.write(f"🦆 PDF: {uploaded_file.name}")

                # Chunk the loaded PDF
                if pdf_text is not None:
                    text_splitter = RecursiveCharacterTextSplitter(
                        separators=["\n"],
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len,
                    )
                    chunked_pdf_text = text_splitter.split_text(pdf_text)
                    st.session_state["chunked_pdf_text"] = chunked_pdf_text
                    st.session_state["pdf_chunked"] = True
                    st.sidebar.write(f"Chunked PDF length: {len(chunked_pdf_text)}")


def main() -> None:
    """Main App"""

    # Check if OpenAI API key is set
    openai_key = get_openai_key()
    if openai_key is None or openai_key == "" or openai_key == "sk-***":
        st.write("🔑  OpenAI API key not set")
        return

    if "pdf_chunked" not in st.session_state:
        st.write("🦆 Waiting for PDF")
        return

    # Create the retriever
    if st.session_state["pdf_chunked"] is True:
        qdrant = None
        embeddings = OpenAIEmbeddings()
        if "retriever" not in st.session_state:
            st.sidebar.markdown("Creating the retriever...")
            if (
                "input_data_source" in st.session_state
                and st.session_state["input_data_source"] == "PDF"
            ):
                chunked_pdf_documents = st.session_state["chunked_pdf_documents"]
                qdrant = Qdrant.from_documents(
                    documents=chunked_pdf_documents,
                    embedding=embeddings,
                    location=":memory:",  # Local mode with in-memory storage only
                    collection_name="chat_with_pdf",
                )
            elif (
                "input_data_source" in st.session_state
                and st.session_state["input_data_source"] == "Upload"
            ):
                chunked_pdf_text = st.session_state["chunked_pdf_text"]
                qdrant = Qdrant.from_texts(
                    texts=chunked_pdf_text,
                    embedding=embeddings,
                    location=":memory:",  # Local mode with in-memory storage only
                    collection_name="chat_with_pdf",
                )

            if qdrant is not None:
                retriever = qdrant.as_retriever()
                st.session_state["retriever"] = retriever
                st.sidebar.markdown("🤖  Retriever created")
        else:
            st.sidebar.markdown("🤖  Retriever available")

    # Create the QA chain
    if "retriever" in st.session_state:
        if "qa" not in st.session_state:
            st.sidebar.markdown("Creating the chain...")
            qa = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(
                    temperature=llm_settings.default_temperature,
                    model=llm_settings.gpt_4,
                ),
                retriever=st.session_state["retriever"],
                condense_question_llm=ChatOpenAI(
                    temperature=llm_settings.default_temperature,
                    model=llm_settings.chat_gpt,
                ),
            )
            st.session_state["qa"] = qa
            st.sidebar.markdown("🔗  Chain created")
        else:
            st.sidebar.markdown("🔗  Chain available")

    # Show reload button
    show_reload()

    if "qa" in st.session_state:
        # User query
        user_query = st.text_input(
            "Ask a question",
            placeholder="When did Airbnb IPO?",
            key="user_query",
        )

        if user_query:
            # Create a session variable to store the conversation
            if "conversation" not in st.session_state:
                st.session_state["conversation"] = []
            # Create a session variable to store the chat history
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            # Store the user query in the conversation
            st.session_state["conversation"].append(
                Message(role="user", content=user_query)
            )

            # Ask the question
            query_result = st.session_state["qa"](
                {
                    "question": user_query,
                    "chat_history": st.session_state["chat_history"],
                }
            )

            # Get the answer
            query_answer = (
                query_result["answer"]
                if "answer" in query_result
                else "Could not understand, please try again"
            )

            # Store the answer in the conversation and chat_history
            st.session_state["conversation"].append(
                Message(role="assistant", content=query_answer)
            )
            st.session_state["chat_history"].append((user_query, query_answer))

    if "conversation" in st.session_state:
        for i in range(len(st.session_state["conversation"]) - 1, -1, -1):
            msg: Message = st.session_state["conversation"][i]
            if msg.role == "user":
                message(msg.content, is_user=True, key=str(i))
            elif msg.role == "assistant":
                message(msg.content, key=str(i))
            elif msg.role == "system":
                message(msg.content, key=str(i), seed=42)


st.set_page_config(page_title="Knowledge Base Demo", page_icon="🔎", layout="wide")
st.markdown("## Build a chat product using your own data")

sidebar()
main()
