from player import Player
import pandas as pd

pd.options.display.max_columns = 100

class FootballPlayerLoader:
    """Chargeur spécifique pour l'extraction et la structuration des données des joueurs de football.
    """
    def __init__(self) -> None:
        pass

    def load_all_player(self) -> list[Player]:
        """Charge et instancie l'ensemble des joueurs de football depuis le fichier de données.

        Returns
        -------
        list[Player]
            Une liste d'objets Player enrichis avec les données extraites.
        """
        res = []
        df_football = pd.read_csv(
            "data/football_european_leagues_tdd/player.csv"
        )
        for i in range(len(df_football)):
            joueur = Player(None, None, None, "H", None, None, None)
            joueur.prenom_nom = df_football.loc[i, "player_name"]
            joueur.data_naissance = df_football.loc[i, "birthday"]
            joueur.poids = df_football.loc[i, "weight (kg)"]
            joueur.height = df_football.loc[i, "height (cm)"]
            res.append(joueur)
        return res
