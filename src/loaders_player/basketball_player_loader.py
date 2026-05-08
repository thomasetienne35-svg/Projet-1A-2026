import pandas as pd

from player import Player

pd.options.display.max_columns = 100


class BasketballPlayerLoader:
    """Chargeur spécifique pour l'extraction et la structuration des données des joueurs de basketball."""

    def __init__(self) -> None:
        """Initialise la classe."""
        pass

    def load_all_player(self) -> list[Player]:
        """Charge et instancie l'ensemble des joueurs de basketball depuis le fichier de données.

        Returns:
        -------
        list[Player]
            Une liste d'objets Player enrichis avec les données extraites.
        """
        res = []
        df_basketball = pd.read_csv("data/basketball/player.csv")

        for i in range(len(df_basketball)):
            prenom = df_basketball.loc[i, "first_name"]
            nom = df_basketball.loc[i, "last_name"]
            nom_complet = f"{prenom} {nom}"
            joueur = Player(None, None, None, None, None, None, None)

            joueur.prenom_nom = nom_complet
            joueur.nationalite = None
            joueur.date_naissance = df_basketball.loc[i, "birthdate"]
            joueur.genre = None
            joueur.height = df_basketball.loc[i, "height"]
            joueur.poids = df_basketball.loc[i, "weight"]
            joueur.team = df_basketball.loc[i, "team_id"]

            res.append(joueur)

        return res
