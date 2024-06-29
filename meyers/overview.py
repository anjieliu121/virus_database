import streamlit as st
import streamlit.components.v1 as components

# lab logo and database description
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image('images/database_logo.png')
with col2:
    st.header("The Meyers Database portal offers descriptions and interactive visualizations of data \
    utilized in scenario hubs, forecasts, or other scientific projects.\nIts primary function is to facilitate \
    quick visualizations to aid in comprehending extensive datasets.")
st.divider()


# emoji keys
st.header("What does the emoji before each page mean?")
st.markdown(":telescope:  real-world data")
st.markdown(":hammer_and_wrench:  simulated data")
st.divider()


# contact info
st.header("Contact Us")
# embedded meyers lab
iframe_src = "http://www.bio.utexas.edu/research/meyers/index.html"
components.iframe(iframe_src, height=400, scrolling=True)
# linkedin link
st.link_button(f"Contact Web Creator 👈", "https://www.linkedin.com/in/anjie-liu-a73574253/")