from PostgresConnection import engine_connection
import pandas as pd
from sqlalchemy import text
import matplotlib.pyplot as plt

def main():

    # Get the data from the postgres database
    database = "Arxiv_data"
    table_title = "Arxiv_data_title"
    table_summary = "Arxiv_data_summary"

    engine = engine_connection(database)

    query_title = f'SELECT title, COUNT(*) AS Occurences FROM public."{table_title}" GROUP BY title ORDER BY Occurences DESC LIMIT 20'
    query_summary = f'SELECT summary, COUNT(*) AS Occurences FROM public."{table_summary}" GROUP BY summary ORDER BY Occurences DESC LIMIT 20'
    with engine.connect() as connection:
        result_title = connection.execute(text(query_title)).fetchall()
        result_summary = connection.execute(text(query_summary)).fetchall()

    # Get the results into DataFrames
    df_Arxiv_title = pd.DataFrame(result_title)
    df_Arxiv_summary = pd.DataFrame(result_summary)

    print(df_Arxiv_title.head(20))
    print(df_Arxiv_summary.head(20))

    #plot the data
    # Sort the DataFrame by 'occurrences' in descending order, to have the highest values on top
    df_Arxiv_title = df_Arxiv_title.sort_values('occurences', ascending=True)
    df_Arxiv_summary = df_Arxiv_summary.sort_values('occurences', ascending=True)
    
    # Plot the data
    plt.figure(figsize=(15, 7))
    plt.subplot(1, 2, 1)
    plt.barh(df_Arxiv_title["title"], df_Arxiv_title["occurences"])
    plt.title('Top 20 words in title')
    plt.ylabel('Word')
    plt.xlabel('Count')

    plt.subplot(1, 2, 2)
    plt.barh(df_Arxiv_summary["summary"], df_Arxiv_summary["occurences"])
    plt.title('Top 20 words in summary')
    plt.ylabel('Word')
    plt.xlabel('Count')

    plt.tight_layout()
    plt.show()

    

if __name__ == "__main__":
    main()