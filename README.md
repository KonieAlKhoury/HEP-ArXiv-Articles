# HEP-ArXiv-Articles

This project is dedicated to analysing ghe articles published to ArXiv for the High Energy Physics (HEP) and the ATLAS experiment.

The analysis includes:

- Reading and processing the last 500 published articles, using metadata such as title, summary, and authors.
- Extracting and analyzing the metadata, to ensure its accuracy and quality.
- Process the data from the articles and store them in a PostgreSQL database, which allows for efficient querying and data analysis.
- Performing text analysis on the articles' summaries and titles.
- Using machine learning techniques to classify the articles based on their content.

This project aims to provide insights into the current research trends in High Energy Physics and the ATLAS experiment, and to demonstrate how data science techniques can be applied to analyse and classify the large sets of academic articles.


## Getting Started

These instructions will help setup the enviroment needed to run the code

This project uses Python 3. You can check your Python version with the following command:

```bash
python --version
```
The packages that are needed to run the code, you can install them running the following:

```bash
pip3 install -r requirements.txt
```

## Structure

This project has the following structure:

- `src/`: This directory contains all the code for the project.
  - `PapersExtraction.py`: This script handles the extraction of Arxiv data and performing analysis to check the accuracy of the data.
  - `PostgresConnection.py`: This script contains functions to connect to PostgreSQL database and query/write tables 
  - `DataPreparation.py`: This script reads the postgres table, then process and structure the data 
  - `WordsOccurences.py`: This scripts allows to performce analysis on the occurencies in the articles' summaries and titles
  - `ModelPrediction.py`: This scripts contains machine learning model training, and applies the model to make predictions.
- `requirements.txt`: This file lists the dependencies that need to be installed.
- `README.md`: This file provides an overview of the project.



Another way to import is using arxiv library
```python
import arxiv

#Define the search query for the ArXiv API
#This query will return the last 100 papers in the 'hep-ph' category
query = 'cat:hep-ph AND all:ATLAS'

# # Use arxiv to fetch the data
search = arxiv.Search(query=query, max_results=500, sort_by=arxiv.SortCriterion.SubmittedDate)

# # Print the titles of the papers
for result in search.results():
    print(result.title)
```