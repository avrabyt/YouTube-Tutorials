import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# This demo is mainly from the suggestion on Community Post 
# https://www.youtube.com/channel/UCDMP6ATYKNXMvn2ok1gfM7Q/community?lb=UgkxMTe1HSFYPta6YDSZCXqkSCp2cKfyiYmU
# ".....Another suggestion for streamlit-aggrid features to explore is buttons inside the aggrid. 
# I think it would be interesting because there aren't many examples of that in the Streamlit forum.""

st.header("Implementing Button within AgGrid table")
# Dump any DataFrame
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data = d)

# Dump as AgGrid Table
# AgGrid(df)

# JavaScript function 
# api.applyTransaction({add: [{}]})   # This line would end row at the end always 
# Finding row index is important to add row just after the selected index
js_add_row = JsCode("""
function(e) {
    let api = e.api;
    let rowPos = e.rowIndex + 1; 
    api.applyTransaction({addIndex: rowPos, add: [{}]})    
};
"""     
)  

# cellRenderer with a button component.
# Resources:
# https://blog.ag-grid.com/cell-renderers-in-ag-grid-every-different-flavour/
# https://www.w3schools.com/css/css3_buttons.asp
cellRenderer_addButton = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <style>
                .btn_add {
                    background-color: #71DC87;
                    border: 2px solid black;
                    color: #D05732;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2.2em;
                    width: 10em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    >&#x2193; Add</button>
            </span>
        `;
        }

        getGui() {
            return this.eGui;
        }

    };
    ''')

# Dump as AgGrid Table
# AgGrid(df)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_column(field = '',  
                    onCellClicked = js_add_row,
                    cellRenderer = cellRenderer_addButton,
                    lockPosition='right')
gridoptions = gd.build()
grid_table = AgGrid(df,gridOptions = gridoptions,
                    allow_unsafe_jscode = True,
                    theme = 'balham', 
                    height = 400,
                    )