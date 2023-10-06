import streamlit as st
import requests
import pandas as pd

# Define the SQL query
QUERY = """
SELECT * FROM `elegant-tendril-395105.1.cleaned_jobs`
LIMIT 100
"""

# Fetch data from BigQuery using REST API
def fetch_data(query):
    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/elegant-tendril-395105/queries"
    data = {
        "query": query,
        "useLegacySql": False
    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        rows = response.json().get("rows", [])
        return pd.DataFrame([row["f"] for row in rows])
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return pd.DataFrame()

# Use Streamlit to display the data
st.write(fetch_data(QUERY))
