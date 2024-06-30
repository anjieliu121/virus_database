import streamlit as st

def display_full_data(df, notes=None):
    st.markdown("## Raw Data Preview")
    st.dataframe(df, use_container_width=True, height=265)
    if notes is not None:
        st.caption(f"Note: {notes}")


def display_subset_data(df, notes=None, sort_by=None):
    st.markdown("###### Filtered Data Preview")
    if sort_by:
        df = df.sort_values(by=sort_by, ascending=True, na_position='first')
    st.dataframe(df, use_container_width=True, height=160)
    if notes is not None:
        st.caption(f"Note: {notes}")
