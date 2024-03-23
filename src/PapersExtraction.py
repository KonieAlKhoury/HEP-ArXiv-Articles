import feedparser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Get_data_postgres import  write_data_postgres

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
    # Parse the data from the URL
    data = feedparser.parse(url)

    # Check if the feed was parsed successfully
    if data.bozo:
        print("Error parsing the feed:", data.bozo_exception)
    else:
        # Check if any entries were fetched
        if len(data.entries) == 0:
            print("No entries found")
    return data


def main():
    # load the data of the last 500 papers in the 'hep-ph' category and from the ATLAS experiment
    query = 'cat:hep-ph+AND+all:ATLAS'
    max_results=500
    add_options = '&sortBy=submittedDate&sortOrder=descending'

    data = load_data(query , max_results, add_options)

    # Print the keys of the first entry to see what is in the data
    print(data.entries[0].keys())

    List_Arxiv = []
    # Extract the title, summary, authors, updated and published date
    for entry in data.entries:
        List_Arxiv.append({
            'title':entry.title,
            'summary': entry.summary, 
            'authors':entry.authors, 
            'updated':entry.updated, 
            'published':entry.published})

    #Load data in the dataframe and check the first 5 rows        
    df_Arxiv = pd.DataFrame(List_Arxiv)  
    #print the first 5 rows
    print(df_Arxiv.head(5))

    #Get the number of published paper as function of time
    # Convert the string to a datetime object
    df_Arxiv['published'] = pd.to_datetime(df_Arxiv['published'])
    # Count the number of papers published per month
    df_Arxiv['published'].dt.to_period('M').value_counts().sort_index().plot()
    # Add title and labels
    title = 'Number of papers published per month'
    plt.title(title)
    plt.ylabel('Number of papers')
    plt.show()


    # Check the number of papers published under the ATLAS Collaboration
    #Convert he authors column to a list of authors
    df_Arxiv['authors'] = df_Arxiv['authors'].apply(lambda authors: [author['name'] for author in authors])
    # Check if the ATLAS Collaboration is in the list of authors
    df_Arxiv['ATLAS Collaboration'] = df_Arxiv['authors'].apply(lambda authors: 'ATLAS Collaboration' in authors)
    # Plot the number of papers published under the ATLAS Collaboration and other
    df_Arxiv['ATLAS Collaboration'].value_counts().plot(kind='bar')
    # Add title and labels
    plt.title('Papers published under the ATLAS Collaboration compared to Other')
    plt.xlabel('Authors')
    plt.ylabel('Number of papers')
    plt.xticks([1, 0], ['ATLAS Collaboration', 'Other'], rotation=0)
    plt.show()

    #Check if the paper has a search, measurement or other specific results using the title
    #First convert the title to lower case 
    df_Arxiv['title'] = df_Arxiv['title'].str.lower()
    #search for the words in the title
    df_Arxiv['Paper Type'] = df_Arxiv['title'].apply(lambda title: 'Search' if 'search' in title else ('Measurement' if 'measurement' in title else 'Other'))
    df_Arxiv['Paper Type'].value_counts().plot(kind='bar')
    plt.title('Number of paper per type of analysis')
    plt.xlabel('')
    plt.ylabel('Number of papers')
    plt.xticks(rotation=0)
    plt.show()

    #Save the data in the database
    database = "Arxiv_data"
    table = "Last_500_papers"
    #dop the columns Paper Type and ATLAS Collaboration
    del df_Arxiv['Paper Type'],df_Arxiv['ATLAS Collaboration'] 
    write_data_postgres(df_Arxiv,database,table)
    

if __name__ == '__main__':
    main()
