import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer


# Title page and footer
title = "💸 Salary"
#Title().page_config(title)
#Footer().footer()

# Import data
data_url = 'https://storage.googleapis.com/jobs_data_1234/jobs_data.csv'
jobs_all = pd.read_csv(data_url)

columns_to_convert = ['skills_string','extensions_string']
for col in columns_to_convert:
    jobs_all[col] = jobs_all[col].str.split('|')

jobs_all.rename(columns={'skills_string': 'skills', 'extensions_string': 'extensions'}, inplace=True)


# Remove salaries below £20,000 (below minimum wage - error)
jobs_all['salary_adjusted'][jobs_all['salary_adjusted'] < 20000] = np.nan

# Remove salaries above £500,000 (most likely salary extraction error)
jobs_all['salary_adjusted'][jobs_all['salary_adjusted'] > 500000] = np.nan

# Drop rows without salary data
jobs_data = jobs_all[jobs_all.salary_adjusted.notna()] 

# Convert nans to empty lists
jobs_all['skills'] = jobs_all['skills'].apply(lambda x: [] if isinstance(x, float) and np.isnan(x) else x)
skills = [item for sublist in jobs_all['skills'].tolist() for item in sublist]
skills = list(set(skills))


# Flatten the skills column
skills_df = jobs_all.explode('skills')

# Count occurrences of each skill
skill_counts = skills_df['skills'].value_counts()

# Convert counts to percentages
skill_percentages = (skill_counts / len(jobs_all)) * 100

# Reset index for plotting
skill_percentages = skill_percentages.reset_index()
skill_percentages.columns = ['Skill', 'Percentage']

# Remove the word 'via' from values in the platform column 
jobs_all['via'] = jobs_all['via'].apply(lambda x: x.replace("via ", "") if isinstance(x, str) else x)



# Top page build

st.title("Data Analyst Job Market")


# Plot using Altair
chart = alt.Chart(skill_percentages).mark_bar().encode(
    x=alt.X('Skill:N', sort='-y', title='Skill'),
    y=alt.Y('Percentage:Q', title='Percentage of Job Postings (%)'),
    tooltip=[
    alt.Tooltip('Skill:N', title='Skill'), 
    alt.Tooltip('Percentage:Q', title='Percentage', format='.2f')]
).properties(
    title={'text': 'Skills', 'offset': 0},
    width=800,
    height = 400
)

st.altair_chart(chart, use_container_width=True)

# Explode the skills column
exploded_df = jobs_all.explode('skills')

# Group by skills and calculate average salary
avg_salary_by_skill = exploded_df.groupby('skills')['salary_adjusted'].mean().reset_index()

# Plot using Altair
chart = alt.Chart(avg_salary_by_skill).mark_bar().encode(
    x=alt.X('skills:N', sort='-y'),
    y=alt.Y('salary_adjusted:Q', title='Salary (£ per annum)'),
    tooltip=[
        alt.Tooltip('skills:N', title='Skill'), 
        alt.Tooltip('salary_adjusted:Q', title='Average Salary', format='.0f')
    ]
).properties(
    title='Average Salary by Skill',
    width= 600,
    height = 400
)

st.altair_chart(chart, use_container_width=True)


# Use the yearly salary column directly

salary_df = jobs_all[['title', 'company_name', 'salary_adjusted' ]] # select columns
salary_df = salary_df[salary_df['salary_adjusted'].notna()]
salary_df['salary_adjusted'] = salary_df['salary_adjusted'].astype(int)


chart_with_titles = alt.Chart(salary_df).mark_bar().encode(
    x=alt.X('salary_adjusted', title="Salary (£ per annum)", bin=alt.Bin(step=5000)),  # Set the step size for bins
    y=alt.Y('count()', title="Number of Job Postings")
).properties(
    title={'text': 'Salary distribution', 'offset': 0},
    width=600,
    height=400
)
st.altair_chart(chart_with_titles)



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


# Trends

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



