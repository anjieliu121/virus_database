import streamlit as st

def display_full_data(df, notes=None):
    st.markdown("## Data Preview")
    st.dataframe(df, use_container_width=True, height=265)
    if notes is not None:
        st.caption(f"Note: {notes}")