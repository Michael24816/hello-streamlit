import streamlit as st
from google.cloud import bigquery
from google.auth.credentials import AnonymousCredentials

# Initialize a BigQuery client with anonymous credentials
client = bigquery.Client(credentials=AnonymousCredentials(), project="elegant-tendril-395105")

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
