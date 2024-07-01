import streamlit as st

from utils.buttons import download_full_data
from utils.data_io import read_json

########################################################################################################################
#                                               set up                                                                 #
########################################################################################################################
page = read_json("flu/megadata/vaccine_effectiveness.json")
data_path = f"{page['section']}/data/{page['file_name']}"

st.markdown(f"# {page['page_name']}")
st.markdown(f">{page['description']}")

# get data
# data_full = read_df(file_path)

# download data, updated date, source
download_full_data(data_path, page["file_name"], page["local_file_update_date"], page["source"])
