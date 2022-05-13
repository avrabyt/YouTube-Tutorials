import streamlit as st
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd

# Load data
@st.cache
def data_upload():
    df = pd.read_csv("covid-variants.csv")
    return df
st.subheader("Data")
df = data_upload()
# Grid 1 - Display
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple',use_checkbox=True)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_pagination(enabled=True)
gridoptions = gd.build()
grid1 = AgGrid(df,gridOptions=gridoptions,
                    update_mode= GridUpdateMode.SELECTION_CHANGED)

sel_row = grid1["selected_rows"] # Type -> List
df_sel = pd.DataFrame (sel_row) # Convert list to dataframe
st.subheader("Output")
# Grid 2 - Highlight
grid2 = AgGrid(df_sel)