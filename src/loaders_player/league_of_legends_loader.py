from player import Player
import pandas as pd

pd.options.display.max_columns = 100


class LeagueOfLegendsLoader:
    def __init__(self):
        pass

    def load_all_player(self):
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
                team=df_lol.loc[i, "team"] # Ici on passe directement le nom (String)
                )
            
            res.append(joueur)
        return res