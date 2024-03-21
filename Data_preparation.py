from sqlalchemy import create_engine
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from Get_data_postgres import Get_data_postgres



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


    #Pusing the table to a new table in the same database with the name test1
    new_table = "Last_200_papers_processed"   
    connection_str = f"postgresql://postgres:POSTgres21032024@localhost:5432/{database}"

    #Create a SQLAlchemy engine
    engine = create_engine(connection_str)
    #Push the data to the new table, if exists replace the data
    df_Arxiv.to_sql(new_table, con=engine, if_exists='replace',index=False)


if __name__ == "__main__":
    main()