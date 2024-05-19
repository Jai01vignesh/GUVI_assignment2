import streamlit as st
from st_pages import Page, show_pages
import time
from sqlalchemy import create_engine,inspect
import pandas as pd
import random
import datetime
import lorem

if 'is_trending' not in st.session_state:
    st.session_state['is_trending'] = False
st.set_page_config(
        page_title="Twitter like app",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
        }
    )

side_bar = st.sidebar

show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("pages/posts_feed.py", "Tweet", ":books:"),
        Page("pages/posts.py", "Posts Feed", ":books:"),
        Page("pages/rand_posts.py", "Trending Posts", ":books:"),
    ]
)
def postgres_create(df):
        connection = create_engine("postgresql://postgres:qweaszx@localhost:5432/guvi_social_app") #Postgresql connection - dbname://userid:password@hostname:portnumber/databasename
        tab = inspect(connection)
        df_df = pd.DataFrame.from_dict([df])
        update_post(df_df,connection)
        return (connection)
            
def update_post(df_df,connection):
    df_df.to_sql("social_app", con = connection, if_exists='append',
                            index =False)
    
def generate_random_tweet():

    user = random.choice(["user2", "user3", "user4", "user5"])  # Select a random user
    content = lorem.sentence()  # Generate random content using lorem ipsum

    # Generate random number of hashtags (up to 3)
    dt = datetime.datetime.now()
    post_date = dt.date()
    post_time = dt.strftime("%X")
    return {"user": user, "content": content, "post_date":post_date ,"post_time":str(post_time)}

def generate_random_tweets(n, hashtgs):
    for _ in range(n):
        tweet = generate_random_tweet()
        key = f"{tweet.get("user")}{tweet.get("post_date")}{tweet.get("post_time")}"
        print(hashtgs)
        if hashtgs =="":
            hashtags = ['food','cricket','country','war','news','social_app']
        else:
            hashtags_tmp = hashtgs.split("#") 
            hashtags = list(filter(lambda s: s.strip(), hashtags_tmp))
            print(hashtags)
        for hashtag in hashtags:
            userid = tweet.get("user") 
            post_date = tweet.get("post_date")
            post_time = tweet.get("post_time")
            post = tweet.get("content")
            data_temp ={'user':userid,'post_date':post_date,'post_time':post_time,'content':post,'hashtags':hashtag}
            connection = postgres_create(data_temp)

with st.container():
    n = st.text_input("Enter the no of thoughts to be generated")
    hashtags = st.text_input("Hashtags")

    if st.button("Generate random thoughts"):
        generate_random_tweets(int(n),hashtags)
