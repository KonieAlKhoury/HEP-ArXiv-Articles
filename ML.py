from Get_data_postgres import engine_connection
import pandas as pd
from sqlalchemy import text

def main():
    # Get the data from the postgres database
    database = "Arxiv_data"
    table_title = "Arxiv_data_title"
    table_summary = "Arxiv_data_summary"

    engine = engine_connection(database)

    query_title = f'SELECT * FROM public."{table_title}"'
    query_summary = f'SELECT * FROM public."{table_title}"'
    with engine.connect() as connection:
        result_title = connection.execute(text(query_title)).fetchall()
        result_summary = connection.execute(text(query_summary)).fetchall()

    # Get the results into DataFrames
    df_Arxiv_title = pd.DataFrame(result_title)
    df_Arxiv_summary = pd.DataFrame(result_summary)

    # print(df_Arxiv_title.head(5))

if __name__ == "__main__":
    main()