import requests 
import os
from time import sleep
import streamlit as st

url = f"https://discord.com/api/webhooks/{st.secrets['TOKEN_WEBHOOK']}"

def main(msg):
    global url
    data = {
    "content" : f"{msg}",
    "username" : "LOG_STREMILIT"
    }
    result = requests.post(url, json = data)
    sleep(0.5)    
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('erro')
        sleep(1)
    else: pass

if __name__ == "__main__":
    main("teste")
