from nba_api.stats.endpoints import leaguedashplayerstats
# get the mean ppg of every nba player in the league in that season 
df = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2024-25",
    per_mode_detailed="PerGame"
).get_data_frames()[0]

dfpoints = df["PTS"]

print(dfpoints.mean())