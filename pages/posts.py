import streamlit as st
import datetime
import pandas as pd
from sqlalchemy import create_engine

st.session_state.is_trending = False
def main():
    # Color picker widget
    def fetch_data(connection): 

        SQL_Query0 = pd.read_sql('select * from social_app;', 
                         connection)
        return(SQL_Query0)

    

    def display_tweet(tweet):
        st.markdown(
            f"""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <span style="font-weight: bold; margin-right: 5px;">{tweet[0]}</span>
                    <span style="color: #888;">{tweet[4]}</span>
                    <span style="color: #888; flex-grow: 1; text-align: right;">{tweet[1]}</span>
                </div>
                <div style="margin-bottom: 5px;">{tweet[3]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def format_timestamp(timestamp):
        """
        Format the timestamp.
        """
        return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%b %d, %Y %I:%M %p')

        # Display each tweet
    connection = create_engine("postgresql://postgres:qweaszx@localhost:5432/guvi_social_app")
    tweets = fetch_data(connection)
    for tweetddsd in tweets.values:
        display_tweet(tweetddsd)


if __name__ == "__main__":
    main()