# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Home",
        page_icon="👋",
    )

    st.write("# Data Analyst Job Market")

    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        ## Short description of the project  \n
        The aim of this project is to gain insight into the Data Analyst Job market in London, UK. \n
        The data used in this project is collected from the Google Jobs platform. \n
        Data is collected using SerpAPI. \n
        Data collection and cleaning is automated using Google Cloud Functions and Google Cloud Scheduler. \n
        Links:\n
        - [GitHub: Data Pipeline](https://github.com/Michael24816/Data-Analyst-Job-Market-Analysis) \n
        - [Data](https://storage.googleapis.com/jobs_data_1234/jobs_data.csv)
        - [GitHub: Website](https://github.com/Michael24816/hello-streamlit)
        - [LinkedIn](https://www.linkedin.com/in/michael-feduk) 

    """
    )


if __name__ == "__main__":
    run()
