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
def read_states():
    df = pd.read_csv("utils/us-states.csv")
    return df


@st.cache_data(ttl=24 * 3600)
def add_lat_lon(df, state_column):
    states = read_states()
    result = pd.merge(df, states, left_on=state_column, right_on='name', how='left')
    result = result.drop(columns=['state', 'name'])
    return result


@st.cache_data(ttl=24 * 3600)
def add_state_fullname(df, state_abbr_column):
    states = read_states()
    result = pd.merge(df, states, left_on=state_abbr_column, right_on='state', how='left')
    result = result.drop(columns=['latitude', 'longitude'])
    result.insert(0, 'name', result.pop('name'))
    return result


@st.cache_data(ttl=24 * 3600)
def subset_df_col(df, cols_select):
    return df[cols_select]
