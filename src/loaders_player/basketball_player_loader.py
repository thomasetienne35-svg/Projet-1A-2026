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
            "data/basketball/player.csv"
        )
        for i in range(len(df_basketball)):
            prenom = df_basketball.loc[i, "first_name"]
            nom = df_basketball.loc[i, "last_name"]
            nom_complet = f"{prenom} {nom}"

            joueur = Player(
                prenom_nom = nom_complet,
                nationalite = None,
                date_naissance = df_basketball.loc[i, "birthdate"],
                genre = None,  
                taille = df_basketball.loc[i, "height"],
                poids = df_basketball.loc[i, "weight"],
                team = df_basketball.loc[i, "team_id"]
            )
            
            res.append(joueur)
        return res 
