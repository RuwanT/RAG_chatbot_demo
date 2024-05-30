import streamlit as st

# Persistent storage for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Layout
st.markdown("""
    <h1 style='text-align: center; font-size: 36px;'>Virtual HDR Manager</h1>
    <h2 style='text-align: center; font-size: 24px;'>School of Computing Technologies - RMIT University</h2>
    """, unsafe_allow_html=True)


    
# Textbox for user input
user_input = st.text_input('How can I help you:')

# Send button
if st.button('Send'):
    # Add the user input to the messages list
    st.session_state['messages'].append(user_input)
    # Clear the input box after sending the message
    st.session_state['user_input'] = ''

# Display area for messages
st.write('Message History:')
for message in st.session_state['messages']:
    # st.write(message)
    st.markdown(f'<div style="border: 1px solid #ccc; padding: 10px;">{message}</div>', unsafe_allow_html=True)
    # st.text_area('Answer', message, key=message, label_visibility='collapsed')
