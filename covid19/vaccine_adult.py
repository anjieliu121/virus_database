import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.buttons import download_full_data, single_select, multi_select
from utils.data_display import display_full_data, display_cols, display_subset_data
from utils.data_io import read_json, read_df, add_state_fullname
from utils.text import explain_graph, data_contributor

########################################################################################################################
#                                               set up                                                                 #
########################################################################################################################
# set up
page = read_json("covid19/megadata/vaccine_adult.json")
data_path = f"{page['section']}/data/{page['file_name']}"

options_geographic_level = page["columns"]["Geographic Level"]["values"]
relationship_geographic_level = page["columns"]["Geographic Level"]["relationship"]
options_demographic_level = page["columns"]["Demographic Level"]["values"]
relationship_demographic_level = page["columns"]["Demographic Level"]["relationship"]
options_indicator_label = page["columns"]["indicator_label"]["values"]
relationship_indicator_label = page["columns"]["indicator_label"]["relationship"]

st.markdown(f"# {page['page_name']}")
st.markdown(f">{page['description']}")

# get data
data_full = read_df(data_path)
cols = list(page['columns'].keys())

# download data, updated date, source
download_full_data(data_path, page["file_name"], page["local_file_update_date"], page["source"])

# display data
display_full_data(data_full)

# display column description
display_cols(page["columns"])

########################################################################################################################
#                                               plots                                                                  #
########################################################################################################################
st.markdown("## Interactive Data Visualization")

#print(np.unique(data_full['Demographic Level']).tolist())
#for i in np.unique(data_full['Demographic Level']).tolist():
#    data_subset = data_full[data_full['Demographic Level'] == i]
#    print(i, np.unique(data_subset['Demographic Name']).tolist())
########################################################################################################################
#                                               plot 1                                                                 #
########################################################################################################################
st.markdown("##### Weekly Estimates by Geography")

# select geographic level
chosen_geographic_level = single_select("Select a Geographic Level", options_geographic_level, default="State")

# select geography
options_geography = relationship_geographic_level[chosen_geographic_level]["values"]
chosen_geography = multi_select("Select at least one Geographic Region", options_geography, relationship_geographic_level[chosen_geographic_level]["default"])

if chosen_geographic_level == "National":
    # select demographic level
    chosen_demographic_level = single_select("Select a Demographic Level", options_demographic_level, default="Poverty Status")

    # select demographic name
    options_demographic_name = relationship_demographic_level[chosen_demographic_level]["values"]
    chosen_demographic_name = multi_select("Select at least one Demographic Name", options_demographic_name, relationship_demographic_level[chosen_demographic_level]["default"])

# select indicator level
chosen_indicator_level = single_select("Select an Indicator Level", options_indicator_label, default=0, key="indicator_label1")

# select indicator category label
options_indicator_category_label = relationship_indicator_label[chosen_indicator_level]["values"]
chosen_indicator_category_label = multi_select("Select at least one Indicator Category Label", options_indicator_category_label, relationship_indicator_label[chosen_indicator_level]["default"], key="indicator_category1")

# prepare data
if chosen_geographic_level == "National":
    data_subset = data_full[(data_full['Geographic Name'].isin(chosen_geography)) & (data_full['Demographic Level'] == chosen_demographic_level)  & (data_full['Demographic Name'].isin(chosen_demographic_name)) & (data_full['indicator_category_label'].isin(chosen_indicator_category_label))]
else:
    data_subset = data_full[(data_full['Geographic Name'].isin(chosen_geography)) & (data_full['indicator_category_label'].isin(chosen_indicator_category_label))]
display_subset_data(data_subset, "Only [National] has [Demographic Level] options.")
data_subset = data_subset.copy()  # deal with SettingWithCopyWarning
data_subset.loc[:, 'geography_demography_indicator_category'] = data_subset['Geographic Name'] + ' - ' + data_subset['Demographic Name'] + ' - ' + data_subset['indicator_category_label']
data_subset['Week_ending'] = pd.to_datetime(data_subset['Week_ending'], format='%m/%d/%Y %I:%M:%S %p')
data_subset = data_subset.sort_values("Week_ending")

# plot
if chosen_geographic_level == "National":
    explain_graph(f"Status of Adults in {chosen_geography} who are {chosen_demographic_name} on receiving the updated 2023-24 COVID-19 vaccine from {'2023-9-30'} to {'2024-05-11'}")
else:
    explain_graph(f"Status of Adults in {chosen_geography} on receiving the updated 2023-24 COVID-19 vaccine from {'2023-9-30'} to {'2024-05-11'}")

fig = px.line(
    data_subset,
    x='Week_ending',
    y='Estimate',
    color='geography_demography_indicator_category',
    hover_data=data_full.columns
)

fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

data_contributor(page["upload_users"])

# unused but useful information

# when having 2 column conditions
# (1) first subset on one condition, then subset on the second condition: 0.003303050994873047 seconds
# (2) subset on two conditions at once:                                   0.0030248165130615234 seconds
# (3) only subset on 1 condition: 0.0018818378448486328 seconds

# find execution time
# start_time = time.time()
# main()
# print("--- %s seconds ---" % (time.time() - start_time))

# print(chosen_demographic_level, np.unique(data_subset["Demographic Name"]).tolist())
# print(chosen_indicator_level, np.unique(data_subset["indicator_category_label"]).tolist())

#print(data_subset[['Week_ending', 'Demographic Level', 'Geographic Name', 'Estimate']])
