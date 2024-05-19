# guvi_assignment2
#Social Media Hashtag Trend Analyzer Application
Technologies used -Python, SQL , AWS Lambda , Dynamodb,  Streamlit
Python libraries used -  re,json,boto3,random,datetime,sqlalchemy,streamlit,lorem,time,plotly

#Problem Statement:
To create a streamlit based Social media text and hashtag posting application with  Hashtag analyzing feature.

Streamlit is used to create User Interface for this application, user entered posts are pushed to aws s3 and then using aws lambda trigger pushed to aws dynamo db. Using Dynamo DB streams the data is sent to postgresql with the help of a lambda trigger. from postgresql the data is queried regularly on a minute basis and the displayed in streamlit using plotly chart.