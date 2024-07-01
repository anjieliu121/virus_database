import streamlit as st
import plotly.express as px

from utils.buttons import download_full_data, single_select
from utils.data_display import display_full_data, display_filter_cols, display_cols, display_subset_data
from utils.data_io import read_json, read_df, add_state_fullname
from utils.text import explain_graph, data_contributor

########################################################################################################################
#                                               set up                                                                 #
########################################################################################################################
# set up
page = read_json("covid19/megadata/patient_impact_hospital_capacity.json")
data_path = f"{page['section']}/data/{page['file_name']}"

st.markdown(f"# {page['page_name']}")
st.markdown(f">{page['description']}")

# get data
data_full = read_df(data_path)
cols = list(page['columns'].keys())

# download data, updated date, source
download_full_data(data_path, page["file_name"], page["local_file_update_date"], page["source"])

# add state full name to dataset
data_full = add_state_fullname(data_full, "state")

# display data
display_full_data(data_full, "The first column 'name' is not a part of the original data. It is added for clearer interpretability. ")

# display column description
display_cols(page["columns"])

# display data by column names
display_filter_cols(data_full, cols, "adult, pediatric")

########################################################################################################################
#                                               plots                                                                  #
########################################################################################################################
st.markdown("## Interactive Data Visualization")


########################################################################################################################
#                                               plot                                                                   #
########################################################################################################################
st.markdown("##### Timeseries of a Variable in a State")

# select state
options_states = page["columns"]["state"]["values"]
chosen_state = single_select("Select a State / Federal district / Inhabited territories in the U.S.", options_states, default="Texas")

# select variable
options_y = list(page["columns"].keys())
options_y.remove("state")
options_y.remove("date")
chosen_y = single_select("Select a variable on the y-axis", options_y, default=0)

# prepare data
data_subset = data_full[data_full["name"] == chosen_state]
display_subset_data(data_subset, None, "date")

# graph
explain_graph(f"{chosen_y} in {chosen_state} from {'2020-1-1'} to {'2024-4-27'}")
fig = px.scatter(
    data_subset,
    x='date',
    y=chosen_y,
    hover_data={"name":True}
)
fig.update_layout(
    height=600,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

data_contributor(page["upload_users"])







# unused but useful code snippets:
# sort unique items:
# options_states = sorted(data_full["name"].unique())

