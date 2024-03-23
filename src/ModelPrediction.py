from PostgresConnection import engine_connection
import pandas as pd
from sqlalchemy import text
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


def find_category(row, words):
    """
    Find the category of a given row based on the presence of certain words in the title or summary.

    Parameters:
    - row: A dictionary representing a row of data.
    - words: A list of words representing the categories to search for.

    Returns:
    - The category that matches the words found in the title or summary, or 'None' if no match is found.
    """
    
    title_words = set(row['title'].lower().split())
    summary_words = set(row['summary'].lower().split())
    for category in words:
        if category.lower() in title_words or category.lower() in summary_words:
            return category
    return 'None'

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
    df_countVec = df_countVec.sort_values('count', ascending=False).head(40)

    ArxivTransformer = TfidfTransformer()
    SummaryWeights = ArxivTransformer.fit_transform(words_count)

    SummaryWeights = np.asarray(SummaryWeights.mean(axis=0)).ravel().tolist()
    df_Summaryweights = pd.DataFrame({'word': countVec.get_feature_names_out(), 'weight': SummaryWeights})

    df_Summaryweights = df_Summaryweights.sort_values(by='weight', ascending=False).head(40)
    df_Summaryweights = df_Summaryweights.sort_values('weight', ascending=True)


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
    plt.savefig('plots/Top40FromCountVectorizer.png')
    
    # Training Machine Learning Model to classify the paper into categories based on the title and summary
    #preparinf the category data
    Targetedwords = df_countVec["word"].values
    # Removing the words  two, also, using, data, atlas, cms, lhc from the targeted categories
    Targetedwords = [x for x in Targetedwords if x not in ['two', 'also', 'using', 'data', 'atlas', 'cms','lhc','tev','gev','physics','one', 'collider','new']]
    # using as targeted categories the top 20 words in the summary, to create a new category column
    df_Arxiv['category'] = df_Arxiv.apply(find_category, args=(Targetedwords[::-1],), axis=1)
    TargetedCategories = df_Arxiv['category'].values

    # Prepare the data ftor training by getting the values from summary and title and combining them 
    Arxiv_title_summary = (df_Arxiv["summary"]+df_Arxiv["title"]).values

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        max_features=3000)
    word_vectorizer.fit(Arxiv_title_summary)
    Featurestransformed = word_vectorizer.transform(Arxiv_title_summary)

    X_train,X_test,y_train,y_test = train_test_split(Featurestransformed,TargetedCategories,random_state=1, test_size=0.5,shuffle=True)

    #Start training the classifier
    print('Training the KNeighborsClassifier')
    clfKNC = KNeighborsClassifier(n_neighbors=2)
    clfKNC.fit(X_train, y_train)
    prediction = clfKNC.predict(X_test)
 
    print('Training the LogisticRegression')
    clfLR=LogisticRegression(random_state=0,n_jobs=-1,verbose=3,max_iter=1500)
    clfLR.fit(X_train,y_train)
    y_pred = clfLR.predict(X_test)

    # Models Accuracy, comparison between KNeighbors Classifier and LogisticRegression Classifier
    print('\n Accuracy of KNeighbors Classifier on training set: {:.2f}'.format(clfKNC.score(X_train, y_train)))
    print('Accuracy of KNeighbors Classifier on test set: {:.2f}'.format(clfKNC.score(X_test, y_test)))
 
    print('\n Accuracy of LogisticRegression Classifier on training set: {:.2f}'.format(clfLR.score(X_train, y_train)))
    print('Accuracy of LogisticRegression Classifier on testing set: {:.2f}'.format(clfLR.score(X_test, y_test)))


if __name__ == "__main__":
    main()