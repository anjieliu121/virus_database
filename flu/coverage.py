import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.buttons import download_full_data, single_select, multi_select
from utils.data_display import display_full_data, display_subset_data
from utils.data_io import read_json, read_df
from utils.text import explain_graph

########################################################################################################################
#                                               set up                                                                 #
########################################################################################################################
# set up

page = read_json("flu/megadata/coverage.json")
data_path = f"{page['section']}/data/{page['file_name']}"

options_geography = page['columns']['Geography']['values']
options_age = page['columns']['Age']['values']


st.markdown(f"# {page['page_name']}")
st.markdown(f">{page['description']}")

# get data
data_full = read_df(data_path)

# download data, updated date, source
download_full_data(data_path, page["file_name"], page["local_file_update_date"], page["source"])

# display data
display_full_data(data_full)

########################################################################################################################
#                                               plots                                                                  #
########################################################################################################################
st.markdown("## Interactive Data Visualization")

########################################################################################################################
#                                               plot 1                                                                 #
########################################################################################################################
st.markdown("##### Flu Coverage by Age Groups in a Geography")


# select geography
chosen_geography = single_select("Select a Geography", options_geography, default="Texas", key="geography1")

# select y variable
# TODO: understand the difference between Y
options_y = ["flu.coverage.rd4.sc_A_B","flu.coverage.rd4.sc_C_D","flu.coverage.rd4.sc_E_F"]
chosen_y = single_select("Select a Y variable", options_y, default=0)

# select age groups
chosen_age = multi_select("Select at least one Age group", options_age, "6 Months - 4 Years","65+ Years")

# prepare data
data_subset = data_full[(data_full["Age"].isin(chosen_age)) & (data_full['Geography'] == chosen_geography)]
display_subset_data(data_subset)

# plot
explain_graph(f"2023-24 Flu Coverage in {chosen_geography}")
fig = px.line(
    data_subset,
    x='Week_Ending_Sat',
    y=chosen_y,
    color='Age',
    hover_data=data_full.columns
)

fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

########################################################################################################################
#                                               plot 2                                                                 #
########################################################################################################################
st.markdown("##### Flu Coverage Population in a Geography")

# select geography
chosen_geography = single_select("Select a Geography", options_geography, default="Texas", key="geography2")

# prepare data
data_subset = data_full[data_full['Geography'] == chosen_geography]
data_subset = data_subset[['Geography', 'Age', 'Population']]
data_subset = data_subset.drop_duplicates()
# sort by age group
data_subset['Age']=pd.Categorical(data_subset['Age'],categories=options_age)
data_subset=data_subset.sort_values('Age')



display_subset_data(data_subset)

# plot
explain_graph(f"2023-24 Flu Coverage Population in {chosen_geography}")
fig = px.bar(
    data_subset,
    x='Age',
    y='Population',
    hover_data=data_subset.columns
)

fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)


# unused but useful code snippets:
# print(np.unique(data_full["Geography"]).tolist())
# print(np.unique(data_full["Age"]).tolist())

# not successful sorting with a custom order
# age_group_order = {options_age[i]: i for i in range(len(options_age))}
# data_subset.sort_values(by=['Age'], key=lambda x: x.map(age_group_order))