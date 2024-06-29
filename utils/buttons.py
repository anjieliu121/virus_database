import streamlit as st

def display_download_button(file_name, date=None):
    # st.markdown(download_button_css, unsafe_allow_html=True)

    columns = st.columns([1,1,1,1,1])
    with columns[0]:
        with open(f"data/{file_name}") as f:
            st.download_button(
                label="Download Full Data",
                data=f,
                file_name=file_name,
                mime="text/csv",
            )
    with columns[1]:
        if date:
            st.caption(f"Last Update:  \n %s" % date)