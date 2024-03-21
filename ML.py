import pandas as pd
from Get_data_postgres import Get_data_postgres



def main():
    #Get the data from the postgres database
    database = "Arxiv_data"
    table_title = "Arxiv_data_title"
    # table_summary = "Arxiv_data_summary"

    df_Arxiv_title = Get_data_postgres(database,table_title)
    # df_Arxiv_summary = Get_data_postgres(database,table_summary)

    print(df_Arxiv_title.head(5))


if __name__ == "__main__":
    main()