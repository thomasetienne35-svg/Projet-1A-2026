import pandas as pd

from player import Player

pd.options.display.max_columns = 100

class LeagueOfLegendsLoader:
    """Chargeur spécifique pour les joueurs professionnels de League of Legends.
    """
    def __init__(self) -> None:
        pass

    def load_all_player(self) -> list[Player]:
        """Charge et instancie l'ensemble des joueurs de League of Legends.

        Returns:
        -------
        list[Player]
            Une liste d'objets Player contenant les informations extraites.
        """
        res = []
        df_lol = pd.read_csv(
            "data/league_of_legends_tdd/player.csv"
        )
        for i in range(len(df_lol)):

            joueur = Player(
                prenom_nom=df_lol.loc[i, "name"], 
                nationalite=df_lol.loc[i, "country_of_birth"],
                date_naissance=df_lol.loc[i, "birthdate"],
                genre=None,
                taille=None,
                poids=None,
                team=df_lol.loc[i, "team"],
            )

            res.append(joueur)
        return res