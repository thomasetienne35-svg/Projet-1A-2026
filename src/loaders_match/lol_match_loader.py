from match import Match
from sport import Sport
import pandas as pd

pd.options.display.max_columns = 100

class LolMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_lol_match = pd.read_csv("data/league_of_legends_tdd/match.csv")
        df_lol_team = pd.read_csv("data/league_of_legends_tdd/team.csv")
        df_lol_player = pd.read_csv("data/league_of_legends_tdd/player.csv")
        
        for i in range(len(df_lol_match)):
            match = Match(None, "lol", None, None)
            match.id = i + 2
            
            abbr_blue = df_lol_match.loc[i, "team_blue"]
            abbr_red = df_lol_match.loc[i, "team_red"]

            # =========================================================
            # SAUVEGARDE DES STATS (On garde les données brutes : ex. "VIT")
            # =========================================================
            match.team_blue = str(abbr_blue).strip()
            match.team_red = str(abbr_red).strip()
            match.winner = str(df_lol_match.loc[i, "winner"]).strip()
            match.date = df_lol_match.loc[i, "date"]  # Utilisé pour filtrer par date
            match.patch = df_lol_match.loc[i, "patch"] # Au cas où on veut filtrer par patch

            match.kills_team_blue = df_lol_match.loc[i, "kills_team_blue"]
            match.deaths_team_blue = df_lol_match.loc[i, "deaths_team_blue"]
            match.assists_team_blue = df_lol_match.loc[i, "assists_team_blue"]

            match.kills_team_red = df_lol_match.loc[i, "kills_team_red"]
            match.deaths_team_red = df_lol_match.loc[i, "deaths_team_red"]
            match.assists_team_red = df_lol_match.loc[i, "assists_team_red"]
            # =========================================================

            # --- Récupération des joueurs (Blue Team) ---
            equipe_filtree_blue = df_lol_team[df_lol_team["team_abbreviation"] == abbr_blue]
            if not equipe_filtree_blue.empty:
                nom_complet_team = equipe_filtree_blue.iloc[0]["team"]
                liste_noms_joueurs_home = df_lol_player[df_lol_player["team"] == nom_complet_team]["name"].tolist()
                match.list_home_player = liste_noms_joueurs_home
            else:
                match.list_home_player = []

            # --- Récupération des joueurs (Red Team) ---
            equipe_filtree_red = df_lol_team[df_lol_team["team_abbreviation"] == abbr_red]
            if not equipe_filtree_red.empty:
                nom_complet_team = equipe_filtree_red.iloc[0]["team"]
                liste_noms_joueurs_away = df_lol_player[df_lol_player["team"] == nom_complet_team]["name"].tolist()
                match.list_away_player = liste_noms_joueurs_away
            else:
                match.list_away_player = []

            res.append(match)
            
        return res