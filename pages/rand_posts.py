import time
from sqlalchemy import create_engine
import pandas as pd
from st_pages import get_pages, get_script_run_ctx 
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import datetime
st.session_state.is_trending = True

placeholder =st.empty()
def fetch_data(connection): 

        SQL_Query0 = pd.read_sql('select "hashtags",count("hashtags") as "Number" from social_app group by "hashtags";', 
                         connection)
        return(SQL_Query0)


connection = create_engine("postgresql://postgres:qweaszx@localhost:5432/guvi_social_app") #Postgresql connection - dbname://userid:password@hostname:portnumber/databasename
st.subheader("Hashtag")
while st.session_state.is_trending:
    Sql = fetch_data(connection)
    #print("Fetching data every one tw")
    time.sleep(1) 
    
    cross_tb_app =pd.crosstab(Sql['Number'],Sql['hashtags'])
    with placeholder:
        fig = px.bar(y =Sql['Number'], x=Sql['hashtags'],color = Sql['hashtags'] )

        # Plot!
        st.plotly_chart(fig, use_container_width=True, height = 200)

     
              
 


                                 