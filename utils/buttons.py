import streamlit as st


def download_full_data(file_path, file_name, date, source, source_only=False):
    if source_only:
        st.caption("Source:  [link](%s)" % source)
        st.caption("Visualization will be added soon.")
    else:
        columns = st.columns([0.2, 0.2, 0.2, 0.4])
        with columns[0]:
            with open(file_path) as f:
                st.download_button(
                    label="Download Full Data",
                    data=f,
                    file_name=file_name,
                    mime="text/csv",
                )
        with columns[1]:
            st.caption(f"Latest Update:  \n %s" % date)
        with columns[2]:
            st.caption("Data Source:  \n [link](%s)" % source)


def single_select(caption, options, default=0, key=None):
    box = st.selectbox(caption, options, index=default, key=key)
    return box


def multi_select(caption, options, *default):
    if len(default) > 0:
        box = st.multiselect(caption, options, default=list(default))
    else:
        box = st.multiselect(caption, options, default=None)
    return box

