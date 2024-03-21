import feedparser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def load_data(query, max_results, add_options=''):
    """
    Loads data from the arXiv API based on the given query.

    Args:
        query (str): The search query to be used.
        max_results (int): The maximum number of results to retrieve.
        add_options (str, optional): Additional options to be added to the API query. Defaults to ''.

    Returns:
        dict: A dictionary containing the parsed data from the arXiv API.

    Raises:
        None

    """

    # Define the URL for the ArXiv API
    url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}{add_options}'

    data = feedparser.parse(url)

    # Check if the feed was parsed successfully
    if data.bozo:
        print("Error parsing the feed:", data.bozo_exception)
    else:
        # Check if any entries were fetched
        if len(data.entries) == 0:
            print("No entries found")
    return data


def save_dataframes(df, filename):
    #remove the Paper Type and ATLAS Collaboration columns
    del df['Paper Type'],df['ATLAS Collaboration'] 
    # Change authors to a set, to match the PostgreSQL data requirements
    df['authors'] = df['authors'].apply(set)
    # Save the data to a csv file
    df.to_csv('filename', index=False)

    # df_Arxiv.to_parquet('df_Arxiv.parquet.gzip',
    #               compression='gzip')
 


def main():
    # This load the data of the last 200 papers in the 'hep-ph' category and from the ATLAS experiment
    query = 'cat:hep-ph+AND+all:ATLAS'
    max_results=200
    add_options = '&sortBy=submittedDate&sortOrder=descending'

    data = load_data(query , max_results, add_options)

    # Print the keys of the first entry to see what is in the data
    print(data.entries[0].keys())

    List_Arxiv = []
    for entry in data.entries:
        List_Arxiv.append({
            'title':entry.title,
            'summary': entry.summary, 
            'authors':entry.authors, 
            'updated':entry.updated, 
            'published':entry.published})

    #Load data in the dataframe and check the first 5 rows        
    df_Arxiv = pd.DataFrame(List_Arxiv)  
    # print(df_Arxiv.head(5))

    #Get the number of published paper as function of time
    # Convert the string to a datetime object
    df_Arxiv['published'] = pd.to_datetime(df_Arxiv['published'])

    # Count the number of papers published per month
    df_Arxiv['published'].dt.to_period('M').value_counts().sort_index().plot()
    # Add title and labels
    title = 'Number of papers published per month'
    plt.title(title)
    plt.ylabel('Number of papers')
    # plt.show()


    # Check the number of papers published under the ATLAS Collaboration
    #Convert he authors column to a list of authors
    df_Arxiv['authors'] = df_Arxiv['authors'].apply(lambda authors: [author['name'] for author in authors])
    # Check if the ATLAS Collaboration is in the list of authors
    df_Arxiv['ATLAS Collaboration'] = df_Arxiv['authors'].apply(lambda authors: 'ATLAS Collaboration' in authors)
    # print(df_Arxiv['ATLAS Collaboration'].value_counts())
    # Plot the number of papers published under the ATLAS Collaboration and other
    df_Arxiv['ATLAS Collaboration'].value_counts().plot(kind='bar')
    # Add title and labels
    plt.title('% of Papers published under the ATLAS Collaboration')
    plt.xlabel('Authors')
    plt.ylabel('Number of papers')
    plt.xticks([1, 0], ['ATLAS Collaboration', 'Other'], rotation=0)
    # plt.show()

    #Check if the paper has a search, measurement or other specific results using the title
    #First convert the title to lower case 
    df_Arxiv['title'] = df_Arxiv['title'].str.lower()
    df_Arxiv['Paper Type'] = df_Arxiv['title'].apply(lambda title: 'Search' if 'search' in title else ('Measurement' if 'measurement' in title else 'Other'))
    df_Arxiv['Paper Type'].value_counts().plot(kind='bar')
    # Add title and labels
    plt.title('Number of paper per type of analysis')
    plt.xlabel('')
    plt.ylabel('Number of papers')
    plt.xticks(rotation=0)
    # plt.show()

    #Save the data in a csv file
    # save_dataframes(df_Arxiv, 'Arxiv_data.csv')
    


if __name__ == '__main__':
    main()
