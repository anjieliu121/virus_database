import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px

from utils.data_io import read_json, read_df, add_lat_lon
from utils.buttons import download_full_data, single_select, multi_select
from utils.data_display import display_full_data, display_subset_data
from utils.text import explain_graph, data_contributor


# set up
st.markdown("# 2023 Respiratory Virus Response")
page = read_json("respiratory_viruses/megadata/response.json")
# SyntaxError: f-string: unmatched '[' -> inside f"", we cannot have another pair of double quotes, must be single quotes
st.markdown(f">{page['description']}")

# get data
file_path = f"{page['section']}/data/{page['file_name']}"
data_full = read_df(file_path)

# download data, updated date, source
download_full_data(file_path, page["file_name"], page["local_file_update_date"], page["source"])

# display data
display_full_data(data_full)

# visualization
st.markdown("## Interactive Data Visualization")

# graphs I want to make:
# map percent_visits for each pathogen at each week_end (evolve overtime)
# time-series for each state for one or more pathogens


st.markdown("##### Evolution of Pathogen Over Time in the United States")
# select pathogen
options_pathogen = page["columns"]["pathogen"]["values"]
chosen_pathogen = single_select("Select a Pathogen", options_pathogen, default=0, key="pathogen1")
# load geojson
with open("utils/us-states.json") as response:
    geo = json.load(response)
# prepare data
data_subset = data_full[data_full["pathogen"] == chosen_pathogen]
# ANIMATE MAP
explain_graph(f"Changing Percent Visits of {chosen_pathogen} in Emergency Department in the United States from {'2022-10-01'} to {'2024-06-22'}")
fig = px.choropleth_mapbox(
    data_subset,
    geojson=geo,
    locations='geography',
    featureidkey="properties.name",
    color='percent_visits',
    color_continuous_scale="sunsetdark",
    range_color=(data_subset.percent_visits.min(), data_subset.percent_visits.max()),
    opacity=0.5,
    hover_data=data_subset.columns,
    animation_frame='week_end',
)
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=2,
        center={"lat": 54, "lon": -118},
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.markdown("##### Pathogen at a Specific Week in the United States")
# select pathogen
options_pathogen = page["columns"]["pathogen"]["values"]
chosen_pathogen = single_select("Select a Pathogen", options_pathogen, default=0, key="pathogen2")
# select week
options_week = data_full["week_end"].unique().tolist()
chosen_week = single_select("Select a Week_End", options_week, default=0)
# prepare data
data_subset = data_full[(data_full["week_end"] == chosen_week) & (data_full["pathogen"] == chosen_pathogen)]
display_subset_data(data_subset, None, "geography")
# graph
explain_graph(f"Percent Visits of {chosen_pathogen} in Emergency Department in the United States in the Week Ending on {chosen_week}")
fig = px.choropleth_mapbox(
    data_subset,
    geojson=geo,
    locations='geography',
    featureidkey="properties.name",
    color='percent_visits',
    color_continuous_scale="sunsetdark",
    range_color=(data_subset.percent_visits.min(), data_subset.percent_visits.max()),
    opacity=0.5,
    hover_data=data_subset.columns
)
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=2.4,
        center={"lat": 54, "lon": -118},
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600
)
st.plotly_chart(fig, use_container_width=True)
st.divider()


st.markdown("##### Evolution of Pathogen Over Time in a Specific Geography")
# select geography
options_geography = page["columns"]["geography"]["values"]
chosen_geography = multi_select("Select a Geography", options_geography, "United States", "Texas")
# select pathogen
chosen_pathogen = multi_select("Select a Pathogen", options_pathogen, "COVID-19")
# prepare data
data_subset = data_full[data_full['geography'].isin(chosen_geography) & data_full['pathogen'].isin(chosen_pathogen)]
display_subset_data(data_subset, None, "geography")
data_subset['geography_pathogen'] = data_subset['geography'] + ' - ' + data_subset['pathogen']
# graph
explain_graph(f"Percent Visits of {chosen_pathogen} in Emergency Department in {chosen_geography} from {'2022-10-01'} to {'2024-06-22'}")
fig = px.line(
    data_subset,
    x='week_end',
    y='percent_visits',
    color='geography_pathogen',
    line_group='geography',
    #title='Income by Week End',
    #facet_col='geography',  # This will create a subplot for each country
    #facet_col_wrap=1,       # Adjust the wrapping of subplots if needed
    hover_data=data_full.columns
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)
st.divider()


data_contributor(page["upload_users"])



# unused but useful code snippets:
# shift an element of a list to the beginning of the list:
# options.insert(0, options.pop(options.index("United States")))
# data types:
# print(data_full.dtypes)
