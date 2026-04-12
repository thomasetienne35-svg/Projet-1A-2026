from match import Match
import pandas as pd

pd.options.display.max_columns = 100


class FootballMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_football = pd.read_csv(
            r"D:\Projet-1A-2026\data\football_european_leagues_tdd\match.csv"
        )  # Il faut trouver une solution pour cette ligne car l'emplacement de notre fichier de donnée va changer en
        # en fonction de là où on clone le repo
        for i in range(len(df_football)):
            match = Match(None, "football", None, None)
            match.id = df_football.loc[i, "id"]
            colonnes_home = ["home_team_goal"] + [
                f"home_player_{i}" for i in range(1, 12)
            ]
            match.list_home_player = df_football.loc[i, colonnes_home].tolist()
            colonnes_away = ["away_team_goal"] + [
                f"away_player_{i}" for i in range(1, 12)
            ]
            match.list_away_player = df_football.loc[i, colonnes_away].tolist()
            res.append(match)
        return res
