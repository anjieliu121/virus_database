import streamlit as st
from utils.data_io import read_json


# set up
st.header("2023 Respiratory Virus Response | COVID-19, Flu, RSV")
page = read_json("respiratory_viruses/megadata/response.json")
st.markdown(f">{page["description"]}")
st.markdown("Source: [link](%s)" % page["source"])
# download data, updated date, source
col1, col2, col3 = st.columns(3)
#with col1:
