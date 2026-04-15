from match import Match
from sport import Sport

import pandas as pd


class VolleyMatchLoaderFemme:
    def __init__(self):
        pass

    def load_all_match(self):
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
            "Netherlands": "NED",
        }

        for i in range(len(df_match_volley_femme)):
            
            match = Match(None, "volley" : Sport, None, None)
            match.id = f"F{i+1}"
            
            pays_1 = df_match_volley_femme.loc[i, "country_1"]
            pays_2 = df_match_volley_femme.loc[i, "country_2"]

            code_1 = country_mapping.get(pays_1)
            code_2 = country_mapping.get(pays_2)

            if code_1:
                match.list_home_player = df_player_femme[
                    df_player_femme["country_code"] == code_1
                ]["name"].tolist()
            else:
                match.list_home_player = []
                print(
                    f"Erreur : Le pays {pays_1} n'a pas été trouvé dans le dictionnaire."
                )

            if code_2:
                match.list_away_player = df_player_femme[
                    df_player_femme["country_code"] == code_2
                ]["name"].tolist()
            else:
                match.list_away_player = []
                print(
                    f"Erreur : Le pays {pays_2} n'a pas été trouvé dans le dictionnaire."
                )

            res.append(match)
        return res


class VolleyMatchLoaderHomme:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_match_volley_homme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/match_men.csv"
        )
        df_player_homme = pd.read_csv(
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/player_men.csv"
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
            "Netherlands": "NED",
        }

        for i in range(len(df_match_volley_homme)):
            match = Match(None, "volley", Sport, None, None)
            match.id = f"H{i + 1}"

            pays_1 = df_match_volley_homme.loc[i, "country_1"]
            pays_2 = df_match_volley_homme.loc[i, "country_2"]

            code_1 = country_mapping.get(pays_1)
            code_2 = country_mapping.get(pays_2)

            if code_1:
                match.list_home_player = df_player_homme[
                    df_player_homme["country_code"] == code_1
                ]["name"].tolist()
            else:
                match.list_home_player = []
                print(
                    f"Erreur : Le pays {pays_1} n'a pas été trouvé dans le dictionnaire."
                )

            if code_2:
                match.list_away_player = df_player_homme[
                    df_player_homme["country_code"] == code_2
                ]["name"].tolist()
            else:
                match.list_away_player = []
                print(
                    f"Erreur : Le pays {pays_2} n'a pas été trouvé dans le dictionnaire."
                )

            res.append(match)
        return res


class VolleyMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        chemin_match_f = (
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/match_women.csv"
        )
        chemin_player_f = (
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/player_women.csv"
        )

        chemin_match_h = (
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/match_men.csv"
        )
        chemin_player_h = (
            "/home/onyxia/work/Projet-1A-2026/data/volleyball_tdd/player_men.csv"
        )

        mapping_femmes = {
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
            "Netherlands": "NED",
        }

        mapping_hommes = {
            "France": "FRA",
            "Poland": "POL",
            "Slovenia": "SLO",
            "Italy": "ITA",
            "United States": "USA",
            "Brazil": "BRA",
            "Japan": "JPN",
            "Germany": "GER",
            "Argentina": "ARG",
            "Serbia": "SRB",
            "Canada": "CAN",
            "Egypt": "EGY",
        }

        loader_femme = VolleyMatchLoader(
            chemin_match_f, chemin_player_f, mapping_femmes
        )
        liste_matchs_femmes = loader_femme.load_all_matches()

        loader_homme = VolleyMatchLoader(
            chemin_match_h, chemin_player_h, mapping_hommes
        )
        liste_matchs_hommes = loader_homme.load_all_matches()

        matchs_volley = liste_matchs_femmes + liste_matchs_hommes

        for index, match in enumerate(matchs_volley):
            match.id = f"M{index + 1}"

        return matchs_volley
