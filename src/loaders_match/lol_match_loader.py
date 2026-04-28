from match import Match
from sport import Sport

import pandas as pd

pd.options.display.max_columns = 100


class LolMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_lol_match = pd.read_csv(
            "data/league_of_legends_tdd/match.csv"
        )
        df_lol_team = pd.read_csv(
            "data/league_of_legends_tdd/team.csv"
        )
        df_lol_player = pd.read_csv(
            "data/league_of_legends_tdd/player.csv"
        )
        for i in range(len(df_lol_match)):
            match = Match(None, "lol", None, None)
            match.id = i + 2
            abbr_blue = df_lol_match.loc[i, "team_blue"]
            abbr_red = df_lol_match.loc[i, "team_red"]
            equipe_filtree_blue = df_lol_team[df_lol_team["team_abbreviation"] == abbr_blue]
            equipe_filtree_red = df_lol_team[df_lol_team["team_abbreviation"] == abbr_red]
            if not equipe_filtree_blue.empty:
                nom_complet_team = equipe_filtree_blue.iloc[0]["team"]
                liste_noms_joueurs_home = df_lol_player[df_lol_player["team"] == nom_complet_team]["name"].tolist()
                match.list_home_player = liste_noms_joueurs_home
            else:
                match.list_home_player = []
            if not equipe_filtree_red.empty:
                nom_complet_team = equipe_filtree_red.iloc[0]["team"]
                liste_noms_joueurs_away = df_lol_player[df_lol_player["team"] == nom_complet_team]["name"].tolist()
                match.list_away_player = liste_noms_joueurs_away
            else:
                match.list_away_player = []
            res.append(match)
        return res