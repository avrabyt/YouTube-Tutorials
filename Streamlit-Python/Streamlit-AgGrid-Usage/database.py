import streamlit as st
from google.oauth2 import service_account
import gspread

def send_to_database(res):
    # Create a Google Authentication connection object
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
    gc = gspread.authorize(credentials)
    sh = gc.open("AgGrid-Database")
    worksheet = sh.worksheet("Sheet1") #
    my_bar = st.progress(0)
    for ind in res.index:
        percent_complete = (ind+1)/len(res) 
        my_bar.progress(percent_complete)
        values_list = worksheet.col_values(1)
        length_row = len(values_list)
        worksheet.update_cell(length_row+1, 1, res['Type'][ind])
        worksheet.update_cell(length_row+1, 2, str(res['Quantity'][ind]))
        worksheet.update_cell(length_row+1, 3, str(res['Price'][ind]))
       
    return st.success("Updated to Database ", icon="✅")       