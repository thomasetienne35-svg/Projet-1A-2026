from match import Match
import pandas as pd

pd.options.display.max_columns = 100


class FootballMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_football = pd.read_csv(
            r"./data/football_european_leagues_tdd/match.csv"
        )  # Il faut trouver une solution pour cette ligne car l'emplacement de notre fichier de donnée va changer en
        # en fonction de là où on clone le repo
        df_joueur = pd.read_csv(
            r"./data/football_european_leagues_tdd/player.csv"
        )
        for i in range(len(df_football)):
            match = Match(
                None, "football", [], []
            )  # On initialise les listes de joueurs à [] et non None pour pouvoir utiliser .append()
            match.id = int(df_football.loc[i, "id"])

            # --------Joueur à domicile------------
            colonnes_home = ["home_team_goal"] + [
                f"home_player_{j}" for j in range(1, 12)
            ]
            liste_id_joueur_home = df_football.loc[
                i, colonnes_home
            ].tolist()  # On met tous les ID des joueurs dans une liste
            for id_joueur_home in range(
                len(liste_id_joueur_home)
            ):  # On récupère ensuite ces ID pour aller chercher le nom des joueurs dans le dataframe des joueurs et l'ajouter au match
                if not pd.isna(
                    liste_id_joueur_home[id_joueur_home]
                ):  # pd.isna() permet de filtrer les NaN (valeurs manquantes pandas), contrairement à "is not None" qui ne les détecte pas
                    nom_joueur_home = df_joueur.loc[
                        df_joueur["player_api_id"]
                        == liste_id_joueur_home[id_joueur_home],
                        "player_name",
                    ]  # .loc renvoie une Series pandas, on vérifie donc qu'elle n'est pas vide avant d'extraire la valeur avec .values[0]
                    if not nom_joueur_home.empty:
                        match.list_home_player.append(nom_joueur_home.values[0])

            # --------Joueur à l'extérieur--------------
            colonnes_away = ["away_team_goal"] + [
                f"away_player_{j}" for j in range(1, 12)
            ]
            liste_id_joueur_away = df_football.loc[
                i, colonnes_away
            ].tolist()  # On met tous les ID des joueurs dans une liste
            for id_joueur_away in range(
                len(liste_id_joueur_away)
            ):  # On récupère ensuite ces ID pour aller chercher le nom des joueurs dans le dataframe des joueurs et l'ajouter au match
                if not pd.isna(
                    liste_id_joueur_away[id_joueur_away]
                ):  # pd.isna() permet de filtrer les NaN (valeurs manquantes pandas), contrairement à "is not None" qui ne les détecte pas
                    nom_joueur_away = df_joueur.loc[
                        df_joueur["player_api_id"]
                        == liste_id_joueur_away[id_joueur_away],
                        "player_name",
                    ]  # .loc renvoie une Series pandas, on vérifie donc qu'elle n'est pas vide avant d'extraire la valeur avec .values[0]
                    if not nom_joueur_away.empty:
                        match.list_away_player.append(nom_joueur_away.values[0])

            res.append(match)
        return res
