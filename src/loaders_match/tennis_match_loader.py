from match import Match
from sport import Sport
import pandas as pd

class TennisMatchLoaderFemme:
    def __init__(self, chemin):
        self.chemin = chemin

    def load_all_match(self):
        res = []
        # On utilise la variable self.chemin ici
        df_tennis_femme = pd.read_csv(self.chemin)
        
        for i in range(len(df_tennis_femme)):
            match = Match(None, "tennis",  [], [])
            match.id = f"F{i + 1}"
            # 2. Correction de la syntaxe Pandas avec .loc
            match.list_home_player = [df_tennis_femme.loc[i, "winner_id"]]
            match.list_away_player = [df_tennis_femme.loc[i, "loser_id"]]
            res.append(match)
        return res

class TennisMatchLoaderHomme:
    # 1. Pareil ici, on accepte le chemin
    def __init__(self, chemin):
        self.chemin = chemin

    def load_all_match(self):
        res = []
        df_tennis_homme = pd.read_csv(self.chemin)
        
        for i in range(len(df_tennis_homme)):
            match = Match(None, "tennis", [], [])
            match.id = f"H{i + 1}"
            # 2. Correction de la syntaxe Pandas avec .loc
            match.list_home_player = [df_tennis_homme.loc[i, "winner_id"]]
            match.list_away_player = [df_tennis_homme.loc[i, "loser_id"]]
            res.append(match)
        return res

class TennisMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        chemin_wta = "data/tennis_tdd/wta_matches_2024.csv"
        chemin_atp = "data/tennis_tdd/atp_matches_2024.csv"

        loader_femme = TennisMatchLoaderFemme(chemin_wta)
        # 3. Correction du nom de la méthode (sans 's' à la fin)
        liste_matchs_femmes = loader_femme.load_all_match()

        loader_homme = TennisMatchLoaderHomme(chemin_atp)
        liste_matchs_hommes = loader_homme.load_all_match()

        matchs = liste_matchs_femmes + liste_matchs_hommes
        
        return matchs