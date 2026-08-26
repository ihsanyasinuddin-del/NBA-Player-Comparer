from rich import print 
from rich.align import Align
from rich.panel import Panel
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

        
def main():
    season = input("Enter the season: ")
    while True: 
        p1_name = input("Enter player one: ")
        result = get_player(p1_name)
        if result is None:
            print("This player could not be found, please enter a valid name.")
            continue 
        p1_id, p1_full_name = result
        p1_stats = get_stats(player_id=p1_id, season=season)
        if p1_stats is None:
            print(f"{p1_full_name} did not play in that season.")
            continue 
        else:
            break 

    while True: 
        p2_name = input("Enter player two: ")
        result2 = get_player(p2_name)
        if result2 is None:
            print("This player could not be found, please enter a valid name.")
            continue 
        p2_id, p2_full_name = result2
        p2_stats = get_stats(player_id=p2_id, season=season)
        if p2_stats is None:
            print(f"{p2_full_name} did not play in that season.")
            continue 
        break

    print(
        Panel(
            Align.center("[red]NBA COMPARISON"), 
            expand = True))
    display_stats(p1_full_name, p1_stats, season)
    print("\n\nVS")
    display_stats(p2_full_name, p2_stats, season)
    comparison(p1_stats, p2_stats, p1_full_name, p2_full_name)


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
        "PTS": season_row["PTS"],
        "FG": season_row["FG_PCT"] * 100,
        "FT": season_row["FT_PCT"] * 100,
        "REB": season_row["REB"],
        "AST": season_row["AST"],
        "STL": season_row["STL"],
        "BLK": season_row["BLK"],
        "TOV":  season_row["TOV"],
        "3PT": season_row["FG3_PCT"] * 100,

    }
    return stats 


def display_stats(full_name, stats, season):
        print("\n")
        print(f"Player: {full_name} - Season: {season}")
        print("-----------------------------------------")
        print(f"{'Scoring:':<15} {stats['PTS']} PPG")
        print(f"{'FG:':<15} {stats['FG']:.1f}%")
        print(f"{'FT:':<15} {stats['FT']:.1f}%")
        print(f"{'3PT:':<15} {stats['3PT']:.1f}%")
        print(f"{'Rebounds:':<15} {stats['REB']} RPG")
        print(f"{'Playmaking:':<15} {stats['AST']} APG")
        print(f"{'Steals:':<15} {stats['STL']} SPG")
        print(f"{'Blocks:':<15} {stats['BLK']} BPG")
        print(f"{'Turnovers:':<15} {stats['TOV']}")



def comparison(p1_stats, p2_stats, name_one, name_two):
    comparison_dict = {
    "Scoring": [p1_stats["PTS"], p2_stats["PTS"]],
    "Assists": [p1_stats["AST"], p2_stats["AST"]],
    "FG": [p1_stats["FG"], p2_stats["FG"] ],
    "FT": [p1_stats["FT"], p2_stats["FT"]],
    "3PT": [p1_stats["3PT"], p2_stats["3PT"]],
    "Rebounds": [p1_stats["REB"], p2_stats["REB"]],
    "Steals": [p1_stats["STL"], p2_stats["STL"]],
    "Blocks": [p1_stats["BLK"], p2_stats["BLK"]],
    }
    print("\n\nCATEGORY WINNERS: ")
    for category in comparison_dict:
        stat_one = comparison_dict[category][0]
        stat_two = comparison_dict[category][1] 
        if stat_one > stat_two:
            print(f"{category + ':':<15}{name_one}")
        elif stat_two > stat_one:
            print(f"{category + ':':<15}{name_two}")
        else:
            print(f"{category + ':':<15}Tied")

    if p1_stats["TOV"] > p2_stats["TOV"]:
        print(f"{'Turnovers:':<15}{name_two}")
    elif p2_stats["TOV"] > p1_stats["TOV"]:
        print(f"{'Turnovers:':<15}{name_one}")
    else:
        print(f"{'Turnovers:':<15}Tied")

if __name__ == "__main__":
    main()
