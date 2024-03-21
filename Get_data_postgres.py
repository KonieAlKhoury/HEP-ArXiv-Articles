from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import os

def Get_data_postgres(database,table):
    # Get the value of the POSTGRES_USER environment variable
    postgres_user = os.environ.get('POSTGRES_USER')
    # Get the value of the POSTGRES_PW environment variable
    postgres_pw = os.environ.get('POSTGRES_PW')
    #Use the value of the POSTGRES_USER environment variable in the connection string
    connection_str = f"postgresql://{postgres_user}:{postgres_pw}@localhost:5432/{database}"
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