from player import Player
from sport import Sport
import pandas as pd

pd.options.display.max_columns = 100

class BasketballPlayerLoader:
    def __init__(self):
        pass

    def load_all_player(self):
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