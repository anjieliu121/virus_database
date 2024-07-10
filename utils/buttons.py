import streamlit as st

from utils.data_io import get_file_size, convert_df, get_df_size


def download_full_data(file_path, file_name, date, source):
    if file_name == "":
        st.caption("Source:  [link](%s)" % source)
        st.caption("Visualization will be added soon.")
    else:
        columns = st.columns([0.3, 0.2, 0.2, 0.3])
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
        with columns[3]:
            st.caption("File Size:  \n %s" % get_file_size(file_path))


def download_full_data_gcp(df, file_name, date, source):
    csv = convert_df(df)
    columns = st.columns([0.3, 0.2, 0.2, 0.3])
    with columns[0]:
        st.download_button(
            label="Download Full Data",
            data=csv,
            file_name=file_name,
            mime="text/csv",
        )
    with columns[1]:
        st.caption(f"Latest Update:  \n %s" % date)
    with columns[2]:
        st.caption("Data Source:  \n [link](%s)" % source)
    with columns[3]:
        st.caption("Data Size:  \n %s" % get_df_size(df))


def single_select(caption, options, default=0, key=None):
    if isinstance(default, str):
        default = options.index(default)
    box = st.selectbox(caption, options, index=default, key=key)
    return box


def multi_select(caption, options, *default, key=None):
    if len(default) == 1:
        if isinstance(default[0], list):
            default = default[0]
    default_new = []
    for i in default:
        if isinstance(i, int):
            i = options[i]
        default_new.append(i)
    if len(default_new) > 0:
        box = st.multiselect(caption, options, default=list(default_new), key=key)
    else:
        box = st.multiselect(caption, options, default=None, key=key)
    return box

