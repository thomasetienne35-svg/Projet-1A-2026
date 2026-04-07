from match import Match
from sport import Sport

import pandas as pd

class TennisMatchLoaderFemme:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_tennis_femme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/tennis_tdd/wta_matches_2024.csv"
        )
        for i in range(len(df_tennis_femme)):
            
            match = Match(None, Tennis : Sport, None, None)
            match.id = f"F{i+1}"
            match.list_home_player = df_tennis_femme[i, "winner_id"]
            match.list_away_player = df_tennis_femme[i, "loser_id"]
            res.append(match)
        return res



class TennisMatchLoaderHomme:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_tennis_homme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/tennis_tdd/atp_matches_2024.csv"
        )
        for i in range(len(df_tennis_homme)):
            
            match = Match(None, Tennis : Sport, None, None)
            match.id = f"H{i+1}"
            match.list_home_player = df_tennis_homme[i, "winner_id"]
            match.list_away_player = df_tennis_homme[i, "loser_id"]
            res.append(match)
        return res

class TennisMatchLoader:
    
    def __init__(self):
        pass
    
    def load_all_match(self):

        chemin_wta = "/home/onyxia/work/Projet-1A-2026/data/tennis_tdd/wta_matches_2024.csv"
        chemin_atp = "/home/onyxia/work/Projet-1A-2026/data/tennis_tdd/atp_matches_2024.csv"

        loader_femme = TennisMatchLoaderFemme(chemin_wta)
        liste_matchs_femmes = loader_femme.load_all_matches()

        loader_homme = TennisMatchLoaderHomme(chemin_atp)
        liste_matchs_hommes = loader_homme.load_all_matches()

        matchs = liste_matchs_femmes + liste_matchs_hommes

