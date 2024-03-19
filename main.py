import feedparser

# Define the URL for the ArXiv API
def load_data(query , max_results, add_options=''):
 
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



# This load the data of the last 200 papers in the 'hep-ph' category and from the ATLAS experiment
query = 'cat:hep-ph+AND+all:ATLAS'
max_results=200
add_options = '&sortBy=lastUpdatedDate&sortOrder=descending'

data = load_data(query , max_results, add_options)

# Print the keys of the first entry to see what is in the data
print(data.entries[0].keys())


# for entry in data.entries:
#     print(entry.title)
#     print(entry.summary)
#     print("**")
