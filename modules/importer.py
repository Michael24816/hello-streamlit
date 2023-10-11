import pandas as pd
import streamlit as st
import numpy as np


class DataImport:
    """"
    Import data from CSV file on Google Cloud
    """
    def __init__(self):
        pass

    @staticmethod
    @st.cache_data(ttl=60*60)
    def get_data():
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

        # Convert nans to empty lists
        jobs_all['skills'] = jobs_all['skills'].apply(lambda x: [] if isinstance(x, float) and np.isnan(x) else x)
        skills = [item for sublist in jobs_all['skills'].tolist() for item in sublist]
        skills = list(set(skills))

        # Remove the word 'via' from values in the platform column 
        jobs_all['via'] = jobs_all['via'].apply(lambda x: x.replace("via ", "") if isinstance(x, str) else x)

        return jobs_all