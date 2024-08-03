import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv

#from langchain_openai import OpenAIEmbeddings, ChatOpenAI, AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
#from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings

USE_OPENAI = True

# read API keys for Pinecone and OpenAI
#   Should have keys saved in .env file
success_env = load_dotenv(find_dotenv())
    


def get_vectorstore():
    if USE_OPENAI:
        embedding = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-3-small",
            api_version="2023-06-01-preview",
        )
        vector_store_dir = "../hdr-manager-rmit-chroma_db"
    else:
        embedding = MistralAIEmbeddings()
        
        
        
    vectorstore = Chroma(persist_directory=vector_store_dir, 
                             embedding_function=embedding)
    
    return vectorstore

def get_context_retriever_chain(vectorstore):
    if USE_OPENAI:
        llm = AzureChatOpenAI(
            azure_deployment="gpt4",
            api_version="2023-06-01-preview",
        )
    else:
        llm = ChatMistralAI()
    
    retriever = vectorstore.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information most relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain
    
def get_conversational_rag_chain(retriever_chain):
    if USE_OPENAI:
        llm = AzureChatOpenAI(
            azure_deployment="gpt4",
            api_version="2023-06-01-preview",
        )
    else:
        llm = ChatMistralAI()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a administration officer at RMIT university taked with providing accurate information."),
        ("system", "Answer the users question based on the following context:\n\n{context}"),
        ("system", "You should always provide the link to the intranet page where the information was found."),
        ("system", "If the information to answer the question is not found in the context, clearly mention that you dont have that information and ask the user to contact HDR DA for school."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)
    
def get_response(user_query):
    
    # retriver_chain = get_context_retriever_chain(st.session_state.vector_store)
    # rag_chain = get_conversational_rag_chain(retriver_chain)
    
    response = st.session_state.rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_query
    })
    return response['answer']

# Layout
st.set_page_config(page_title="HDR-Assist")
st.markdown("""
    <h1 style='text-align: center; font-size: 36px; margin-bottom: -20px;'>HDR-Assist</h1>
    <h2 style='text-align: center; font-size: 24px; margin-top: -10px;'>Support tool for Higher Degree by Research supervisors</h2>
    """, unsafe_allow_html=True)

    
if "agreed" not in st.session_state:
    
    st.markdown("""
        - Do not enter prompts that contain:
            1. Information that you would not usually share with other people.
            2. Personal, sensitive, and health information about yourself or anyone else. This includes details such as names, student and staff ID numbers, email addresses, phone numbers, dates of birth, and photos.
        - Ensure that you employ critical thinking to evaluate the outputs that you receive, as generative AI applications may at times provide incorrect, biased and inappropriate content.
        - Use of this service must comply with the RMIT [Acceptable Use Standard - Information Technology](https://policies.rmit.edu.au/document/view.php?id=76)
        """, unsafe_allow_html=True)
    
    st.session_state.agreed = st.checkbox('I acknowledge')
    st.button('Start')
    
    
elif (not st.session_state.agreed):
    st.markdown("""
        - Do not enter prompts that contain:
            1. Information that you would not usually share with other people.
            2. Personal, sensitive, and health information about yourself or anyone else. This includes details such as names, student and staff ID numbers, email addresses, phone numbers, dates of birth, and photos.
        - Ensure that you employ critical thinking to evaluate the outputs that you receive, as generative AI applications may at times provide incorrect, biased and inappropriate content.
        - Use of this service must comply with the RMIT [Acceptable Use Standard - Information Technology](https://policies.rmit.edu.au/document/view.php?id=76)
        """, unsafe_allow_html=True)
    
    st.session_state.agreed = st.checkbox('I acknowledge')
    st.button('Start')
        
    
else:
    
    st.markdown("""
        <h3 style='text-align: center; font-size: 18px; border: 2px solid red;'>As an AI chatbot, my role is to assist you in accessing information relevant to HDR. Please ensure the accuracy of the information by consulting the provided intranet links.</h3>
        """, unsafe_allow_html=True)
    # Persistent storage for messages, vector store and retrival/rag chains
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello I am HDR-Assist. How can I help you?")
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore()
        
    if "retriver_chain" not in st.session_state:
        st.session_state.retriver_chain = get_context_retriever_chain(st.session_state.vector_store)

    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = get_conversational_rag_chain(st.session_state.retriver_chain)
        
    # Textbox for user input
    user_query = st.chat_input('Type your question here...')
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)