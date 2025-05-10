import streamlit as st
from app.chatbot import build_qa_chain
from app.document_loader import load_and_split_pdf
from app.date_utils import parse_date
from app.form_tools import validate_email_input, validate_name, validate_phone
from app.agent_tools import book_appointment

st.title("📄 Gemini RAG Chatbot + Form Agent")

uploaded = st.file_uploader("Upload your document", type="pdf")
if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.getbuffer())
    chunks = load_and_split_pdf("temp.pdf")
    qa = build_qa_chain(chunks)
    st.success("Document loaded!")

query = st.text_input("Ask me anything from the document:")
if query and uploaded:
    response = qa.invoke({"input": query})
    st.write("🤖", response["answer"])

if st.button("📞 Request Callback"):
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        date_input = st.text_input("Appointment Date (e.g., next Monday)")

        submitted = st.form_submit_button("Book")

        if submitted:
            if all([validate_name(name), validate_email_input(email), validate_phone(phone)]):
                date = parse_date(date_input)
                result = book_appointment.run(name=name, email=email, phone=phone, date=date)
                st.success(result)
            else:
                st.error("Invalid input. Please check name, email, or phone.")
