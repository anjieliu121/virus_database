import streamlit as st

from utils.buttons import download_full_data
from utils.data_io import read_json

# set up
st.markdown("# 2011-2024 Flu Vaccine Effectiveness (VE) Estimates")
page = read_json("flu/megadata/vaccine_effectiveness.json")
st.markdown(f">{page['description']}")
download_full_data(None, None, None, page["source"], source_only=True)
