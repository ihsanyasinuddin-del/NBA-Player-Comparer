import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout="wide")

def request_stats(id):
    career = playercareerstats.PlayerCareerStats(player_id=id, per_mode36="PerGame")
    return career 


def make_line_graph(career1, career2, desired_stat, title):
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

if st.session_state.get("the_season"): 
    season = st.session_state["the_season"]
    df = leaguedashplayerstats.LeagueDashPlayerStats(
    season=season,
    per_mode_detailed="PerGame"
    ).get_data_frames()[0]

def find_percentile(id, desired_stat, name):
    qualifier = df["GP"] * df["MIN"]
    qualified_df = df[qualifier > 1500]
    length = len(qualified_df)
    n = 0 
    points1 = qualified_df.query(f"PLAYER_ID == {id}")[f"{desired_stat}"]
    if points1.empty:
            st.write(f"{name} has not played enough minutes to be displayed on the radar chart.")
            worked = False
            return worked
    points = points1.iloc[0]
    for x in qualified_df[f"{desired_stat}"]:
        if x < points:
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
            career1 = request_stats(player_one_id)
            career2 = request_stats(player_two_id)
            make_line_graph(career1, career2, desired_stat="PTS", title="Points Per Game")
            make_line_graph(career1, career2, desired_stat="AST", title="Assists")
            make_line_graph(career1, career2, desired_stat="FG_PCT", title="Field Goal Percentage")
            make_line_graph(career1, career2, desired_stat="FG3_PCT", title="Three-point percentage")
            make_line_graph(career1, career2, desired_stat="REB", title="Rebounds")
        with right:
            points_percentile_one = find_percentile(player_one_id, "PTS", name_one)
            if not points_percentile_one:
                one_check = False
            else:
                ast_percentile_one = find_percentile(player_one_id, "AST", name_one)
                three_point_percentile_one = find_percentile(player_one_id, "FG3_PCT", name_one)
                rebounds_percentile_one = find_percentile(player_one_id, "REB", name_one)
                steal_percentile_one = find_percentile(player_one_id, "STL", name_one)
                blocks_percentile_one = find_percentile(player_one_id, "BLK", name_one)
                one_check = True 

            points_percentile_two = find_percentile(player_two_id, "PTS", name_two)
            if not points_percentile_two:
                two_check = False
            else:
                ast_percentile_two = find_percentile(player_two_id, "AST", name_two)
                three_point_percentile_two = find_percentile(player_two_id, "FG3_PCT", name_two)
                rebounds_percentile_two = find_percentile(player_two_id, "REB", name_two)
                steal_percentile_two = find_percentile(player_two_id, "STL", name_two)
                blocks_percentile_two = find_percentile(player_two_id, "BLK", name_two)
                two_check = True 

            st.markdown("#### Radar Chart Player Comparison", text_alignment="center")
            categories = ["Scoring", "Playmaking", "Shooting", "Rebounds", "Steals", "Rim Protection"]
            fig = go.Figure()
            if one_check:
                fig.add_trace(go.Scatterpolar(
                    r=[
                        points_percentile_one,
                        ast_percentile_one,
                        three_point_percentile_one,
                        rebounds_percentile_one,
                        steal_percentile_one,
                        blocks_percentile_one

                    ],
                    theta=categories,
                    name=f"{name_one}",
                    fill="toself",


                    ))  
            if two_check:
                fig.add_trace(go.Scatterpolar(
                    r=[
                        points_percentile_two,
                        ast_percentile_two,
                        three_point_percentile_two,
                        rebounds_percentile_two,
                        steal_percentile_two,
                        blocks_percentile_two

                        ],
                        theta=categories,
                        name=f"{name_two}",
                        fill="toself",
                        
                              


                    ))
            fig.update_layout(
                template="plotly_dark",
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0,100],
                        tickvals=[20,40,60,80,100],
                        
                    )
                )
            )
            st.plotly_chart(fig, use_container_width=True, )

    else:
        st.write("Input two players on the homepage to see more stats!")
else:
    st.write("Input two players on the homepage to see more stats!")

