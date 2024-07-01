import streamlit as st

from utils.buttons import single_select
from utils.data_io import subset_df_col
from utils.text import column_description


def display_full_data(df, notes=None):
    st.markdown("## Raw Data Preview")
    st.dataframe(df, use_container_width=True, height=265)
    if notes is not None:
        st.caption(f"Note: {notes}")


def display_subset_data(df, notes=None, sort_by=None):
    st.markdown("Filtered Data Preview")
    if sort_by:
        df = df.sort_values(by=sort_by, ascending=True, na_position='first')
    st.dataframe(df, use_container_width=True, height=160)
    if notes is not None:
        st.caption(f"Note: {notes}")


def display_cols(columns):
    st.markdown("##### Column Description")
    chosen_column = single_select("Select a column to view its description", columns.keys(), default=0, key=None)
    description = columns[chosen_column]
    if isinstance(description, str):
        column_description(description)
    else:
        column_description(description["description"])


def display_filter_cols(df, cols, sample_search_text):
    st.markdown("##### Filter Data by Columns")
    st.warning("Filtered columns will not affect the visualization below.", icon="⚠️")
    # TODO: add css to text_input() in style.css
    search_phrases = st.text_input('I want column names that contain phrases like ... (separate each word by a comma)', sample_search_text)
    search_list = [i.strip().lower() for i in search_phrases.split(",")]
    cols_select = [col for col in cols if any(word in col.lower() for word in search_list)]
    df = subset_df_col(df, cols_select)
    st.dataframe(df, use_container_width=True, height=160)
