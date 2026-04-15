import pandas as pd
import numpy as np


class ChampionshipPointsCalculator:
    def __init__(self, sport_name: str, matches_df: pd.DataFrame):
        """
        Initialise le calculateur avec le nom du sport et le DataFrame des matchs.
        """
        self.sport_name = sport_name.lower()
        self.matches_df = matches_df

    def get_team_points(self) -> pd.DataFrame:
        """
        Méthode principale qui agit comme un "aiguilleur".
        Elle redirige vers la bonne méthode de calcul selon le sport.
        """
        if self.sport_name == "football":
            return self._calculate_football_points()
        
        elif self.sport_name == "basketball":
            return self._calculate_basketball_points()
            
        elif self.sport_name == "tennis":
            return self._calculate_tennis_points()
            
        elif self.sport_name in ["volley", "volleyball"]:
            return self._calculate_volley_points()
            
        elif self.sport_name == "lol":
            return self._calculate_lol_points()
            
        else:
            raise ValueError(f"Statistiques non implémentées pour le sport : {self.sport_name}")

    def _calculate_football_points(self):
        
        df = self.matches_df.copy()
        
        team_id = None
    
        for equipe in df_equipes_foot:
            if equipe.name.lower() == nom_equipe.lower(): 
                team_id = equipe.id
                break
    
        if team_id is None:
            return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        matchs_domicile = df_matches_foot[df_matches_foot['home_team_api_id'] == team_id]
        matchs_exterieur = df_matches_foot[df_matches_foot['away_team_api_id'] == team_id]

        victoires_dom = (matchs_domicile['home_team_goal'] > matchs_domicile['away_team_goal']).sum()
        nuls_dom = (matchs_domicile['home_team_goal'] == matchs_domicile['away_team_goal']).sum()
    
        victoires_ext = (matchs_exterieur['away_team_goal'] > matchs_exterieur['home_team_goal']).sum()
        nuls_ext = (matchs_exterieur['home_team_goal'] == matchs_exterieur['away_team_goal']).sum()

        points_totaux = ((victoires_dom + victoires_ext) * 3) + ((nuls_dom + nuls_ext) * 1)
    
        return points_totaux

        # --- TON CODE ICI ---
        
        raise NotImplementedError("Le calcul pour le football n'est pas encore codé !")

    def _calculate_basketball_points(self):
        # RAPPEL : Au basket, il n'y a généralement pas de match nul. Victoire = x pts, Défaite = y pts (selon ton barème).
        df = self.matches_df.copy()
        
        # --- TON CODE ICI ---
        
        raise NotImplementedError("Le calcul pour le basketball n'est pas encore codé !")

    def _calculate_tennis_points(self):
        # RAPPEL : Le tennis est un sport individuel. Tu peux compter le nombre de victoires par joueur.
        df = self.matches_df.copy()
        
        # --- TON CODE ICI ---
        
        raise NotImplementedError("Le calcul pour le tennis n'est pas encore codé !")

    def _calculate_volley_points(self):
        # RAPPEL : Au volley, le barème peut dépendre du score final (ex: victoire 3-0/3-1 = 3pts, victoire 3-2 = 2pts, défaite 2-3 = 1pt).
        df = self.matches_df.copy()
        
        # --- TON CODE ICI ---
        
        raise NotImplementedError("Le calcul pour le volley n'est pas encore codé !")

    def _calculate_lol_points(self):
        # RAPPEL : Calcul simple du nombre de parties gagnées par équipe.
        df = self.matches_df.copy()
        
        # --- TON CODE ICI ---
        
        raise NotImplementedError("Le calcul pour LoL n'est pas encore codé !")