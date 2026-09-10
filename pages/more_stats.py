import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import playercareerstats

st.set_page_config(layout="wide")

def make_line_graph(id1, id2, desired_stat, title):
    career1 = playercareerstats.PlayerCareerStats(player_id=id1, per_mode36="PerGame")
    career2 = playercareerstats.PlayerCareerStats(player_id=id2, per_mode36="PerGame")
    df1 = career1.season_totals_regular_season.get_data_frame()
    df2 = career2.season_totals_regular_season.get_data_frame()
    points1 = df1[[f"{desired_stat}", "SEASON_ID"]]
    points2 = df2[[f"{desired_stat}", "SEASON_ID"]]
    if desired_stat in ["FG_PCT", "FG3_PCT"]:
        points1[f"{desired_stat}"] = points1[f"{desired_stat}"] * 100
        points2[f"{desired_stat}"] = points2[f"{desired_stat}"] * 100
    combined_points = pd.merge(points1, points2, on="SEASON_ID")
    combined_points = combined_points.rename(columns={f"{desired_stat}_x" : f"{name_one}", f"{desired_stat}_y" : f"{name_two}"})
    st.markdown(f"### {title}" , text_alignment="center" )
    st.line_chart(data=combined_points, x="SEASON_ID", y=[f"{name_one}", f"{name_two}"], x_label="Season", y_label=f"{title}", color=["red", "green"])

if st.session_state.get("player_one_id"):
    player_one_id = st.session_state.get("player_one_id")
    if st.session_state.get("player_two_id"):
        name_one = st.session_state.get("chosen_name")
        name_two = st.session_state.get("chosen_name2")
        player_two_id = st.session_state.get("player_two_id")
        left, right = st.columns([0.5, 0.5])
        with left:
            make_line_graph(player_one_id, player_two_id, desired_stat="PTS", title="Points Per Game")
            make_line_graph(player_one_id, player_two_id, desired_stat="AST", title="Assists")
            make_line_graph(player_one_id, player_two_id, desired_stat="FG_PCT", title="Field Goal Percentage")
            make_line_graph(player_one_id, player_two_id, desired_stat="FG3_PCT", title="Three-point percentage")
            make_line_graph(player_one_id, player_two_id, desired_stat="REB", title="Rebounds")
    else:
        st.write("Input two players on the homepage to see more stats!")
else:
    st.write("Input two players on the homepage to see more stats!")

