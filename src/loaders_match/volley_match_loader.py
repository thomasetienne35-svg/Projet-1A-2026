from match import Match
import pandas as pd

class VolleyMatchLoaderFemme:
    """Chargeur spécifique pour les matchs de volley-ball féminin.
    """
    def __init__(self) -> None:
        pass

    def load_all_match(self) -> list[Match]:
        """Charge, nettoie et compile l'intégralité des matchs de volley-ball féminin.

        Returns
        -------
        list[Match]
            Une collection complète d'objets Match enrichis avec les scores (sets), la date, l'étape du tournoi et les joueuses.
        """
        res = []
        df_match_volley_femme = pd.read_csv("data/volleyball_tdd/match_women.csv")
        df_player_femme = pd.read_csv("data/volleyball_tdd/player_women.csv")

        country_mapping = {
            "France": "FRA", "Türkiye": "TUR", "Kenya": "KEN",
            "Dominican Republic": "DOM", "China": "CHN", "United States": "USA",
            "Japan": "JPN", "Italy": "ITA", "Poland": "POL",
            "Serbia": "SRB", "Brazil": "BRA", "Netherlands": "NED",
        }

        for i in range(len(df_match_volley_femme)):
            match = Match(None, "volley", [], [])
            match.id = f"F{i+1}"
            match.genre = "Femme"

            pays_1 = df_match_volley_femme.loc[i, "country_1"]
            pays_2 = df_match_volley_femme.loc[i, "country_2"]

            code_1 = country_mapping.get(pays_1, pays_1)
            code_2 = country_mapping.get(pays_2, pays_2)

            match.country_code_1 = code_1
            match.country_code_2 = code_2
            match.set_country_1 = df_match_volley_femme.loc[i, "set_country_1"]
            match.set_country_2 = df_match_volley_femme.loc[i, "set_country_2"]
            match.date = df_match_volley_femme.loc[i, "date"] 
            match.stage = df_match_volley_femme.loc[i, "stage"]

            if code_1:
                match.list_home_player = df_player_femme[
                    df_player_femme["country_code"] == code_1
                ]["name"].tolist()
            else:
                print(f"Erreur : Le pays {pays_1} n'a pas été trouvé dans le dictionnaire.")

            if code_2:
                match.list_away_player = df_player_femme[
                    df_player_femme["country_code"] == code_2
                ]["name"].tolist()
            else:
                print(f"Erreur : Le pays {pays_2} n'a pas été trouvé dans le dictionnaire.")

            res.append(match)
        return res


class VolleyMatchLoaderHomme:
    """Chargeur spécifique pour les matchs de volley-ball masculin.
    """
    def __init__(self) -> None:
        pass

    def load_all_match(self) -> list[Match]:
        """Charge, nettoie et compile l'intégralité des matchs de volley-ball masculin.

        Returns
        -------
        list[Match]
            Une collection complète d'objets Match enrichis avec les scores (sets), la date, l'étape du tournoi et les joueurs.
        """
        res = []
        df_match_volley_homme = pd.read_csv("data/volleyball_tdd/match_men.csv")
        df_player_homme = pd.read_csv("data/volleyball_tdd/player_men.csv")

        country_mapping = {
            "France": "FRA", "Poland": "POL", "Slovenia": "SLO",
            "Italy": "ITA", "United States": "USA", "Brazil": "BRA",
            "Japan": "JPN", "Germany": "GER", "Argentina": "ARG",
            "Serbia": "SRB", "Canada": "CAN", "Egypt": "EGY",
        }

        for i in range(len(df_match_volley_homme)):
            match = Match(None, "volley", [], [])
            match.id = f"H{i + 1}"
            match.genre = "Homme"

            pays_1 = df_match_volley_homme.loc[i, "country_code_1"]
            pays_2 = df_match_volley_homme.loc[i, "country_code_2"]

            code_1 = country_mapping.get(pays_1, pays_1)
            code_2 = country_mapping.get(pays_2, pays_2)

            match.country_code_1 = code_1
            match.country_code_2 = code_2
            match.set_country_1 = df_match_volley_homme.loc[i, "set_country_1"]
            match.set_country_2 = df_match_volley_homme.loc[i, "set_country_2"]
            match.date = df_match_volley_homme.loc[i, "date"]
            match.stage = df_match_volley_homme.loc[i, "stage"]
            if code_1:
                match.list_home_player = df_player_homme[
                    df_player_homme["country_code"] == code_1
                ]["name"].tolist()
            else:
                print(f"Erreur : Le pays {pays_1} n'a pas été trouvé dans le dictionnaire.")

            if code_2:
                match.list_away_player = df_player_homme[
                    df_player_homme["country_code"] == code_2
                ]["name"].tolist()
            else:
                print(f"Erreur : Le pays {pays_2} n'a pas été trouvé dans le dictionnaire.")

            res.append(match)
        return res


class VolleyMatchLoader:
    """Charger simultanément les données homme et femme en utilisant les chargeurs spécialisés.
    """
    def __init__(self) -> None:
        pass

    def load_all_match(self) -> list[Match]:
        """Exécute le chargement complet (Hommes + Femmes) des données de volley.

        Returns
        -------
        list[Match]
            Liste combinée de tous les matchs de volley.
        """
        loader_femme = VolleyMatchLoaderFemme()
        liste_matchs_femmes = loader_femme.load_all_match() 

        loader_homme = VolleyMatchLoaderHomme()
        liste_matchs_hommes = loader_homme.load_all_match() 

        matchs_volley = liste_matchs_femmes + liste_matchs_hommes

        for index, match in enumerate(matchs_volley):
            match.id = f"M{index + 1}"

        return matchs_volley