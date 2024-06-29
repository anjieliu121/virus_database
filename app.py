import streamlit as st
from utils.data_io import read_json

st.set_page_config(
    layout="wide"
)

pages_json = read_json('pages.json')

pages = {
    "meyers": [],
    "respiratory_viruses": [],
}

for k in pages_json.keys():
    for i in pages_json[k]:
        page = st.Page(page=i["source"], title=i["title"], icon=i["icon"], url_path=i["url_path"], default=i["default"])
        pages[k].append(page)


pg = st.navigation(
    {
        "Meyers Database": pages["meyers"],
        "Respiratory Viruses": pages["respiratory_viruses"],
        "COVID-19": [],
        "Flu": [],
        "RSV": [],
        "Bird Flu": []
    }
)

# add ut logo to sidebar
# st.sidebar.image("https://github.com/anjieliu121/virus_database/blob/main/images/database_logo.png?raw=true")
st.sidebar.image("https://github.com/anjieliu121/virus_database/blob/main/images/ut_logo.png?raw=true")
# css
with open('utils/style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

pg.run()

