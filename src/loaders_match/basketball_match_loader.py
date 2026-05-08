import pandas as pd

from match import Match

pd.options.display.max_columns = 100


class BasketballMatchLoader:
    """Chargeur spécifique au basketball pour l'extraction et la structuration des données."""

    def __init__(self) -> None:
        pass

    def load_all_match(self) -> list[Match]:
        """Charge et compile les données des matchs de basketball et de leurs joueurs à partir des fichiers CSV.

        Returns:
        -------
        list[Match]
            Une liste d'objets Match où chaque instance contient les informations.
        """
        res = []
        df_basketball = pd.read_csv("data/basketball/game.csv")
        df_basketball_joueurs = pd.read_csv("data/basketball/player.csv")

        for i in range(len(df_basketball)):
            match = Match(None, "basketball", None, None)

            match.id = df_basketball.loc[i, "game_id"]

            id_home = df_basketball.loc[i, "team_id_home"]
            id_away = df_basketball.loc[i, "team_id_away"]

            match.team_id_home = id_home
            match.team_id_away = id_away
            match.season = df_basketball.loc[i, "season"]

            try:
                score_h = float(df_basketball.loc[i, "pts_home"])
                score_a = float(df_basketball.loc[i, "pts_away"])
            except Exception:
                score_h = 0.0
                score_a = 0.0

            match.home_team_score = score_h
            match.away_team_score = score_a

            match.pts_home = score_h
            match.pts_away = score_a

            joueur_home_lignes = df_basketball_joueurs[
                df_basketball_joueurs["team_id"] == id_home
            ]
            joueur_away_lignes = df_basketball_joueurs[
                df_basketball_joueurs["team_id"] == id_away
            ]

            match.list_home_player = (
                joueur_home_lignes["first_name"] + " " + joueur_home_lignes["last_name"]
            ).tolist()
            match.list_away_player = (
                joueur_away_lignes["first_name"] + " " + joueur_away_lignes["last_name"]
            ).tolist()

            res.append(match)

        return res
