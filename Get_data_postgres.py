from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

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