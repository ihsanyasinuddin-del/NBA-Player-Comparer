import pytest 
from project import get_player
from project import get_stats
from project import display_stats

def test_get_player():
    assert get_player("Stephen Curry") == (201939, "Stephen Curry")


def test_get_stats():
    stats = get_stats(player_id=201939, season="2015-16")
    assert stats["PTS"] == 30.1

def test_display_stats(capsys):
    p1_stats = {
        "PTS": 30.1,
        "FG": 50.4,
        "FT": 90.8,
        "3PT": 45.4,
        "REB": 5.4,
        "AST": 6.7,
        "STL": 2.1,
        "BLK": 0.2,
        "TOV": 3.3
    }

    display_stats(full_name="Stephen Curry", stats=p1_stats, season="2015-16")
    captured = capsys.readouterr()
    assert "Stephen Curry" in captured.out
    assert "30.1 PPG" in captured.out 
