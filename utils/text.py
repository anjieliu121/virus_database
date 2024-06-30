import streamlit as st


def explain_graph(txt):
    st.markdown(f'<p style="background-color:#ffd600;color:#333f48;padding: 10px;border-radius: 8px;">{txt}</p>',
                unsafe_allow_html=True)


def data_contributor(names):
    st.markdown("## Thank you!")
    st.markdown("Thank you for sharing this dataset to Meyers Database!")
    txt = f"{', '.join(names)}"
    st.markdown(f'<p style="background-color:#ffd600;color:#333f48;padding: 10px;border-radius: 8px;">{txt}</p>',
                unsafe_allow_html=True)
    st.markdown("AND Thank you _everyone_ for learning something from the data!")
    st.markdown("Yours sincerely,")
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown(
            """
            <a href="https://meyers-database.streamlit.app">
                <img src="https://github.com/anjieliu121/virus_database/blob/main/images/database_logo.png?raw=true" alt="Meyers Lab">
            </a>
            """,
            unsafe_allow_html=True
        )
