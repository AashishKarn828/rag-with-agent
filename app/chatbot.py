import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory



load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Did you load your .env?")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.4)
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def build_qa_chain(docs):
    vectordb = FAISS.from_documents(docs, embedding)
    retriever = vectordb.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer questions based on the context. Be concise. Context: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
    


    retrieval_chain = RunnableMap({
        "context": lambda x: retriever.invoke(x["input"]),
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"]
    })

    retrieval_chain = retrieval_chain | prompt | llm | StrOutputParser()

    store = {}
    
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]
    
    # Create the chain with message history
    conversational_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    
    return conversational_chain