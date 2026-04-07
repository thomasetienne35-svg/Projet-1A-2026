from match import Match
from sport import Sport

import pandas as pd

class VolleyMatchLoaderFemme:
    def __init__(self):
        pass

    def load_all_player(self):
        res = []
        df_match_volley_femme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/match_women.csv"
        )
        df_player_femme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/player_women.csv"
        )

        country_mapping = {
            "France": "FRA",
            "Türkiye": "TUR",
            "Kenya": "KEN",
            "Dominican Republic": "DOM",
            "China": "CHN",
            "United States": "USA",
            "Japan": "JPN",
            "Italy": "ITA",
            "Poland": "POL",
            "Serbia": "SRB",
            "Brazil": "BRA",
            "Netherlands": "NED"
        }

        for i in range(len(df_volley_femme)):
            
            match = Match(None, Volley : Sport, None, None)
            match.id = f"F{i+1}"
            
            pays_1 = df_match_volley_femme.loc[i, "country_1"]
            pays_2 = df_match_volley_femme.loc[i, "country_2"]
            
            code_1 = country_mapping.get(pays_1)
            code_2 = country_mapping.get(pays_2)
            
            if code_1:
                match.list_home_player = df_player_femme[df_player_femme["country_code"] == code_1]["name"].tolist()
            else:
                match.list_home_player = []
                print(f"Erreur : Le pays {pays_1} n'a pas été trouvé dans le dictionnaire.")
                
            if code_2:
                match.list_away_player = df_player_femme[df_player_femme["country_code"] == code_2]["name"].tolist()
            else:
                match.list_away_player = []
                print(f"Erreur : Le pays {pays_2} n'a pas été trouvé dans le dictionnaire.")

            res.append(match)
        return res



