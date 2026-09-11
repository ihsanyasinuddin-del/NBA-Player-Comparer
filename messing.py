from nba_api.stats.endpoints import leaguedashplayerstats

def find_percentile(id, desired_stat):
    df = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2015-16",
    per_mode_detailed="PerGame"
    ).get_data_frames()[0]
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
print(find_percentile(201939, "REB"))