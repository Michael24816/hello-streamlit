import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
#from modules.formater import Title, Footer
from modules.importer import DataImport



# Title page and footer
title = "💸 Salaries"
#Title().page_config(title)
#Footer().footer()
st.title("Salaries")
# Import data
jobs_all = DataImport().get_data()


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

