# # utils
#
# import re
# from typing import Any
#
#
# def get_file_id(data: str) -> tuple[Any, bool]:
#     match = re.search(r'src="([^"]+)"', data)
#     if match:
#         return match.group(1), True
#     else:
#         return data, False
#
# #gigachat_api
#
# import streamlit as st
# import requests
# from requests.auth import HTTPBasicAuth
#
# CLIENT_ID = st.secrets['CLIENT_ID']
# SECRET = st.secrets['SECRET']
#
# # curl -L -X POST 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth' \
# # -H 'Content-Type: application/x-www-form-urlencoded' \
# # -H 'Accept: application/json' \
# # -H 'RqUID: ee5e29f9-22f1-429b-808d-4c9110df93cd' \
# # -H 'Authorization: Basic <Authorization key>' \
# # --data-urlencode 'scope=GIGACHAT_API_PERS'
#
# def get_access_token():
#     url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json',
#         'RqUID': 'dd94ede1-310f-482c-af6c-efa342e2ab89',
#     }
#     payload = {"scope": "GIGACHAT_API_PERS"}
#
#     res = requests.post(
#         url,
#         headers=headers,
#         auth=HTTPBasicAuth(CLIENT_ID, SECRET),
#         data=payload,
#         verify=False
#     )
#     try:
#         access_token = res.json()['access_token']
#     except Exception as e:
#         raise RuntimeError(f"Не удалось получить токен: {e}")
#     return access_token
#
# def get_image(file_id: str, access_token: str):
#     url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{file_id}/content"
#
#     payload = {}
#     headers = {
#         'Accept': 'application/jpg',
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     response = requests.get(url, headers=headers, data=payload, verify=False)
#     return response.content
#
#
# def send_prompt(msg: str, access_token: str):
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#     payload = {
#         "model": 'GigaChat',
#         "messages": [
#             {"role": "user",
#              "content": msg}
#         ],
#         "stream": False,
#         "update_interval": 0
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }
#     resp = requests.post(url, headers=headers, json=payload, verify=False)
#     return resp.json()['choices'][0]['message']['content']
#
#
#
#
# # main.py
#
# import streamlit as st
#
# st.title('PoliteGPT')
#
#
# if "access_token" not in st.session_state:
#     try:
#         st.session_state.access_token = get_access_token()
#     except Exception as e:
#         st.toast(e)
#
# if "messages" not in st.session_state:
#     st.session_state.messages = [{'role': 'ai', 'content':
#         'Добрый день. Ты можешь интересоваться всем, чем угодно. Главное, будь вежлив :) ...'}]
#
# for msg in st.session_state.messages:
#     st.chat_message(msg['role']).write(msg['content'])
#
# if user_prompt := st.chat_input():
#     st.chat_message('user').write(user_prompt)
#     st.session_state.messages.append({'role': 'user', 'content': user_prompt})
#
#     with st.spinner('Думаю...'):
#         # Безопасный доступ к токену:
#         access_token = st.session_state.get("access_token", None)
#         if access_token is not None:
#             response = send_prompt(user_prompt, access_token)
#             st.session_state.messages.append({'role': 'ai', 'content': response})
#             st.chat_message('ai').write(response)
#         else:
#             st.toast("Ошибка: отсутствует access_token, попробуйте перезапустить приложение.")
#
