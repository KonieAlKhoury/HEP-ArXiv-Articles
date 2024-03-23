from sqlalchemy import create_engine
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from PostgresConnection import Get_data_postgres, write_data_postgres
import os
import string

def data_preparation(df):
    """
    Preprocesses the input dataframe by performing several data cleaning steps.

    Args:
        df (pandas.DataFrame): The input dataframe containing the text data.

    Returns:
        pandas.DataFrame: The preprocessed dataframe with cleaned text data.
    """

    # start preparing the data by setting all words to lower case
    df = df.str.lower()
    # remove "\n" from title and summary and convert them to a space
    df = df.str.replace("\n", " ")

    #remove the stop/filling words, such as the, I , we , and, etc .. 
    # Using the stopwords from the nltk package and setting it to english
    stops = stopwords.words('english')
    # Split the title and summary into words
    df = df.str.split()
    df = df.apply(lambda x: [item for item in x if item not in stops])

    #remove all numbers from the title and summary
    df = df.apply(lambda x: [item for item in x if item.isdigit() == False])

    #remove all ponctuations from the title and summary
    df = df.apply(lambda x: [''.join(c for c in item if c not in string.punctuation) for item in x])

    #remove all empty elements and special words with $ or \\ in them to remove latex words 
    df = df.apply(lambda x: [item for item in x if item != " " and item != ""  and '$' not in item and '\\' not in item])

    return df
    
    


def main():
    #Get the data from the postgres database
    database = "Arxiv_data"
    table = "Last_500_papers"
    df_Arxiv = Get_data_postgres(database,table)

    df_Arxiv['title'] = data_preparation(df_Arxiv['title'])
    df_Arxiv['summary'] = data_preparation(df_Arxiv['summary'])

    #Pushing the processed data to a new table in the same database
    #Prepare the 3 dataframes, 1 for the title, 1 for the summary and 1 for the authors
    # create a unique identifier per each row (to be used for joining the dataframes later on)
    df_Arxiv['paperidentifier'] = df_Arxiv.index
    df_Arxiv_title = df_Arxiv[['paperidentifier','title']]
    df_Arxiv_summary = df_Arxiv[['paperidentifier','summary']]
    df_Arxiv_authors = df_Arxiv[['paperidentifier','authors']]

    #Convert the list-like columns to seperate rows
    df_Arxiv_title = df_Arxiv_title.explode('title')
    df_Arxiv_summary = df_Arxiv_summary.explode('summary')
    df_Arxiv_authors = df_Arxiv_authors.explode('authors')

 
    #Push the data to the new table, if exists replace the data
    write_data_postgres(df_Arxiv_title,database,"Arxiv_data_title")
    write_data_postgres(df_Arxiv_summary,database,"Arxiv_data_summary")
    write_data_postgres(df_Arxiv_authors,database,"Arxiv_data_authors")
 
if __name__ == "__main__":
    main()