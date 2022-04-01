import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Functions

@st.cache
def data_upload():
    df = pd.read_csv("covid-variants.csv")
    return df

#st.header("This is Streamlit Default Dataframe")
df = data_upload()
# st.dataframe(data=df)
# st.info(len(df))

_funct = st.sidebar.radio(label="Functions", options = ['Display','Highlight','Delete'])

st.header("This is AgGrid Table")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True,groupable=True)

if _funct == 'Display':
    sel_mode = st.radio('Selection Type', options = ['single', 'multiple'])
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df,gridOptions=gridoptions,
                        update_mode= GridUpdateMode.SELECTION_CHANGED,
                        height = 500,
                        allow_unsafe_jscode=True,
                        #enable_enterprise_modules = True,
                        theme = 'fresh')

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
            theme = "material",
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
                theme = "streamlit",
                update_mode = GridUpdateMode.SELECTION_CHANGED,
                reload_data = True,
                allow_unsafe_jscode=True,
                )    
    st.balloons()
    st.info("Total Rows :" + str(len(grid_table['data'])))   
