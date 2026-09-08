import streamlit as st

start_page = st.Page(
    page="pages/website.py",
    title="NBA Comparer Homepage",
    icon="🏀",
    default=True,
)

more_stats = st.Page(
    page="pages/more_stats.py",
    title="More Stats",
    icon="📊",

)

pg = st.navigation(pages=[start_page, more_stats])
st.sidebar.markdown("##### Data from [nba.com](https://www.nba.com/), using [nba_api](https://github.com/swar/nba_api)")
pg.run()