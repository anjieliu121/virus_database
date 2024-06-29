import streamlit as st
import json


@st.cache_data(ttl=24 * 3600)
def read_json(file_source):
    with open(file_source) as f:
        d = json.load(f)
    return d