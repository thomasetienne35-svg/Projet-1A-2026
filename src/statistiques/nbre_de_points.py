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
        """Renvoie le nombre de points en championnat (victoire = 3 pts, nul = 1 pt, défaite = 0 pt), le nombre de victoire à domicile et à l'extérieur.

        Returns
        -------
        dict
            contient les informations 

        """
        team_id = None
        for equipe in liste_equipes_foot:
            if equipe.name.lower() == nom_equipe.lower(): 
                team_id = equipe.id
                break
    
        if team_id is None:
            return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        victoires_dom = 0
        victoires_ext = 0
        nuls = 0
        
        for match in liste_matchs_foot:
            
            if match.home_team_api_id == team_id:
                if match.home_team_goal > match.away_team_goal:
                    victoires_dom += 1
                elif match.home_team_goal == match.away_team_goal:
                    nuls += 1
                    
            elif match.away_team_api_id == team_id:
                if match.away_team_goal > match.home_team_goal:
                    victoires_ext += 1
                elif match.away_team_goal == match.home_team_goal:
                    nuls += 1

        points_totaux = ((victoires_dom + victoires_ext) * 3) + (nuls * 1)
    
        return {
            "points": points_totaux,
            "victoires_domicile": victoires_dom,
            "victoires_exterieur": victoires_ext
        }

    def _calculate_basketball_points(self):
        """Renvoie le nombre de points en championnat (victoire = 3 pts, nul = 1 pt, défaite = 0 pt), le nombre de victoire à domicile et à l'extérieur.

        Returns
        -------
        dict
            contient les informations 

        """
        team_id = None
        for equipe in liste_equipes_foot:
            if equipe.name.lower() == nom_equipe.lower(): 
                team_id = equipe.id
                break
    
        if team_id is None:
            return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        victoires_dom = 0
        victoires_ext = 0
        nuls = 0
        
        for match in liste_matchs_foot:
            
            if match.home_team_api_id == team_id:
                if match.home_team_goal > match.away_team_goal:
                    victoires_dom += 1
                elif match.home_team_goal == match.away_team_goal:
                    nuls += 1
                    
            elif match.away_team_api_id == team_id:
                if match.away_team_goal > match.home_team_goal:
                    victoires_ext += 1
                elif match.away_team_goal == match.home_team_goal:
                    nuls += 1

        points_totaux = ((victoires_dom + victoires_ext) * 3) + (nuls * 1)
    
        return {
            "points": points_totaux,
            "victoires_domicile": victoires_dom,
            "victoires_exterieur": victoires_ext
        }

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