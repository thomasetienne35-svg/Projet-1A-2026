from player import Player
import pandas as pd

pd.options.display.max_columns = 100

# Ce qu'on veut mettre dans notre Player : Prénom_NOM, nationalité, date_naissance, genre, taille, poids, team_id


class VolleyPlayerLoader:
    def __init__(self):
        pass

    def load_all_player(self):
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
