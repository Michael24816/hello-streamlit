import streamlit as st
import pandas as pd

QUERY = """
SELECT * FROM `elegant-tendril-395105.1.cleaned_jobs`
LIMIT 100
"""

# Fetch data from BigQuery
def fetch_data(query):
    return pd.read_gbq(query, project_id="elegant-tendril-395105", dialect="standard", use_bqstorage_api=True)

# Use Streamlit to display the data
st.write(fetch_data(QUERY))