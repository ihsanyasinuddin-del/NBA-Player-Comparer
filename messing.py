import streamlit as st
from streamlit_searchbox import st_searchbox


def search_wikipedia(searchterm: str) -> list:
    # search wikipedia for the searchterm
    return wikipedia.search(searchterm) if searchterm else []


# pass search function and other options as needed
selected_value = st_searchbox(
    search_wikipedia,
    placeholder="Search Wikipedia... ",
    key="my_key",
)

st.write(f"Selected value: {selected_value}")