# HEP-ArXiv-Articles

Another way to import is using arxiv library
# import arxiv

# # Define the search query for the ArXiv API
# # This query will return the last 100 papers in the 'hep-ph' category
# query = 'cat:hep-ph AND all:ATLAS'

# # Use arxiv to fetch the data
# search = arxiv.Search(query=query, max_results=100, sort_by=arxiv.SortCriterion.SubmittedDate)

# # Print the titles of the papers
# for result in search.results():
#     print(result.title)
