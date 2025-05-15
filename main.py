import streamlit as st
import uuid
from app.chatbot import build_qa_chain
from app.document_loader import load_and_split_pdf

st.title("📄 Gemini RAG Chatbot + Form Agent")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

uploaded = st.file_uploader("Upload your document", type="pdf")
if uploaded:
    if "qa_chain" not in st.session_state:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded.getbuffer())
        chunks = load_and_split_pdf("temp.pdf")
        st.session_state.qa_chain = build_qa_chain(chunks)
        st.success("Document loaded!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if query := st.chat_input("Ask me anything from the document"):
    if not uploaded:
        st.warning("Please upload a document first")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    
    # Get response with proper history handling
    response = st.session_state.qa_chain.invoke(
        {"input": query, "chat_history": st.session_state.messages},
        config={"configurable": {"session_id": st.session_state.session_id}}
    )
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})