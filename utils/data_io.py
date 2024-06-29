import streamlit as st
import pandas as pd
import json


@st.cache_data(ttl=24 * 3600)
def read_json(file_path):
    with open(file_path) as f:
        d = json.load(f)
    return d

@st.cache_data(ttl=24 * 3600)
def read_df(file_path):
    df = pd.read_csv(file_path)
    return df