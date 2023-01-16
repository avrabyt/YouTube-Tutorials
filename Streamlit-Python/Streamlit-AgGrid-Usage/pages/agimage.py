# Import Modules
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Dummy data
data = {
        'image_url': ['https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_CR0,0,675,1000_AL_.jpg',
                      'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SY1000_CR0,0,704,1000_AL_.jpg',
                      'https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SY1000_CR0,0,679,1000_AL_.jpg',
                      'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg'],
        'name': ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II', 'The Dark Knight'],
        'year': [1994, 1972, 1974, 2008],
        'description': ['Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                        'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                        'The early life and career of Vito Corleone in 1920s New York is portrayed while his son, Michael, expands and tightens his grip on the family crime syndicate.',
                        'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham, the Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.'],
        'rating': [9.2, 9.2, 9.0, 9.0],
        }
df = pd.DataFrame(data)
#st.write(df)
st.header("AgGrid Demo `Part 4`: Grid table with Image Display")

with st.expander('TL;DR', expanded=True):
   
   st.markdown('''
               Medium Article : 
                    [**Enhancing AgGrid table with Image Display in Streamlit Apps**](https://medium.com/the-streamlit-teacher/enhancing-aggrid-table-with-image-display-in-streamlit-apps-425b6e989d5b).                
                > The streamlit-aggrid library allows us to easily add the AgGrid component to a Streamlit app and customize it with various options.
                > We can use a custom cell renderer function to display images in cells of the AgGrid component.
                > By combining the powerful features of AgGrid with the simplicity of Streamlit, we can create interactive and informative data visualization apps quickly and easily.

                Link to the YouTube video : [AgGrid Part 4 : Streamlit AgGrid Extras - Display Image within the Table | JavaScript Injection | Python](https://youtu.be/3Ax3S8g2bak)
                ''')
render_image = JsCode('''
                      
    function renderImage(params){
    // Create a new image element
        var img = new Image();
        
        img.src = params.value;
        
        img.width = 35;
        img.height = 35;
        
        return img;
        
    }             
                      ''')

# build gridoptions object

# Build GridOptions object
options_builder = GridOptionsBuilder.from_dataframe(df)
options_builder.configure_column('image_url', cellRenderer = render_image)
options_builder.configure_selection(selection_mode="single", use_checkbox=True)
grid_options = options_builder.build()

# Create AgGrid component
grid = AgGrid(df, 
                gridOptions = grid_options,
                allow_unsafe_jscode=True,
                height=200, width=500, theme='streamlit')

sel_row = grid["selected_rows"]
if sel_row:
    col1, col2 = st.columns(2)
    st.info(sel_row[0]['description'])
    col1.image(sel_row[0]['image_url'],caption = sel_row[0]['name'])
    col2.subheader("Rating: " + str(sel_row[0]['rating']))

st.sidebar.markdown('''
                - ## Medium Article : 
                   [**Enhancing AgGrid table with Image Display in Streamlit Apps**](https://medium.com/the-streamlit-teacher/enhancing-aggrid-table-with-image-display-in-streamlit-apps-425b6e989d5b)
                
                - ## Link to the YouTube videos :
                    - 1. [AgGrid Part 1](https://youtu.be/F54ELJwspos)
                    - 2. [AgGrid Part 2](https://youtu.be/Zs9-8trPadU)
                    - 3. [AgGrid Part 3](https://youtu.be/sOFM334iILs)
                    - 4. [AgGrid Part 4](https://youtu.be/3Ax3S8g2bak)
            ''' )
st.sidebar.video('https://youtu.be/3Ax3S8g2bak')         
