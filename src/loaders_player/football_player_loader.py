from player import Player
import pandas as pd

pd.options.display.max_columns = 100

# Ce qu'on veut mettre dans notre Player : Prénom_NOM, nationalité, date_naissance, genre, taille, poids, team_id


class FootballPlayerLoader:
    def __init__(self):
        pass

    def load_all_player(self):
        res = []
        df_football = pd.read_csv(
            "c:/Users/id2959/Desktop/Projet-1A-2026/data/football_european_leagues_tdd/player.csv"
        )
        for i in range(len(df_football)):
            joueur = Player(None, None, None, "H", None, None, None)
            joueur.prenom_nom = df_football.loc[i, "player_name"]
            joueur.data_naissance = df_football.loc[i, "birthday"]
            joueur.poids = df_football.loc[i, "weight"]
            joueur.taille = df_football.loc[i, "height"]
            res.append(joueur)
        return res
