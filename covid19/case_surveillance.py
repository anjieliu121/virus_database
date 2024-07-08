import os
import math

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from utils.buttons import single_select, download_full_data, download_full_data_gcp
from utils.data_display import display_full_data, display_cols, display_subset_data
from utils.data_io import read_json, read_df, read_states, get_state_fullname, convert_to_state_abbreviation, \
    add_state_fullname, read_df_gcp
from utils.text import explain_graph, data_contributor

########################################################################################################################
#                                               set up                                                                 #
########################################################################################################################
# set up
page = read_json("covid19/megadata/case_surveillance.json")
states = page['columns']['res_state']['values']
states_util = read_states()
cols = list(page['columns'].keys())
dates = page['columns']['case_month']['values']
# deal with DtypeWarning: Columns (4) have mixed types. Specify dtype option on import or set low_memory=False.
dtypes = {c: page['columns'][c]['dtype'] for c in page['columns']}

# multiple files
data_paths = {}
file_names = {}
for i in states:
    # temp = f"{page['section']}/data/{page['folder_name']}/{i}.csv"
    temp = f"meyers_database/raw/{page['folder_name']}/{i}.csv"
    # temp = f"meyers_database/raw/case_surveillance/AL.csv"
    data_paths[i] = temp

    temp = f"{page['file_name']}_{i}"
    file_names[i] = temp

st.markdown(f"# {page['page_name']}")
st.markdown(f">{page['description']}")

# select state
options_states = get_state_fullname(states)
chosen_state_fullname = single_select("Select a State / Federal district / Inhabited territories in the U.S.", options_states,
                             default="Alaska")
chosen_state = convert_to_state_abbreviation(chosen_state_fullname)

# get data
# data_full = read_df(data_paths[chosen_state], ignore_index=True, dtype=dtypes)
data_full = read_df_gcp(data_paths[chosen_state])


# download data, updated date, source
#download_full_data(data_paths[chosen_state], file_names[chosen_state], page["local_file_update_date"], page["source"])
download_full_data_gcp(data_full, file_names[chosen_state], page["local_file_update_date"], page["source"])

# add state full name to dataset
# data_full = add_state_fullname(data_full, "res_state")

# display data
#notes="The first column 'name' is not a part of the original data. It is added for clearer interpretability. "
display_full_data(data_full)

# display column description
display_cols(page["columns"])


########################################################################################################################
#                                               plots                                                                  #
########################################################################################################################
st.markdown("## Interactive Data Visualization")


########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Case Count per Month")

# prepare data
data_group = data_full.groupby('case_month').size().reset_index(name='count')

# graph
explain_graph(f"Total case number per month in {chosen_state_fullname} from {'2020-1'} to {'2024-6'}")
fig = px.bar(
    data_group,
    x='case_month',
    y='count'
)
fig.update_traces(
    hovertemplate='<b>month</b>: %{x}<br>' +
                      '<b>count</b>: %{y}<br>' +
                      f'<b>state</b>: {chosen_state_fullname}<extra></extra>'
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)
st.divider()


########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Category Proportion of a Variable across Time")

# select variable
options_cols = [c for c in cols if c not in ['case_month', 'res_state', 'state_fips_code', 'county_fips_code', 'case_positive_specimen_interval', 'case_onset_interval']]
chosen_column = single_select("Select a variable", options_cols, default="race", key="col2")

# prepare data
months = np.sort(data_full['case_month'].unique())
categories = data_full[chosen_column].unique()
categories = [str(c) for c in categories] # deal with np.nan and TypeError with np.isnan() and np.isfinite()
for i in ['Unknown', 'Missing', 'nan']:
    if i in categories:
        categories.append(categories.pop(categories.index(i)))
# TODO: check why np.nan exists if the count of it is 0
# create empty df with full categories for each month
template = pd.MultiIndex.from_product([months, categories], names=['case_month', chosen_column])
template_df = pd.DataFrame(index=template).reset_index()
# merge template with actual data
data_group = data_full.groupby(['case_month', chosen_column]).size().reset_index(name='count')
data_group = pd.merge(template_df, data_group, on=['case_month', chosen_column], how='left').fillna(0)
data_group['total_count_by_month'] = data_group.groupby('case_month')['count'].transform('sum')
data_group['proportion'] = data_group['count'] / data_group['total_count_by_month']
# sort df by month
display_subset_data(data_group)

# plot
explain_graph(f"Change in proportion of each {chosen_column} category from {'2020-01'} to {'2024-06'}")
fig = px.bar(data_group,
             x=chosen_column,
             y='proportion',
             color=chosen_column,
             animation_frame='case_month',
             range_y=[0,1],
)
fig.update_traces(
    hovertemplate=f'<b>{chosen_column}</b>: %{{x}}<br>' +
                   '<b>count</b>: %{customdata[0]}<br>' +
                   '<b>proportion</b>: %{y}<br>' +
                  f'<b>state</b>: {chosen_state_fullname}<extra></extra>',
    customdata=data_group[["count"]]
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

# plot
explain_graph(f"Timeseries proportion of each {chosen_column} category from {'2020-01'} to {'2024-06'}")
fig = px.bar(data_group,
             x='case_month',
             y='proportion',
             color=chosen_column,
             range_y=[0,1],
)
fig.update_traces(
    hovertemplate=f'<b>{chosen_column}</b>: %{{x}}<br>' +
                   '<b>count</b>: %{customdata[0]}<br>' +
                   '<b>proportion</b>: %{y}<br>' +
                  f'<b>state</b>: {chosen_state_fullname}<extra></extra>',
    customdata=data_group[["count"]]
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Distribution of Categorical Variable in a Month")

# select variable
options_cols = [c for c in cols if c not in ['case_month', 'res_state', 'state_fips_code', 'county_fips_code', 'case_positive_specimen_interval', 'case_onset_interval']]
chosen_column = single_select("Select a variable", options_cols, default="race", key="col3")

# select month
chosen_month = single_select("Select a month (Note: An empty table means there are no data in this month)", dates, default='2020-03')

# prepare data
data_subset = data_full[data_full["case_month"] == chosen_month]
display_subset_data(data_subset, None, "case_month")

data_group = data_full.groupby([chosen_column]).size().reset_index(name='count')


# plot
explain_graph(f"Count of each {chosen_column} category in {chosen_state_fullname} in {chosen_month}")
fig = px.bar(data_group,
             x=chosen_column,
             y='count',
             color=chosen_column,
)
fig.update_traces(
    hovertemplate=f'<b>{chosen_column}</b>: %{{x}}<br>' +
                   '<b>count</b>: %{y}<br>' +
                  f'<b>state</b>: {chosen_state_fullname}<extra></extra>'
)
fig.update_layout(
    xaxis={'categoryorder':'total descending'},
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)
st.divider()


########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Timeseries Plot of Numerical Variables")

# select variable
options_numeric = ['case_positive_specimen', 'case_onset_interval']
chosen_numeric = single_select("Select a numerical variable", options_numeric, default=0)

# plot
explain_graph(f"{chosen_numeric} in {chosen_state_fullname} from {'2020-01'} to {'2024-06'}")
fig = px.scatter(
    data_full,
    x='case_month',
    y=chosen_numeric,
    hover_data={"res_state":True}
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)
st.divider()


########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Interaction between Categorical Variables")

# select x
options_x = ['age_group', 'sex', 'race', 'ethnicity']
chosen_x = single_select("Select an independent variable on the x-axis", options_x, default=0)

# select y
options_y = options_cols
options_y.remove(chosen_x)
chosen_y = single_select("Select a dependent variable", options_y, default="icu_yn")

# prepare data
data_group = data_full.groupby([chosen_x, chosen_y]).size().reset_index(name='count')
data_group[f'total_count_by_{chosen_x}'] = data_group.groupby(chosen_x)['count'].transform('sum')
data_group['proportion'] = data_group['count'] / data_group[f'total_count_by_{chosen_x}']
display_subset_data(data_group)

# plot
explain_graph(f"{chosen_y} by {chosen_x} in {chosen_state_fullname}")
fig = go.Figure()
y_categories = data_group[chosen_y].unique()
for category in y_categories:
    category_df = data_group[data_group[chosen_y] == category]
    fig.add_trace(go.Scatter(
        x=category_df[chosen_x],
        y=category_df['count'],
        mode='lines+markers',
        name=category
    ))
fig.update_layout(
    xaxis_title=chosen_x,
    yaxis_title="count",
    hovermode="x unified"
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

# plot
explain_graph(f"Proportion of {chosen_y} by {chosen_x} in {chosen_state_fullname}")
fig = px.bar(data_group,
             x=chosen_x,
             y='proportion',
             color=chosen_y,
             range_y=[0, 1],
)
fig.update_traces(
    hovertemplate=f'<b>{chosen_x}</b>: %{{x}}<br>' +
                  f'<b>count</b>: %{{customdata[0]}}<br>' +
                  f'<b>proportion</b>: %{{y}}<br>' +
                  f'<b>state</b>: {chosen_state_fullname}<extra></extra>',
    customdata=data_group[["count"]]
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

# prepare data
data_subset = data_full[~data_full[chosen_y].isin(['Missing', 'Unknown'])]
data_subset = data_subset[~data_subset[chosen_x].isin(['Missing', 'Unknown'])]
data_group = data_subset.groupby([chosen_x, chosen_y]).size().reset_index(name='count')
data_group[f'total_count_by_{chosen_x}'] = data_group.groupby(chosen_x)['count'].transform('sum')
data_group['proportion'] = data_group['count'] / data_group[f'total_count_by_{chosen_x}']
display_subset_data(data_group)

# plot
explain_graph(f"Proportion of {chosen_y} by {chosen_x} in {chosen_state_fullname}  (rows with missing values are removed)")
fig = px.bar(data_group,
             x=chosen_x,
             y='proportion',
             color=chosen_y,
             range_y=[0, 1],
)
fig.update_traces(
    hovertemplate=f'<b>{chosen_x}</b>: %{{x}}<br>' +
                  f'<b>count</b>: %{{customdata[0]}}<br>' +
                  f'<b>proportion</b>: %{{y}}<br>' +
                  f'<b>state</b>: {chosen_state_fullname}<extra></extra>',
    customdata=data_group[["count"]]
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

data_contributor(page["upload_users"])
