import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

def get_response(user_input):
    return "I don't know"

# Layout
st.set_page_config(page_title="Chat with websites")
st.markdown("""
    <h1 style='text-align: center; font-size: 36px;'>Virtual HDR Manager</h1>
    <h2 style='text-align: center; font-size: 24px;'>School of Computing Technologies - RMIT University</h2>
    """, unsafe_allow_html=True)

# Persistent storage for messages
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello I am your virtual HDR manager. How can I help you?")
    ]
    
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
