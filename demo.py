import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# read API keys for Pinecone and OpenAI
#   Should have keys saved in .env file
success_env = load_dotenv(find_dotenv())
    


def get_vectorstore():
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = PineconeVectorStore(index_name="hdr-manager-rmit", embedding=embedding)
    
    return vectorstore

def get_context_retriever_chain(vectorstore):
    llm = ChatOpenAI()
    
    retriever = vectorstore.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain
    
def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the users question based on the following context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)
    
def get_response(user_query):
    
    retriver_chain = get_context_retriever_chain(st.session_state.vector_store)
    rag_chain = get_conversational_rag_chain(retriver_chain)
    
    response = rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_query
    })
    return response['answer']

# Layout
st.set_page_config(page_title="Chat with websites")
st.markdown("""
    <h1 style='text-align: center; font-size: 36px;'>Virtual HDR Manager</h1>
    <h2 style='text-align: center; font-size: 24px;'>School of Computing Technologies - RMIT University</h2>
    """, unsafe_allow_html=True)



with st.sidebar:
    st.header("Settings")
    rmit_email = st.text_input("RMIT email:")
    
if rmit_email is None or rmit_email=="":
    st.info("Please enter an RMIT email in the sidebar:")
else:
    # Persistent storage for messages
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello I am your virtual HDR manager. How can I help you?")
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore()
        
    # Textbox for user input
    user_query = st.chat_input('Type your question here...')
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
        
        # retrieved_documents = retriver_chain.invoke({
        #     "chat_history": st.session_state.chat_history,
        #     "input": user_query
        # })

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
