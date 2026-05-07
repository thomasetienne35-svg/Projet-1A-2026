import pandas as pd

from player import Player

pd.options.display.max_columns = 100

class VolleyPlayerLoader:
    """Chargeur spécifique pour l'extraction et la structuration des données des joueurs de volley."""
    def __init__(self) -> None:
        pass

    def load_all_player(self) -> list[Player]:
        """Charge et instancie l'ensemble des joueurs de volley depuis le fichier de données.

        Returns:
        -------
        list[Player]
            Une liste d'objets Player enrichis avec les données extraites.
        """
        res = []
        df_volley_men = pd.read_csv(
            "data/volleyball_tdd/player_men.csv"
        )
        for i in range(len(df_volley_men)):
            joueur = Player(None, None, None, "H", None, None, None)
            joueur.prenom_nom = df_volley_men.loc[i, "name"]
            joueur.nationalite = df_volley_men.loc[i, "country_code"]
            joueur.date_naissance = df_volley_men.loc[i, "birth_date"]
            joueur.height = df_volley_men.loc[i, "height"]
            res.append(joueur)

        df_volley_women = pd.read_csv(
            "data/volleyball_tdd/player_women.csv"
        )
        for i in range(len(df_volley_women)):
            joueur = Player(None, None, None, "F", None, None, None)
            joueur.prenom_nom = df_volley_women.loc[i, "name"]
            joueur.nationalite = df_volley_women.loc[i, "country_code"]
            joueur.date_naissance = df_volley_women.loc[i, "birth_date"]
            joueur.height = df_volley_women.loc[i, "height"]

            res.append(joueur)
        return res
