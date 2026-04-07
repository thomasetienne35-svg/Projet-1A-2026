from match import Match
from sport import Sport

import pandas as pd

pd.options.display.max_columns = 100

# Ce qu'on veut mettre dans notre Player : Nom, nationalité, date_naissance, genre


class BasketballMatchLoader:
    def __init__():
        pass

    def load_all_match():
        res = []
        df_basketball = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/basketball/game.csv"
        )
        for i in range(len(df_basketball)):
            match = Match(None, Basketball, None, None)
            match.id = df_basketball.loc[i, "game_id"]
            colonnes_home = ["home_team_goal"] + [f"home_player_{i}" for i in range (1,12)]
            match.list_home_player = df.basketball.loc[i, colonnes_home].tolist()
            colonnes_away = ["away_team_goal"] + [f"away_player_{i}" for i in range (1,12)]
            match.list_away_player = df_basketball.loc[i,colonnes_away].tolist()
            res.append(match)
        return res