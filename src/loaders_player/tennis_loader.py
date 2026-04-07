from player import Player
import pandas as pd


class TennisPlayerLoader:
    def __init__(self):
        pass

    def load_all_player(self):
        res = []

        df_atp = pd.read_csv("data/tennis_tdd/atp_players_2024.csv")
        df_wta = pd.read_csv("data/tennis_tdd/wta_players_2024.csv")

        df_atp["genre"] = "Homme"
        df_wta["genre"] = "Femme"

        df_tennis = pd.concat([df_atp, df_wta], ignore_index=True)

        for i in range(len(df_tennis)):
            prenom = str(df_tennis.loc[i, "name_first"])
            nom = str(df_tennis.loc[i, "name_last"])
            nom_complet = f"{prenom} {nom}"

            joueur = Player(
                prenom_nom = nom_complet,
                nationalite = df_tennis.loc[i, "ioc"], 
                date_naissance = df_tennis.loc[i, "dob"], 
                genre = df_tennis.loc[i, "genre"], 
                taille = df_tennis.loc[i, "height"],
                poids = None,
                equipe = None
            )
            
            res.append(joueur)

        return res