from player import Player
from sport import Sport

import pandas as pd

pd.options.display.max_columns = 100

# Ce qu'on veut mettre dans notre Player : Nom, nationalité, date_naissance, genre


class BasketballPlayerLoader:
    def __init__():
        pass

    def load_all_player():
        res = []
        df_football = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/basketball/player.csv"
        )
        for i in range(len(df_football)):
            joueur = Player(None, None, None, "H")
            joueur.nom = df_football.loc[i, "player_name"]
            joueur.data_naissance = df_football.loc[i, "player_name"]
            res.append(joueur)
        return res