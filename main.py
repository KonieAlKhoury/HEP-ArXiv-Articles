import feedparser

# Define the URL for the ArXiv API
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


def main():
    # This load the data of the last 200 papers in the 'hep-ph' category and from the ATLAS experiment
    query = 'cat:hep-ph+AND+all:ATLAS'
    max_results=200
    add_options = '&sortBy=lastUpdatedDate&sortOrder=descending'

    data = load_data(query , max_results, add_options)

    # Print the keys of the first entry to see what is in the data
    print(data.entries[0].keys())


    for entry in data.entries:
        print(entry.title)
        print(entry.summary)
        print("**")

if __name__ == '__main__':
    main()
