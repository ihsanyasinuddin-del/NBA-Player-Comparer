import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import playercareerstats

if st.session_state.get("player_one_id"):
    player_one_id = st.session_state.get("player_one_id")
    if st.session_state.get("player_two_id"):
        name_one = st.session_state.get("chosen_name")
        name_two = st.session_state.get("chosen_name2")
        player_two_id = st.session_state.get("player_two_id")
        career1 = playercareerstats.PlayerCareerStats(player_id=player_one_id, per_mode36="PerGame")
        career2 = playercareerstats.PlayerCareerStats(player_id=player_two_id, per_mode36="PerGame")
        df1 = career1.season_totals_regular_season.get_data_frame()
        df2 = career2.season_totals_regular_season.get_data_frame()
        points1 = df1[["PTS", "SEASON_ID"]]
        points2 = df2[["PTS", "SEASON_ID"]]
        combined_points = pd.merge(points1, points2, on="SEASON_ID")
        combined_points = combined_points.rename(columns={"PTS_x" : f"{name_one}", "PTS_y" : f"{name_two}"})
        st.line_chart(data=combined_points, x="SEASON_ID", y=[f"{name_one}", f"{name_two}"], x_label="Season", y_label="Points Per Game", color=["red", "green"])
        st.write(st.session_state)
    else:
        st.write("Input two players on the homepage to see more stats!")
else:
    st.write("Input two players on the homepage to see more stats!")

