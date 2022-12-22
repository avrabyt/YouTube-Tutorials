import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import glob
# Functions
# Fixing path issue with explicitly (bad practice!)
file = glob.glob('Streamlit-Python/Streamlit-AgGrid-Usage/Data/*', recursive=True)

@st.cache
def data_upload(file):
    df = pd.read_csv(file[0])
    return df

st.header("AgGrid Demo `Part 1` & `Part 2`")
st.sidebar.title("AgGrid Examples")
df = data_upload(file)
if st.checkbox("Show Streamlit Default Dataframe"):
    st.subheader("This is how Default Streamlit Dataframe looks!")
    st.dataframe(data=df)
# st.info(len(df))

_funct = st.sidebar.radio(label="Functions", options = ['Display','Highlight','Delete'])

st.sidebar.markdown('''
                - ## Medium Article : 
                    [**Automate Streamlit Web App using Interactive AgGrid with Google Sheets**](https://medium.com/towards-data-science/automate-streamlit-web-app-using-interactive-aggrid-with-google-sheets-81b93fd9e648).
                
                - ## Link to the YouTube videos :
                    - 1. [AgGrid Part 1](https://youtu.be/F54ELJwspos)
                    - 2. [AgGrid Part 2](https://youtu.be/Zs9-8trPadU)
                    - 3. [AgGrid Part 3](https://youtu.be/sOFM334iILs)
            ''' )
  
st.sidebar.video('https://youtu.be/F54ELJwspos')
st.sidebar.video('https://youtu.be/Zs9-8trPadU')

st.subheader("This is how AgGrid Table looks!")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)
# _______________________________________________________________
# Enabling tooltip - YouTube-Query by Alexis-Raja Brachet  
# gd.configure_default_column(editable=True,groupable=True,tooltipField = "variant") 
# hover in any rows( under any columns), the variant of that row, will pop up as tootltip information.However, 
# I'm yet to figure out, how to implement more than one column information (what I mean - let's say - ["variant", "date"] collectively as tooltip information) , 
# also, it's bit slow in the begginig  when I tested. 
# ________________________________________________________________

if _funct == 'Display':
    sel_mode = st.radio('Selection Type', options = ['single', 'multiple'])
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df,gridOptions=gridoptions,
                        update_mode= GridUpdateMode.SELECTION_CHANGED,
                        height = 500,
                        allow_unsafe_jscode=True,
                        #enable_enterprise_modules = True,
                        theme = 'balham')

    sel_row = grid_table["selected_rows"]
    st.subheader("Output")
    st.write(sel_row)
if _funct == 'Highlight':
    col_opt = st.selectbox(label ='Select column',options = df.columns)
    cellstyle_jscode = JsCode("""
        function(params){
            if (params.value == 'Alpha') {
                return {
                    'color': 'black',
                    'backgroundColor' : 'orange'
            }
            }
            if (params.value == 'B.1.258') {
                return{
                    'color'  : 'black',
                    'backgroundColor' : 'red'
                }
            }
            else{
                return{
                    'color': 'black',
                    'backgroundColor': 'lightpink'
                }
            }
       
    };
    """)
    gd.configure_columns(col_opt, cellStyle=cellstyle_jscode)
    gridOptions = gd.build()
    grid_table = AgGrid(df, 
            gridOptions = gridOptions, 
            enable_enterprise_modules = True,
            fit_columns_on_grid_load = True,
            height=500,
            width='100%',
            # theme = "material",
            update_mode = GridUpdateMode.SELECTION_CHANGED,
            reload_data = True,
            allow_unsafe_jscode=True,
            )
if _funct == 'Delete':
    
    js = JsCode("""
    function(e) {
        let api = e.api;
        let sel = api.getSelectedRows();
        api.applyTransaction({remove: sel})    
    };
    """     
    )  
    
    gd.configure_selection(selection_mode= 'single')
    gd.configure_grid_options(onRowSelected = js,pre_selected_rows=[])
    gridOptions = gd.build()
    grid_table = AgGrid(df, 
                gridOptions = gridOptions, 
                enable_enterprise_modules = True,
                fit_columns_on_grid_load = True,
                height=500,
                width='100%',
                # theme = "streamlit",
                update_mode = GridUpdateMode.SELECTION_CHANGED,
                reload_data = True,
                allow_unsafe_jscode=True,
                )    
    st.balloons()
    st.info("Total Rows :" + str(len(grid_table['data'])))   
