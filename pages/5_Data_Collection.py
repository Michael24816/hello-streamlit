import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer
from modules.importer import DataImport



# Title page and footer
title = "💸 Data Collection"
#Title().page_config(title)
#Footer().footer()

st.title("Data Collection")

# Import data
jobs_all = DataImport().get_data()

jobs_all['date_time'] = pd.to_datetime(jobs_all['date_time'])
date_counts = jobs_all.groupby(jobs_all['date_time'].dt.date).size().reset_index(name='counts')
date_counts['7_day_avg'] = date_counts['counts'].rolling(window=7).mean()
date_counts_long = date_counts.melt(id_vars=['date_time'], value_vars=['counts', '7_day_avg'], 
                                    var_name='Metric', value_name='Value')



# Add a new column for the legend
date_counts['Metric'] = 'Counts'

base = alt.Chart(date_counts).encode(
    x=alt.X('date_time:T', title="Date")
)

# Create a line chart for counts
line_counts = base.mark_line().encode(
    y=alt.Y('counts:Q', title="Number of Job Postings"),
    color=alt.Color('Metric:N', legend=alt.Legend(title="Metric"), scale=alt.Scale(domain=['Counts', '7-Day Avg'], range=['blue', 'red']))
)

# Create a line chart for the 7-day moving average
line_avg = base.mark_line(strokeDash=[5,5]).encode(
    y=alt.Y('7_day_avg:Q'),
    color=alt.value('red')
)

# Adjust the nearest selection to only consider the 'x' encoding
nearest = alt.selection(type='single', nearest=True, on='mouseover', encodings=['x'], empty='none')


# Create a transparent selector (point) chart
selectors = base.mark_point().encode(
    opacity=alt.value(0)
).add_selection(
    nearest
)

# Add a rule (vertical line) that follows the cursor
rules = alt.Chart(date_counts).mark_rule(color='gray').encode(
    x='date_time:T'
).transform_filter(
    nearest
)

# Combine the charts and add the tooltip
date_chart = alt.layer(
    line_counts, line_avg, selectors, rules
).encode(
    tooltip=[
        alt.Tooltip('date_time:T', title='Date'),
        alt.Tooltip('counts:Q', title='Counts'),
        alt.Tooltip('7_day_avg:Q', title='7-Day Avg', format='.0f')  # Format to round to integer
    ]
).properties(
    title={'text': 'Job Postings Collected by Date', 'offset': 0},
    width=600,
    height=400
)

st.altair_chart(date_chart, use_container_width=True)

print("Note: This project stopped being maintained which is why you will see large gaps in data collection.")
