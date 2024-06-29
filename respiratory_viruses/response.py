import streamlit as st
from utils.data_io import read_json, read_df
from utils.buttons import download_full_data, multi_select
from utils.data_display import display_full_data


# set up
st.markdown("# 2023 Respiratory Virus Response | COVID-19, Flu, RSV")
page = read_json("respiratory_viruses/megadata/response.json")
st.markdown(f">{page["description"]}")
# get data
file_path = f"{page["section"]}/data/{page["file_name"]}"
full_data = read_df(file_path)
# download data, updated date, source
download_full_data(file_path, page["file_name"], page["local_file_update_date"], page["source"])
# display data
display_full_data(full_data)
# visualization
options = full_data["geography"].unique().tolist()
options.insert(0, options.pop(options.index("United States")))
multi_select("Select a Geography", options, "United States")

