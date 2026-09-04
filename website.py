import streamlit as st 
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def get_player(players_name):
    name = players.find_players_by_full_name(players_name)
    if not name:
        return 
    player_id = name[0]["id"]
    full_name = name[0]["full_name"]
    return player_id, full_name 

def get_stats(player_id,season):
    output = playercareerstats.PlayerCareerStats(
        per_mode36="PerGame",
        player_id=player_id 
        )
    player_data = (output.season_totals_regular_season.get_data_frame())
    season_data = (player_data[player_data["SEASON_ID"] == season])
    if season_data.empty:
        return 
    season_row = season_data.iloc[0]
    stats = {
        "Points": season_row["PTS"],
        "Three-point percentage": f"{season_row['FG3_PCT'] * 100:.1f}%",
        "Field goal percentage": f"{season_row["FG_PCT"] * 100:.1f}%",
        "Free-throw percentage": f"{season_row["FT_PCT"] * 100:.1f}%",
        "Rebounds": season_row["REB"],
        "Assists": season_row["AST"],
        "Steals": season_row["STL"],
        "Blocks": season_row["BLK"],
        "Turnovers":  season_row["TOV"],

    }
    return stats 





st.markdown("# NBA COMPARER :basketball:", text_alignment="center")


#Get a list of all seasons
output = playercareerstats.PlayerCareerStats(
        per_mode36="PerGame",
        player_id=201939 
        )

df = output.season_totals_regular_season.get_data_frame()
seasons = df["SEASON_ID"].tolist()

selected_season = st.selectbox(f"Select the desired season:", 
options=seasons,
index=None
)


player_one = st.text_input("Enter player one ")
player_one_id, player_one_name = get_player(player_one)
player_one_stats = get_stats(player_id=player_one_id, season=selected_season)

player_two = st.text_input("Enter player two ")
player_two_id, player_two_name = get_player(player_two)
player_two_stats = get_stats(player_id=player_two_id, season=selected_season)

col1, col2 = st.columns(2, border=True)

compare = st.button("COMPARE", icon="⚖️", width="stretch")


def display_stats_and_compare(playeronestats, playertwostats, name1, name2,):
    with col1:
        st.markdown(f"## {name1}", text_alignment="center")
    with col2:
        st.markdown(f"## {name2}", text_alignment="center")
    for stat in playeronestats:
        if stat == "Turnovers":
            if playeronestats[stat] > playertwostats[stat]:
                with col1:
                    st.metric(f"{stat}", f"{playeronestats[stat]}")
                with col2:
                    st.metric(f"{stat} 🏆", f"{playertwostats[stat]}")
            elif playertwostats[stat] > playeronestats[stat]:
                with col1:
                    st.metric(f"{stat} 🏆", f"{playeronestats[stat]}")
                with col2:
                    st.metric(f"{stat}", f"{playertwostats[stat]}")
            else:
                with col1:
                    st.metric(f"{stat}:", f"{playeronestats[stat]}")
                with col2:
                    st.metric(f"{stat}:", f"{playertwostats[stat]}")
        else:
            if playeronestats[stat] > playertwostats[stat]:
                with col1:
                    st.metric(f"{stat} 🏆", f"{playeronestats[stat]}")
                with col2:
                    st.metric(f"{stat}", playertwostats[stat])
            elif playertwostats[stat] > playeronestats[stat]:
                with col1:
                    st.metric(f"{stat}", playeronestats[stat])
                with col2:
                    st.metric(f"{stat} 🏆", f"{playertwostats[stat]}")
            else:
                with col1:
                    st.metric(f"{stat}", playeronestats[stat])
                with col2:
                    st.metric(f"{stat}", playertwostats[stat])   

if player_two_stats is not None:
    if compare: 
        display_stats_and_compare(player_one_stats, player_two_stats, player_one_name, player_two_name)


