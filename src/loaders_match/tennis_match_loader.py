import pandas as pd

from match import Match


class TennisMatchLoaderFemme:
    """Chargeur spécialisé pour les matchs de tennis féminin (WTA)."""

    def __init__(self, chemin_matchs: str, chemin_joueuses: str) -> None:
        self.chemin_matchs = chemin_matchs
        self.chemin_joueuses = chemin_joueuses

    def load_all_match(self) -> list[Match]:
        """Charge et traite l'intégralité des matchs féminins.

        Returns:
        -------
        list[Match]
            Liste des matchs WTA formatés.
        """
        res = []
        df_matchs = pd.read_csv(self.chemin_matchs)
        df_joueuses = pd.read_csv(self.chemin_joueuses)

        df_joueuses["nom_complet"] = (
            df_joueuses["name_first"].astype(str)
            + " "
            + df_joueuses["name_last"].astype(str)
        )

        dict_joueuses = dict(zip(df_joueuses["player_id"], df_joueuses["nom_complet"]))

        for i in range(len(df_matchs)):
            match = Match(None, "tennis", [], [])
            match.id = f"F{i + 1}"

            id_gagnante = df_matchs.loc[i, "winner_id"]
            id_perdante = df_matchs.loc[i, "loser_id"]

            nom_gagnante = dict_joueuses.get(id_gagnante, str(id_gagnante))
            nom_perdante = dict_joueuses.get(id_perdante, str(id_perdante))

            match.list_home_player = [nom_gagnante]
            match.list_away_player = [nom_perdante]
            res.append(match)

        return res


class TennisMatchLoaderHomme:
    """Chargeur spécialisé pour les matchs de tennis masculin (ATP)."""

    def __init__(self, chemin_matchs: str, chemin_joueurs: str) -> None:
        self.chemin_matchs = chemin_matchs
        self.chemin_joueurs = chemin_joueurs

    def load_all_match(self) -> list[Match]:
        """Charge et traite l'intégralité des matchs masculins.

        Returns:
        -------
        list[Match]
            Liste des matchs ATP formatés.
        """
        res = []
        df_matchs = pd.read_csv(self.chemin_matchs)
        df_joueurs = pd.read_csv(self.chemin_joueurs)

        df_joueurs["nom_complet"] = (
            df_joueurs["name_first"].astype(str)
            + " "
            + df_joueurs["name_last"].astype(str)
        )
        dict_joueurs = dict(zip(df_joueurs["player_id"], df_joueurs["nom_complet"]))

        for i in range(len(df_matchs)):
            match = Match(None, "tennis", [], [])
            match.id = f"H{i + 1}"

            id_gagnant = df_matchs.loc[i, "winner_id"]
            id_perdant = df_matchs.loc[i, "loser_id"]

            nom_gagnant = dict_joueurs.get(id_gagnant, str(id_gagnant))
            nom_perdant = dict_joueurs.get(id_perdant, str(id_perdant))

            match.list_home_player = [nom_gagnant]
            match.list_away_player = [nom_perdant]
            res.append(match)

        return res


class TennisMatchLoader:
    """Charger simultanément les données ATP et WTA en utilisant les chargeurs spécialisés."""

    def __init__(self) -> None:
        pass

    def load_all_match(self) -> list[Match]:
        """Exécute le chargement complet (Hommes + Femmes) des données de tennis.

        Returns:
        -------
        list[Match]
            Liste combinée de tous les matchs de tennis (ATP et WTA).
        """
        chemin_matchs_wta = "data/tennis_tdd/wta_matches_2024.csv"
        chemin_matchs_atp = "data/tennis_tdd/atp_matches_2024.csv"

        chemin_joueuses_wta = "data/tennis_tdd/wta_players_2024.csv"
        chemin_joueurs_atp = "data/tennis_tdd/atp_players_2024.csv"

        loader_femme = TennisMatchLoaderFemme(chemin_matchs_wta, chemin_joueuses_wta)
        liste_matchs_femmes = loader_femme.load_all_match()

        loader_homme = TennisMatchLoaderHomme(chemin_matchs_atp, chemin_joueurs_atp)
        liste_matchs_hommes = loader_homme.load_all_match()

        return liste_matchs_femmes + liste_matchs_hommes
