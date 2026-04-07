from match import Match
from sport import Sport

import pandas as pd

pd.options.display.max_columns = 100


class LolMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_lol = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/league_of_legends_tdd/match.csv"
        )
        for i in range(len(df_lol)):
            match = Match(None, Lol, None, None)
            match.id = df_lol.loc[i, "id"]
            colonnes_home = ["home_team_goal"] + [f"home_player_{i}" for i in range (1,12)]
            match.list_home_player = df.lol.loc[i, colonnes_home].tolist()
            colonnes_away = ["away_team_goal"] + [f"away_player_{i}" for i in range (1,12)]
            match.list_away_player = df_lol.loc[i,colonnes_away].tolist()
            res.append(match)
        return res