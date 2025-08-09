import streamlit as st
from gigachat_api import get_access_token, send_prompt


st.title('PoliteGPT')


if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
    except Exception as e:
        st.toast(e)

if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'ai', 'content':
        'Добрый день. Ты можешь интересоваться всем, чем угодно. Главное, будь вежлив :) ...'}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if user_prompt := st.chat_input():
    st.chat_message('user').write(user_prompt)
    st.session_state.messages.append({'role': 'user', 'content': user_prompt})

    with st.spinner('Думаю...'):
        # Безопасный доступ к токену:
        access_token = st.session_state.get("access_token", None)
        if access_token is not None:
            response = send_prompt(user_prompt, access_token)
            st.session_state.messages.append({'role': 'ai', 'content': response})
            st.chat_message('ai').write(response)
        else:
            st.toast("Ошибка: отсутствует access_token, попробуйте перезапустить приложение.")
