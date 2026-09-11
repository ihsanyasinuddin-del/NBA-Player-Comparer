import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats
import plotly.express as px
import plotly.graph_objects as go


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

season = st.session_state["the_season"]
df = leaguedashplayerstats.LeagueDashPlayerStats(
    season=season,
    per_mode_detailed="PerGame"
    ).get_data_frames()[0]

def find_percentile(id, desired_stat):
    qualifier = df["GP"] * df["MIN"]
    qualified_df = df[qualifier > 1500]
    length = len(qualified_df)
    n = 0 
    points1 = qualified_df.query(f"PLAYER_ID == {id}")[f"{desired_stat}"].iloc[0]
    for x in qualified_df[f"{desired_stat}"]:
        if x < points1:
            n += 1
    percentile = (n / length) * 100
    return percentile

if st.session_state.get("player_one_id"):
    player_one_id = st.session_state.get("player_one_id")
    if st.session_state.get("player_two_id"):
        name_one = st.session_state.get("chosen_name")
        name_two = st.session_state.get("chosen_name2")
        player_two_id = st.session_state.get("player_two_id")
        season = st.session_state["the_season"]
        left, right = st.columns([0.5, 0.5])
        with left:
            make_line_graph(player_one_id, player_two_id, desired_stat="PTS", title="Points Per Game")
            make_line_graph(player_one_id, player_two_id, desired_stat="AST", title="Assists")
            make_line_graph(player_one_id, player_two_id, desired_stat="FG_PCT", title="Field Goal Percentage")
            make_line_graph(player_one_id, player_two_id, desired_stat="FG3_PCT", title="Three-point percentage")
            make_line_graph(player_one_id, player_two_id, desired_stat="REB", title="Rebounds")
        with right:
            points_percentile_one = find_percentile(player_one_id, "PTS")
            ast_percentile_one = find_percentile(player_one_id, "AST")
            three_point_percentile_one = find_percentile(player_one_id, "FG3_PCT")
            rebounds_percentile_one = find_percentile(player_one_id, "REB")
            steal_percentile_one = find_percentile(player_one_id, "STL")
            blocks_percentile_one = find_percentile(player_one_id, "BLK")

            points_percentile_two = find_percentile(player_two_id, "PTS")
            ast_percentile_two = find_percentile(player_two_id, "AST")
            three_point_percentile_two = find_percentile(player_two_id, "FG3_PCT")
            rebounds_percentile_two = find_percentile(player_two_id, "REB")
            steal_percentile_two = find_percentile(player_two_id, "STL")
            blocks_percentile_two = find_percentile(player_two_id, "BLK")


            categories = ["points", "assists", "3pt%", "rebounds", "steals", "blocks"]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[
                    points_percentile_one,
                    ast_percentile_one,
                    three_point_percentile_one,
                    rebounds_percentile_one,
                    steal_percentile_one,
                    blocks_percentile_one



                ],
                fill="toself",
                name=f"{name_one}"

                ))  
            fig.add_trace(go.Scatterpolar(
                    r=[
                        points_percentile_two,
                        ast_percentile_two,
                        three_point_percentile_two,
                        rebounds_percentile_two,
                        steal_percentile_two,
                        blocks_percentile_two

                    ],
                    fill="toself",
                    name=f"{name_two}"      


                        ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0,100],
                        tickvals=[20,40,60,80,100]
                    )
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("Input two players on the homepage to see more stats!")
else:
    st.write("Input two players on the homepage to see more stats!")

