from match import Match
from sport import Sport
import pandas as pd

class TennisMatchLoaderFemme:
    def __init__(self, chemin_matchs, chemin_joueuses):
        self.chemin_matchs = chemin_matchs
        self.chemin_joueuses = chemin_joueuses

    def load_all_match(self):
        res = []
        df_matchs = pd.read_csv(self.chemin_matchs)
        df_joueuses = pd.read_csv(self.chemin_joueuses)
        
        # --- LE DICTIONNAIRE MAGIQUE (Femmes) ---
        # 1. On crée une colonne avec le nom complet
        df_joueuses["nom_complet"] = df_joueuses["name_first"].astype(str) + " " + df_joueuses["name_last"].astype(str)
        # 2. On crée le dictionnaire { ID : "Prenom Nom" }
        dict_joueuses = dict(zip(df_joueuses["player_id"], df_joueuses["nom_complet"]))
        
        for i in range(len(df_matchs)):
            match = Match(None, "tennis", [], [])
            match.id = f"F{i + 1}"
            
            id_gagnante = df_matchs.loc[i, "winner_id"]
            id_perdante = df_matchs.loc[i, "loser_id"]
            
            # 3. Traduction ! (Si l'ID n'est pas dans le dico, on garde l'ID par sécurité)
            nom_gagnante = dict_joueuses.get(id_gagnante, str(id_gagnante))
            nom_perdante = dict_joueuses.get(id_perdante, str(id_perdante))
            
            match.list_home_player = [nom_gagnante]
            match.list_away_player = [nom_perdante]
            res.append(match)
            
        return res

class TennisMatchLoaderHomme:
    def __init__(self, chemin_matchs, chemin_joueurs):
        self.chemin_matchs = chemin_matchs
        self.chemin_joueurs = chemin_joueurs

    def load_all_match(self):
        res = []
        df_matchs = pd.read_csv(self.chemin_matchs)
        df_joueurs = pd.read_csv(self.chemin_joueurs)
        
        # --- LE DICTIONNAIRE MAGIQUE (Hommes) ---
        df_joueurs["nom_complet"] = df_joueurs["name_first"].astype(str) + " " + df_joueurs["name_last"].astype(str)
        dict_joueurs = dict(zip(df_joueurs["player_id"], df_joueurs["nom_complet"]))
        
        for i in range(len(df_matchs)):
            match = Match(None, "tennis", [], [])
            match.id = f"H{i + 1}"
            
            id_gagnant = df_matchs.loc[i, "winner_id"]
            id_perdant = df_matchs.loc[i, "loser_id"]
            
            # Traduction !
            nom_gagnant = dict_joueurs.get(id_gagnant, str(id_gagnant))
            nom_perdant = dict_joueurs.get(id_perdant, str(id_perdant))
            
            match.list_home_player = [nom_gagnant]
            match.list_away_player = [nom_perdant]
            res.append(match)
            
        return res

class TennisMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        # Chemins vers les matchs
        chemin_matchs_wta = "data/tennis_tdd/wta_matches_2024.csv"
        chemin_matchs_atp = "data/tennis_tdd/atp_matches_2024.csv"
        
        # Chemins vers les joueurs (que tu avais dans ton PlayerLoader !)
        chemin_joueuses_wta = "data/tennis_tdd/wta_players_2024.csv"
        chemin_joueurs_atp = "data/tennis_tdd/atp_players_2024.csv"

        # On donne les deux chemins à nos chargeurs
        loader_femme = TennisMatchLoaderFemme(chemin_matchs_wta, chemin_joueuses_wta)
        liste_matchs_femmes = loader_femme.load_all_match()

        loader_homme = TennisMatchLoaderHomme(chemin_matchs_atp, chemin_joueurs_atp)
        liste_matchs_hommes = loader_homme.load_all_match()

        return liste_matchs_femmes + liste_matchs_hommes