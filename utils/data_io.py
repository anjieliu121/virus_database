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


@st.cache_data(ttl=24 * 3600)
def add_lat_lon(df, state_column):
    states = pd.read_csv("utils/us-states.csv")
    result = pd.merge(df, states, left_on=state_column, right_on='name')
    result = result.drop(columns=['state', 'name'])
    print("Note: add_lat_lon() will ignore 'United States'")
    return result
