from Get_data_postgres import engine_connection
import pandas as pd
from sqlalchemy import text
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def main():
    # Get the data from the postgres database
    database = "Arxiv_data"
    table_title = "Arxiv_data_title"
    table_summary = "Arxiv_data_summary"

    engine = engine_connection(database)

    query = f'''
        SELECT t.paperidentifier, t.title, s.summary FROM public."{table_title}" t
        LEFT JOIN public."{table_summary}" s ON t.paperidentifier = s.paperidentifier
        ORDER BY t.paperidentifier DESC
    '''

    # query = f'SELECT paperidentifier, summary FROM public."{table_summary}"'

    with engine.connect() as connection:
        result_title = connection.execute(text(query)).fetchall()

    df_Arxiv = pd.DataFrame(result_title, columns=['PaperIdentifier', 'title', 'summary'])
    df_Arxiv = df_Arxiv.groupby('PaperIdentifier').agg({
    'title': lambda x: ' '.join(set(x)),
    'summary': lambda x: ' '.join(set(x))    }).reset_index()


    #Use the CountVectorizer to get the number of occurences of each word in the summary
    countVec = CountVectorizer(max_df=0.90, min_df=0.05)
    countVec.fit(df_Arxiv["summary"])

    words_count = countVec.transform(df_Arxiv["summary"])

    #make array from number of occurrences
    count = np.asarray(words_count.sum(axis=0)).ravel().tolist()

    #make a new data frame with columns term and occurrences, meaning word and number of occurences
    df_countVec = pd.DataFrame({'word': countVec.get_feature_names_out(), 'count': count})
    df_countVec = df_countVec.sort_values('count', ascending=False).head(20)
    # print(bowListFrame)

    ArxivTransformer = TfidfTransformer()
    SummaryWeights = ArxivTransformer.fit_transform(words_count)

    SummaryWeights = np.asarray(SummaryWeights.mean(axis=0)).ravel().tolist()
    df_Summaryweights = pd.DataFrame({'word': countVec.get_feature_names_out(), 'weight': SummaryWeights})

    df_Summaryweights = df_Summaryweights.sort_values(by='weight', ascending=False).head(20)
    df_Summaryweights = df_Summaryweights.sort_values('weight', ascending=True)
    print(df_Summaryweights)

    #plot the data
    df_countVec = df_countVec.sort_values('count', ascending=True)
 
    # Plot the data
    plt.figure(figsize=(18, 9))
    plt.subplot(1, 2, 1)
    plt.barh(df_countVec["word"], df_countVec["count"])
    plt.title('Top 20 words in title')
    plt.ylabel('Word')
    plt.xlabel('Count')

    plt.subplot(1, 2, 2)
    plt.barh(df_Summaryweights["word"], df_Summaryweights["weight"])
    plt.title('Top 20 words sorted by weight')
    plt.ylabel('Word')
    plt.xlabel('weight')
    plt.show()
    

                  
if __name__ == "__main__":
    main()