from sqlalchemy import create_engine
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from Get_data_postgres import Get_data_postgres
import os
import string



def main():
    #Get the data from the postgres database
    database = "Arxiv_data"
    table = "Last_200_papers"
    df_Arxiv = Get_data_postgres(database,table)

    # start preparing the data by setting the title and suummary to lower case
    df_Arxiv['title'] = df_Arxiv['title'].str.lower()
    df_Arxiv['summary'] = df_Arxiv['summary'].str.lower()
    
    # remove "\n" from title and summary and convert them to a space
    df_Arxiv['title'] = df_Arxiv['title'].str.replace("\n", " ")
    df_Arxiv['summary'] = df_Arxiv['summary'].str.replace("\n", " ")

    #remove the stop/filling words, such as the, I , we , and, etc .. 
    # Using the stopwords from the nltk package and setting it to english
    stops = stopwords.words('english')
    # Split the title and summary into words
    df_Arxiv['title'] = df_Arxiv['title'].str.split()
    df_Arxiv['summary'] = df_Arxiv['summary'].str.split()
    # Remove the stop words
    df_Arxiv['title'] = df_Arxiv['title'].apply(lambda x: [item for item in x if item not in stops])
    df_Arxiv['summary'] = df_Arxiv['summary'].apply(lambda x: [item for item in x if item not in stops])

    #remove all numbers from the title and summary
    df_Arxiv['title'] = df_Arxiv['title'].apply(lambda x: [item for item in x if item.isdigit() == False])
    df_Arxiv['summary'] = df_Arxiv['summary'].apply(lambda x: [item for item in x if item.isdigit() == False])

    #remove all words with $ or \\ in them to remove latex words 
    df_Arxiv['title'] = df_Arxiv['title'].apply(lambda x: [item for item in x if '$' not in item and '\\' not in item])
    df_Arxiv['summary'] = df_Arxiv['summary'].apply(lambda x: [item for item in x if '$' not in item and '\\' not in item])

    #remove all ponctuations from the title and summary
    df_Arxiv['title'] = df_Arxiv['title'].apply(lambda x: [''.join(c for c in item if c not in string.punctuation) for item in x])
    df_Arxiv['summary'] = df_Arxiv['summary'].apply(lambda x: [''.join(c for c in item if c not in string.punctuation) for item in x])


    #Pushing the processed data to a new table in the same database
    #Prepare the 3 dataframes, 1 for the title, 1 for the summary and 1 for the authors
    # create a unique identifier per each row (to be used for joining the dataframes later on)
    df_Arxiv['Paper identifier'] = df_Arxiv.index
    df_Arxiv_title = df_Arxiv[['Paper identifier','title']]
    df_Arxiv_summary = df_Arxiv[['Paper identifier','summary']]
    df_Arxiv_authors = df_Arxiv[['Paper identifier','authors']]

    #Convert the list-like columns to seperate rows
    df_Arxiv_title = df_Arxiv_title.explode('title')
    df_Arxiv_summary = df_Arxiv_summary.explode('summary')
    df_Arxiv_authors = df_Arxiv_authors.explode('authors')

 
    # # Get the value of the POSTGRES_USER environment variable
    postgres_user = os.environ.get('POSTGRES_USER')
    # # Get the value of the POSTGRES_PW environment variable
    postgres_pw = os.environ.get('POSTGRES_PW')
    # Use the value of the POSTGRES_USER environment variable in the connection string
    connection_str = f"postgresql://{postgres_user}:{postgres_pw}@localhost:5432/{database}"

    #Create a SQLAlchemy engine
    engine = create_engine(connection_str)
    #Push the data to the new table, if exists replace the data
    df_Arxiv_title.to_sql("Arxiv_data_title", con=engine, if_exists='replace',index=False)
    df_Arxiv_summary.to_sql("Arxiv_data_summary", con=engine, if_exists='replace',index=False)
    df_Arxiv_authors.to_sql("Arxiv_data_authors", con=engine, if_exists='replace',index=False)

if __name__ == "__main__":
    main()