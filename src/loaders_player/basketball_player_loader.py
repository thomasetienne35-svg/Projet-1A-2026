from player import Player
from sport import Sport

import pandas as pd

pd.options.display.max_columns = 100

# Ce qu'on veut mettre dans notre Player : Nom, nationalité, date_naissance, genre


class BasketballPlayerLoader:
    def __init__(self):
        pass

    def load_all_player(self):
        res = []
        df_basketball = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/basketball/player.csv"
        )
        for i in range(len(df_basketball)):
            joueur = Player(None, first_name, last_name, birthdate, height, weight, team_id)
            joueur.nom = df_basketball.loc[i, "player_name"]
            joueur.data_naissance = df_basketball.loc[i, "player_name"]
            
            res.append(joueur)
        return res