import streamlit as st
import datetime
import re
import datetime
import boto3
import json
from sqlalchemy import create_engine,text,inspect
from sqlalchemy.types import Integer,VARCHAR
import pandas as pd

st.session_state.is_trending = False
def main():
    
    

    def create_con(Accesskey,Pass_key,srvc_name):
        s3 = boto3.client(
        service_name=srvc_name,
        region_name='ap-south-2',
        aws_access_key_id = Accesskey, 
        aws_secret_access_key = Pass_key
        )
        return s3


    def create_bucket(s3):
        # Specify the bucket name you wish to create
        bucket_name = 'user-posts-guvi-capston2'
        # Create the S3 bucket
        
            # Verify bucket existence
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' exists and is accessible.")
        except:
            try:
                s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={
                                                'LocationConstraint': 'ap-south-2'})
                print(f"Bucket '{bucket_name}' was successfully created.")
            except Exception as e:
                print(f"An error occurred while creating the bucket: {e}")
        
        return bucket_name

    def put_obj(s3,bucket_name,key,myDictionary ={}):
        serializedMyData = json.dumps(myDictionary)
        s3.put_object(Bucket=bucket_name,Key=key, Body=serializedMyData)

 


    def create_dynamo_db(dynamo_db):
        table = dynamo_db.create_table(
        TableName ='app_data_guvi_capstone2',
        KeySchema =[ 
                {
                'AttributeName':'userid',
                'KeyType':'HASH'
                },
                {
                'AttributeName':'postdate',
                'KeyType':'RANGE'
                }
            ],
        ProvisionedThroughput ={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
        AttributeDefinitions =[
            {
                'AttributeName': 'userid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'postdate',
                'AttributeType': 'S'
            }
            ],
            )
        return table
    

    def sqlcol(df_mongo):    
    
        type_df = {}
        for i,j in zip(df_mongo.columns, df_mongo.dtypes):
            if "object" in str(j):
                type_df.update({i: VARCHAR(length=50)})

            if "int" in str(j):
                type_df.update({i: Integer})

        return type_df
    

     #Function call to convert the data types
    def postgres_create(df):
        connection = create_engine("postgresql://postgres:qweaszx@localhost:5432/guvi_social_app") #Postgresql connection - dbname://userid:password@hostname:portnumber/databasename
        tab = inspect(connection)
        df_df = pd.DataFrame.from_dict([df])
        if tab.has_table("social_app") == False:
            op_dtype = sqlcol(df_df)
            df_df.to_sql("social_app", con = connection, if_exists='append',
                            index =False) # pushing data from mongo dataframe to postgree table census , rows will be replaced if the table already exists
            with connection.connect() as conn:
                conn.execute(text('ALTER TABLE social_app ADD PRIMARY KEY("user");'))
        else:
            update_post(df_df,connection)
        return (connection)
            
    def update_post(df_df,connection):
        df_df.to_sql("social_app", con = connection, if_exists='append',
                            index =False)

    def split_hashtags(post):
        hashtag_list =[]
        post_tmp =post.split()
        pat = re.compile(r"#(\w+)")       
        for text in post_tmp:
            hashtag_temp = pat.findall(text)
            if hashtag_temp != []:
                for i in hashtag_temp:
                    hashtag_list.append(i)
                print(hashtag_list)
        return(hashtag_list)


   





    Path = "F:/New folder/GUVI/Bravo_04_accessKeys.csv"
    with open(Path,"r") as pwd:
        for i in pwd:
            Accesskey,Pass_key = i.split(",")
    #Dynamodb
    dynamo_db = create_con(Accesskey,Pass_key,'dynamodb')

    response = dynamo_db.list_tables()
    if 'app_data_guvi_capstone2' not in response['TableNames']:          
        dynamo_tble = create_dynamo_db(dynamo_db)
    #s3 
    s3 = create_con(Accesskey,Pass_key,'s3')
    bucket_name=create_bucket(s3)
    
    
    user1,user2 = st.columns(2)
    for cl,userid in [[user1,'user1']]:#,[user2,'user2']]:
        with cl:
            with st.container():
        
                    st.title('Post your thoughts')
                    # Add comment section
                    post = st.text_area("",max_chars=280,key = userid)
                    # Post button
                    placeholder =st.empty()
                    with placeholder:
                        if st.button("Post",key =str([userid])):
                            if '#' not in post:
                                st.error('Please use atleast one # hashtag', icon="🚨")
                            else:
                                dt = datetime.datetime.now()
                                post_date = dt.date()
                                post_time = dt.strftime("%X")
                                key = f"{userid}{post_date}{post_time}"
                                data = {'user':userid,'post_date':str(post_date),'post_time':str(post_time),'content':post}
                                put_obj(s3,bucket_name,key,data)
                                hashtags = split_hashtags(post)
                                for hashtag in hashtags:
                                    data_temp ={'user':userid,'post_date':post_date,'post_time':post_time,'content':post,'hashtags':hashtag}
                                    connection = postgres_create(data_temp)
                                st.write('Thoughts posted', icon="🚨")

                              
                       


if __name__ == "__main__":
    main()