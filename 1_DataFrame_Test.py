import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer
from modules.importer import DataImport

# Title page and footer
title = "💸 Salary"
#Title().page_config(title)
#Footer().footer()



# Import data
jobs_all = DataImport().get_data()


# Top page build

st.title("Data Analyst Job Market")
# Flatten the skills column
skills_df = jobs_all.explode('skills')

# Count occurrences of each skill
skill_counts = skills_df['skills'].value_counts()

# Convert counts to percentages
skill_percentages = (skill_counts / len(jobs_all))

# Reset index for plotting
skill_percentages = skill_percentages.reset_index()
skill_percentages.columns = ['Skill', 'Percentage']
max_skill = skill_percentages['Percentage'].max()
adjusted_percentage_max = max_skill * 1.10


# Base chart
base = alt.Chart(skill_percentages).encode(
    y=alt.Y('Skill:N', sort='-x', title=None),
    x=alt.X('Percentage:Q', 
            title=None, 
            axis=alt.Axis(format='%', labels=False),
            scale=alt.Scale(domain=(0, max_skill))
            ),
    tooltip=[
        alt.Tooltip('Skill:N', title='Skill'), 
        alt.Tooltip('Percentage:Q', title='Percentage', format='.2%')
    ]
)

# Bar chart
bars = base.mark_bar().properties(
    title='Most Common Skills',
    width=800,
    height=400
)

# Text labels to the right of bars
text = base.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    color='white'
).encode(
    text=alt.Text('Percentage:Q', format='.2%')
)

# Combine bar chart and text labels
chart = (bars + text)

st.altair_chart(chart, use_container_width=True)




# Group by skills and calculate average salary
avg_salary_by_skill = skills_df.groupby('skills')['salary_adjusted'].mean().reset_index()

max_salary = avg_salary_by_skill['salary_adjusted'].max()
adjusted_max = max_salary * 1.10


# Get a sorted list of skills from the DataFrame to order the chart
sorted_skills = avg_salary_by_skill.sort_values(by='salary_adjusted', ascending=False)['skills'].tolist()


avg_salary_by_skill['salary_with_symbol'] = avg_salary_by_skill['salary_adjusted'].apply(lambda x: f"£{x:,.0f}")

base = alt.Chart(avg_salary_by_skill)

bars = base.mark_bar().encode(
    x=alt.X('salary_adjusted:Q', 
            title=None,
            axis=alt.Axis(labels=False), 
            scale=alt.Scale(domain=(0, adjusted_max))
           ),
    y=alt.Y('skills:N', sort=sorted_skills, title=None),
    tooltip=[
        alt.Tooltip('skills:N', title='Skill'), 
        alt.Tooltip('salary_with_symbol:N', title='Salary')
    ]
).properties(
    title='Average Salary by Skill',
    width=600,
    height=400
)

text = base.mark_text(
    align = 'left',
    baseline = 'middle',
    dx = 3,
    color = 'white'
).encode(
    x=alt.X('salary_adjusted:Q'),
    y=alt.Y('skills:N', sort=sorted_skills),
    text='salary_with_symbol:N'
)

chart = (bars + text)
st.altair_chart(chart, use_container_width=True)


# Salaries

salary_df = jobs_all[['title', 'company_name', 'salary_adjusted' ]] # select columns
salary_df = salary_df[salary_df['salary_adjusted'].notna()]
salary_df['salary_adjusted'] = salary_df['salary_adjusted'].astype(int)


chart_with_titles = alt.Chart(salary_df).mark_bar().encode(
    #x=alt.X('salary_adjusted', title="Salary (£ per annum)", bin=alt.Bin(step=5000)),  # Set the step size for bins
    x=alt.X('salary_adjusted', 
            title="Salary (£ per annum)", 
            bin=alt.Bin(step=5000)
            #axis=alt.Axis(format="£,d")  # Format axis labels with £ and commas
            
           ),
    y=alt.Y('count()', title="Number of Job Postings")
).properties(
    title={'text': 'Salary distribution', 'offset': 0},
    width=600,
    height=400
)
st.altair_chart(chart_with_titles)



# Platforms

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



