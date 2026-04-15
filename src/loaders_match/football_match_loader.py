from match import Match
import pandas as pd
from pathlib import Path

pd.options.display.max_columns = 100

class FootballMatchLoader:
    def __init__(self):
        # 1. On charge les DataFrames UNE SEULE FOIS lors de l'instanciation de la classe
        chemin_data = Path(__file__).parents[2] / "data" / "football_european_leagues_tdd"
        
        self.df_football = pd.read_csv(chemin_data / "match.csv")
        df_joueur = pd.read_csv(chemin_data / "player.csv")
        
        # On passe l'ID du match en index pour que la recherche d'un match précis soit instantanée
        self.df_football.set_index("id", inplace=True)
        
        # 2. OPTIMISATION MAJEURE : On transforme le dataframe des joueurs en dictionnaire
        # Format : {id_joueur: "nom_du_joueur"}
        # Cela permet de trouver un nom instantanément au lieu de parcourir le tableau 22 fois par match
        self.dict_joueurs = df_joueur.set_index("player_api_id")["player_name"].to_dict()

    def get_match(self, match_id):
        """
        Charge et retourne un objet Match spécifique à partir de son ID.
        """
        # On vérifie si le match existe dans nos données
        if match_id not in self.df_football.index:
            print(f"Match {match_id} introuvable.")
            return None

        # On isole uniquement la ligne du match qui nous intéresse
        row = self.df_football.loc[match_id]

        match = Match(None, "football", [], [])
        match.id = int(match_id)

        # --------Joueurs à domicile------------
        colonnes_home = [f"home_player_{j}" for j in range(1, 12)]
        for col in colonnes_home:
            id_joueur = row[col]
            if pd.notna(id_joueur):
                # .get() cherche l'ID dans le dico. S'il n'existe pas, ça renvoie None sans planter
                nom_joueur = self.dict_joueurs.get(int(id_joueur))
                if nom_joueur:
                    match.list_home_player.append(nom_joueur)

        # --------Joueurs à l'extérieur--------------
        colonnes_away = [f"away_player_{j}" for j in range(1, 12)]
        for col in colonnes_away:
            id_joueur = row[col]
            if pd.notna(id_joueur):
                nom_joueur = self.dict_joueurs.get(int(id_joueur))
                if nom_joueur:
                    match.list_away_player.append(nom_joueur)

        return match

    def load_all_match(self):
        """
        Optionnel : Si tu as quand même besoin de charger TOUS les matchs d'un coup, 
        tu peux réutiliser la fonction get_match pour que le code reste propre.
        """
        res = []
        for match_id in self.df_football.index:
            res.append(self.get_match(match_id))
        return res