import streamlit as st
import streamlit.components.v1 as components

# lab logo and database description
st.markdown("# Meyers Database")
st.markdown("##### The __Meyers Database__ portal offers descriptions and interactive visualizations of data \
    utilized in scenario hubs, forecasts, or other scientific projects.\n ##### Its primary function is to facilitate \
    quick visualizations to aid in comprehending extensive datasets.")
st.divider()


# emoji keys
st.markdown("### What does the emoji before each page mean?")
st.markdown(":telescope:  real-world data")
st.markdown(":hammer_and_wrench:  simulated data")
st.divider()


# contact info
st.markdown("### Contact Us")
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.markdown(
        """
        <a href="http://www.bio.utexas.edu/research/meyers/">
            <img src="https://github.com/anjieliu121/virus_database/blob/main/images/lab_logo.png?raw=true" alt="Meyers Lab">
        </a>
        """,
        unsafe_allow_html=True
    )
# embedded meyers lab: does not show up when deployed
# iframe_src = "http://www.bio.utexas.edu/research/meyers/index.html"
# components.iframe(iframe_src, height=400, scrolling=True)
st.divider()

# author
st.markdown("### Other Resources")
# linkedin link
col1, col2, col3 = st.columns([0.3, 0.3, 0.4], vertical_alignment="top")
with col1:
    st.markdown("Database Author")
    st.markdown(
        """
        <a href="https://www.linkedin.com/in/anjie-liu-a73574253/">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="Repository" width="100" height="100">
        </a>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown("Open-Source Code & Data")
    st.markdown(
        """
        <a href="https://github.com/anjieliu121/virus_database">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="Repository" width="100" height="100">
        </a>
        """,
        unsafe_allow_html=True
    )