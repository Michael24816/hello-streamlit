import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer
from modules.importer import DataImport



# Title page and footer
title = "💸 Platforms"
#Title().page_config(title)
#Footer().footer()

st.title("Platforms")

# Import data
jobs_all = DataImport().get_data()


# Group by platform and count the number of jobs
platform_counts = jobs_all.groupby('via').size().reset_index(name='counts')

# Sort by counts and select the top 10 platforms
top_platforms = platform_counts.sort_values(by='counts', ascending=False).head(10)

# Create a bar chart for the number of jobs by top 10 platforms
platform_chart = alt.Chart(top_platforms).mark_bar().encode(
    x=alt.X('via', title="Platform", sort='-y'),  # Sorting bars by count
    y=alt.Y('counts', title="Number of Job Postings"),
    tooltip=['via', 'counts']
).properties(
    title={'text': 'Top 10 Platforms by Job Postings', 'offset': 0},
    width=600,
    height=400
)

st.altair_chart(platform_chart, use_container_width=True)
