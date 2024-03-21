from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2
import pandas as pd

def main():
    # define the postgres connection string
    connection_str = "postgresql://postgres:POSTgres21032024@localhost:5432/Arxiv_data"

    #Create a SQLAlchemy engine
    engine = create_engine(connection_str)

    try:
        with engine.connect() as connection_str:
            print('Successfully connected to the PostgreSQL database')
    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')

 
    query = 'SELECT * FROM public."Last_200_papers"'
    with engine.connect() as connection:
        results = connection.execute(text(query)).fetchall()
        
    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(results)
    #Check the first row
    print(df.iloc[0])



if __name__ == "__main__":
    main()