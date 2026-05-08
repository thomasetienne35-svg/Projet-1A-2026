import pandas as pd

from player import Player


class TennisPlayerLoader:
    """Chargeur spécifique pour l'extraction et la structuration des données des joueurs de tennis."""
    def __init__(self) -> None:
        pass

    def load_all_player(self) -> list[Player]:
        """Charge et instancie l'ensemble des joueurs de tennis.

        Returns:
        -------
        list[Player]
            Une liste d'objets Player contenant les informations extraites.
        """
        res = []

        df_atp = pd.read_csv("data/tennis_tdd/atp_players_2024.csv")
        df_wta = pd.read_csv("data/tennis_tdd/wta_players_2024.csv")

        df_atp["genre"] = "Homme"
        df_wta["genre"] = "Femme"

        df_tennis = pd.concat([df_atp, df_wta], ignore_index=True)

        for i in range(len(df_tennis)):
            prenom = str(df_tennis.loc[i, "name_first"])
            nom = str(df_tennis.loc[i, "name_last"])
            nom_complet = f"{prenom} {nom}"

            joueur = Player(None, None, None, None, None, None, None)
            
            joueur.prenom_nom = nom_complet
            joueur.nationalite = df_tennis.loc[i, "ioc"] 
            joueur.date_naissance = df_tennis.loc[i, "dob"] 
            joueur.genre = df_tennis.loc[i, "genre"] 
            joueur.height = df_tennis.loc[i, "height"]
            joueur.poids = None
            joueur.team = None
            
            res.append(joueur)

        return res