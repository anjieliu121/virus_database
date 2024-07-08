import math
import os
from st_files_connection import FilesConnection


import numpy as np
import streamlit as st
import pandas as pd
import json


@st.cache_data(ttl=24 * 3600)
def read_json(file_path):
    with open(file_path) as f:
        d = json.load(f)
    return d


@st.cache_data(ttl=24 * 3600)
def read_df(file_path, ignore_index=False, dtype=None):
    if ignore_index:
        df = pd.read_csv(file_path, index_col=0, dtype=dtype)
    else:
        df = pd.read_csv(file_path, dtype=dtype)
    #for c in df:
        #print(c, pd.unique(df[c]), "\n")
    return df


@st.cache_data(ttl=24 * 3600)
def read_df_gcp(file_path, ignore_index=False, dtype=None):
    # example file_path: case_surveillance/AL.csv
    conn = st.connection('gcs', type=FilesConnection)
    if ignore_index:
        df = conn.read(file_path, input_format="csv", index_col=0, dtype=dtype)# , ttl=600
    else:
        df = pd.read_csv(file_path, dtype=dtype)
    return df

# ClientConnectorCertificateError: Cannot connect to host storage.googleapis.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')]
# go to Python 3.12 folder, double click Install Certificates.command

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
    # deal with PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling
    # `frame.insert` many times, which has poor performance.
    # result.insert(0, 'name', result.pop('name'))
    columns = ['name'] + [col for col in result.columns if col != 'name']
    result = result[columns]
    return result


@st.cache_data(ttl=24 * 3600)
def get_state_fullname(state_abbr_list):
    states = read_states()
    states = states[states['state'].isin(state_abbr_list)]
    return states['name'].tolist()


@st.cache_data(ttl=24 * 3600)
def convert_to_state_abbreviation(state_fullname):
    states = read_states()
    states = states[states['name'] == state_fullname]
    return states['state'].iloc[0]


@st.cache_data(ttl=24 * 3600)
def subset_df_col(df, cols_select):
    return df[cols_select]


@st.cache_data(ttl=24 * 3600)
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@st.cache_data(ttl=24 * 3600)
def get_file_size_bytes(file_path):
    return os.path.getsize(file_path)


@st.cache_data(ttl=24 * 3600)
def get_df_size_bytes(df):
    return df.memory_usage(deep=True).sum()


@st.cache_data(ttl=24 * 3600)
def get_df_size(df):
    return convert_size(get_df_size_bytes(df))


@st.cache_data(ttl=24 * 3600)
def get_file_size(file_path):
    return convert_size(get_file_size_bytes(file_path))

@st.cache_data(ttl=24 * 3600)
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")