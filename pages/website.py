import streamlit as st 
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo

st.set_page_config(layout="centered")

@st.cache_data
def get_player(players_name):
    name = players.find_players_by_full_name(players_name)
    if not name:
        return 
    player_id = name[0]["id"]
    full_name = name[0]["full_name"]
    return player_id, full_name 

@st.cache_data
def get_basic_info(playerid):
    info = commonplayerinfo.CommonPlayerInfo(player_id=playerid)
    df = info.common_player_info.get_data_frame()
    height = df["HEIGHT"].iloc[0]
    team = df["TEAM_NAME"].iloc[0]
    position = df["POSITION"].iloc[0]
    return height, team, position

@st.cache_data
def find_previous_year(current_year):
    one, two = current_year.split("-")
    onenew = int(one) - 1
    twonew = int(two) - 1
    previous_year = (f"{onenew}-{twonew}")
    return previous_year

@st.cache_data
def get_stats(player_id,season):
    output = playercareerstats.PlayerCareerStats(
        per_mode36="PerGame",
        player_id=player_id 
        )
    player_data = (output.season_totals_regular_season.get_data_frame())
    season_data = (player_data[player_data["SEASON_ID"] == season])
    if season_data.empty:
        return None, None
    season_row = season_data.iloc[0]
    stats = {
        "Points": season_row["PTS"],
        "Three-point percentage": season_row['FG3_PCT'] * 100,
        "Field goal percentage": season_row["FG_PCT"] * 100,
        "Free-throw percentage": season_row["FT_PCT"] * 100,
        "Rebounds": season_row["REB"],
        "Assists": season_row["AST"],
        "Steals": season_row["STL"],
        "Blocks": season_row["BLK"],
        "Turnovers":  season_row["TOV"],

    }
    previous_season = find_previous_year(season)
    previous_output = output
    previous_player_data = (previous_output.season_totals_regular_season.get_data_frame())
    previous_season_data = (previous_player_data[previous_player_data["SEASON_ID"] == previous_season])
    if previous_season_data.empty:
        return None, None
    previous_season_row = previous_season_data.iloc[0]
    previous_stats = {
            "Points": previous_season_row["PTS"],
            "Three-point percentage": previous_season_row['FG3_PCT'] * 100,
            "Field goal percentage": previous_season_row["FG_PCT"] * 100,
            "Free-throw percentage": previous_season_row["FT_PCT"] * 100,
            "Rebounds": previous_season_row["REB"],
            "Assists": previous_season_row["AST"],
            "Steals": previous_season_row["STL"],
            "Blocks": previous_season_row["BLK"],
            "Turnovers":  previous_season_row["TOV"],
    
    }
    return stats, previous_stats 

def score(score_one, score_two, name1, name2):
    left, mid, right = st.columns([2, 1, 2])
    with left:
        if score_one > score_two:
            st.markdown(f"### {name1} 👑", text_alignment="center")
        else:
            st.markdown(f"### {name1}", text_alignment="center")
        st.markdown(f"# {score_one}", text_alignment="center")

    with mid:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("# --", text_alignment="center")

    with right:
        if score_two > score_one:
            st.markdown(f"### {name2} 👑", text_alignment="center")
        else:
            st.markdown(f"### {name2}", text_alignment="center")
        st.markdown(f"# {score_two}", text_alignment="center")


def display_stats_and_compare(playeronestats, playeroneprevious, playertwostats, playertwoprevious, name1, name2, id1, id2):
    player_one_count = 0
    player_two_count = 0 
    height1, team1, position1 = get_basic_info(id1)
    height2, team2, position2 = get_basic_info(id2)
    with col1:
        st.markdown(f"## {name1}", text_alignment="center")
        st.markdown(f"###### Current team: {team1} | Height: {height1} | Position: {position1}", text_alignment="center")
    with col2:
        st.markdown(f"## {name2}", text_alignment="center")
        st.markdown(f"###### Current team: {team2} | Height: {height2} | Position: {position2}", text_alignment="center")


    for stat in playeronestats:
        if stat in ["Three-point percentage", "Field goal percentage", "Free-throw percentage"]:
            playeronestat = f"{playeronestats[stat]:.1f}%"
            playertwostat = f"{playertwostats[stat]:.1f}%"
        else:
            playeronestat = f"{playeronestats[stat]:.1f}"
            playertwostat = f"{playertwostats[stat]:.1f}"

        # separate logic for turnovers as higher number is worse 
        if stat == "Turnovers":
            if playeronestats[stat] > playertwostats[stat]:
                player_two_count += 1
                with col1:
                    st.metric(f"{stat}", f"{playeronestat}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}", delta_color="inverse")
                with col2:
                    st.metric(f"{stat} 🏆", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}", delta_color="inverse")

            elif playertwostats[stat] > playeronestats[stat]:
                player_one_count += 1
                with col1:
                    st.metric(f"{stat} 🏆", f"{playeronestats[stat]}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}", delta_color="inverse")
                with col2:
                    st.metric(f"{stat}", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}", delta_color="inverse")

            else:
                with col1:
                    st.metric(f"{stat} 🟰", f"{playeronestat}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}", delta_color="inverse")
                with col2:
                    st.metric(f"{stat} 🟰", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}", delta_color="inverse")

        else:
            if playeronestats[stat] > playertwostats[stat]:
                player_one_count += 1
                with col1:
                    st.metric(f"{stat} 🏆", f"{playeronestat}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}")
                with col2:
                    st.metric(f"{stat}", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}")
            elif playertwostats[stat] > playeronestats[stat]:
                player_two_count += 1
                with col1:
                    st.metric(f"{stat}", f"{playeronestat}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}")
                with col2:
                    st.metric(f"{stat} 🏆", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}")
            else:
                with col1:
                    st.metric(f"{stat} 🟰", f"{playeronestat}", delta=f"{(playeronestats[stat] - playeroneprevious[stat]):.1f}")
                with col2:
                    st.metric(f"{stat} 🟰", f"{playertwostat}", delta=f"{(playertwostats[stat] - playertwoprevious[stat]):.1f}")
    score(player_one_count, player_two_count, name1, name2)


def check_same(player_one, player_two):
    if player_one == player_two:
        st.error(f"Please enter two different players", icon="🪞")
        return True  

def reset_inputs():
    st.session_state["season"] = None
    st.session_state["player_one"] = ""
    st.session_state["player_two"] = ""
    st.session_state["player_one_id"] = None
    st.session_state["player_two_id"] = None
    st.session_state["comparison_done"] = False

st.markdown("# NBA COMPARER :basketball:", text_alignment="center")
st.markdown("##### Compare two NBA players across a season of your choosing.", text_alignment="center")

@st.cache_data
def get_seasons_list():
    output = playercareerstats.PlayerCareerStats(
            per_mode36="PerGame",
            player_id=2544 
            )
    df = output.season_totals_regular_season.get_data_frame()
    seasons = df["SEASON_ID"].tolist()
    return seasons

if "season" not in st.session_state:
    st.session_state["season"] = st.session_state.get("the_season", "")
selected_season = st.selectbox(f"Select the desired season:", 
options=get_seasons_list(),
index=None,
key="season",
placeholder=st.session_state["season"]
)

# have to store in separate variable due to streamlit erasing key for widgets when on a new page
st.session_state["the_season"] = selected_season

left, right = st.columns(2)
with left:
    if "player_one" not in st.session_state:
        st.session_state["player_one"] = st.session_state.get("chosen_name", "")
    player_one = st.text_input("Enter player one ", key="player_one").strip()

st.session_state["chosen_name"] = player_one

with right:
    if "player_two" not in st.session_state:
        st.session_state["player_two"] = st.session_state.get("chosen_name2", "")
    player_two = st.text_input("Enter player two ", key="player_two").strip()

st.session_state["chosen_name2"] = player_two

compare = st.button("COMPARE", icon="⚖️", width="stretch")

if "comparison_done" not in st.session_state:
    st.session_state["comparison_done"] = False

if st.session_state.get("comparison_done"):
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.image(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{st.session_state["player_one_id"]}.png?imwidth=1040&imheight=760)")
    with col2:
        st.image(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{st.session_state["player_two_id"]}.png?imwidth=1040&imheight=760)")
    display_stats_and_compare(
        st.session_state["player_one_stats"],
        st.session_state["player_one_previous"],
        st.session_state["player_two_stats"],
        st.session_state["player_two_previous"],
        st.session_state["chosen_name"],
        st.session_state["chosen_name2"],
        st.session_state["player_one_id"],
        st.session_state["player_two_id"],
    )

if not st.session_state["comparison_done"]:
    if compare: 
        first_package = get_player(player_one)
        if first_package is None:
            st.error(f"No results for {player_one} found", icon="❌", )
        else:
            player_one_id, player_one_name = first_package
            st.session_state["player_one_id"] = player_one_id
            player_one_stats, player_one_previous_stats = get_stats(player_id=player_one_id, season=selected_season)
            st.session_state["player_one_stats"] = player_one_stats
            st.session_state["player_one_previous"] = player_one_previous_stats
            if player_one_stats is None:
                if selected_season is None:
                    st.error("Please enter a season!", icon="❌")
                else:
                    st.error(f"{player_one} did not play in that season!", icon="⏳")
            else:
                second_package = get_player(player_two)
                if second_package is None:
                    st.error(f"No results for {player_two} found", icon="❌")
                else:
                    player_two_id, player_two_name = second_package
                    st.session_state["player_two_id"] = player_two_id
                    player_two_stats, player_two_previous_stats = get_stats(player_id=player_two_id, season=selected_season)
                    st.session_state["player_two_stats"] = player_two_stats
                    st.session_state["player_two_previous"] = player_two_previous_stats
                    if player_two_stats is None:
                        if selected_season is None:
                            st.error("Please enter a season!", icon="❌")
                        else:
                            st.error(f"{player_two} did not play in that season!", icon="⏳")
                    else:
                        if not check_same(player_one_id, player_two_id): 
                            st.session_state["comparison_done"] = True 
                            col1, col2 = st.columns(2, border=True)
                            with col1:
                                st.image(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_one_id}.png?imwidth=1040&imheight=760)")
                            with col2:
                                st.image(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_two_id}.png?imwidth=1040&imheight=760)")
                            display_stats_and_compare(player_one_stats, 
                                                    player_one_previous_stats,
                                                    player_two_stats, 
                                                    player_two_previous_stats,
                                                    player_one_name, 
                                                    player_two_name, 
                                                    player_one_id, 
                                                    player_two_id,
                                                    )
                        
                    
left, middle, right = st.columns(3)
with middle:
    st.button("RESET", on_click=reset_inputs, icon="🔁", width="stretch")
