# Modules
import streamlit as st
import requests

# Notion Token
token = '' 
databaseID = ''

# Headers
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

# Functions
# Database Query
def queryDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    return res , data

# Database retrieve
def retrieveDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}"
    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    return res , data

# Calling the function
res , data = queryDatabase(databaseID,headers)

# Dump onto Streamlit
st.write(res.status_code)
st.json(data)
