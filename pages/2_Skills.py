import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer
from modules.importer import DataImport



# Title page and footer
title = "💸 Skills"
#Title().page_config(title)
#Footer().footer()

st.title("Skills")

# Import data
jobs_all = DataImport().get_data()

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
