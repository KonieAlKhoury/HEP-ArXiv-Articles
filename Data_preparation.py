from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def Get_data_postgres(database,table):
    # define the postgres connection string
    connection_str = f"postgresql://postgres:POSTgres21032024@localhost:5432/{database}"

    #Create a SQLAlchemy engine
    engine = create_engine(connection_str)

    try:
        with engine.connect() as connection_str:
            print('Successfully connected to the PostgreSQL database')
    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')

 
    query = f'SELECT * FROM public."{table}"'
    with engine.connect() as connection:
        results = connection.execute(text(query)).fetchall()

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(results)

    return df

def main():
    #Check the first row
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
    #Push the data to the new table, if exists append the data
    df_Arxiv.to_sql(new_table, con=engine, if_exists='append',index=False)


if __name__ == "__main__":
    main()