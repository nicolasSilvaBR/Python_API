# pip install requests
# pip install pandas
# pip install pyarrow
# pip install openpyxl
# pip install python-dotenv

from dotenv import load_dotenv
import os
import requests
import pandas as pd
import streamlit as st

# Carrega o .env
load_dotenv()

# Acessa o token da variável de ambiente
token = os.getenv('MY_API_TOKEN')
if token is None:
    raise ValueError("No API token provided!")

# Cabeçalho de autenticação
headers = {"Authorization": f"Bearer {token}"}

# URLs da API
url_category = "https://myfin-financial-management.bubbleapps.io/api/1.1/obj/category/"
url_recipient = "https://myfin-financial-management.bubbleapps.io/api/1.1/obj/recipient/"


# Fazendo a solicitação para a primeira URL
def chamar_api_myfinance(url):
    response = requests.get(url, headers=headers)
    return response

# guardar o response de cada chamada da api em uma variavel
response_category = chamar_api_myfinance(url_category)
response_recipient = chamar_api_myfinance(url_recipient)

# navegar no json até onde estão dos dados necessários
category_ajustado_json = response_category.json()['response']['results']
recipient_ajustado_json = response_recipient.json()['response']['results']

#transformar o json ajustado em dataframe com o pandas
df_category = pd.DataFrame(category_ajustado_json,columns=['title', '_id'])
df_recipient = pd.DataFrame(recipient_ajustado_json,columns=['title', '_id','category_ref'])

#salvar o dataframe em .xlxs e .parquet
df_category.to_excel('Category.xlsx', index=False)
df_category.to_parquet('Category.parquet', index=False)

df_recipient.to_excel('Recipient.xlsx', index=False)
df_recipient.to_parquet('Recipient.parquet', index=False)