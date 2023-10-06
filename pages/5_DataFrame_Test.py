import streamlit as st
from google.cloud import bigquery

# Initialize a BigQuery client without specifying credentials
client = bigquery.Client(project="elegant-tendril-395105", credentials=None)

# Define the SQL query
QUERY = """
SELECT * FROM `elegant-tendril-395105.1.cleaned_jobs`
LIMIT 100
"""

# Fetch data from BigQuery
def fetch_data(query):
    return client.query(query).to_dataframe()

# Use Streamlit to display the data
st.write(fetch_data(QUERY))
