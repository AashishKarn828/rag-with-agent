import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Did you load your .env?")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.4)
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def build_qa_chain(docs):
    vectordb = FAISS.from_documents(docs, embedding)
    retriever = vectordb.as_retriever()

    # Create a prompt template
    system_prompt = (
        "Use the given context to answer the question. "
        "If you don't know the answer, say you don't know. "
        "Use three sentence maximum and keep the answer concise. "
        "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create the document chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    # Create the retrieval chain
    chain = create_retrieval_chain(retriever, question_answer_chain)
    # chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain
