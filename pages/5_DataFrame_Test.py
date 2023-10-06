import streamlit as st
import pandas_gbq

QUERY = """
SELECT * FROM `elegant-tendril-395105.1.cleaned_jobs`
LIMIT 100
"""

# Fetch data from BigQuery
def fetch_data(query):
    return pandas_gbq.read_gbq(query, project_id="elegant-tendril-395105", credentials=None, dialect="standard")

# Use Streamlit to display the data
st.write(fetch_data(QUERY))