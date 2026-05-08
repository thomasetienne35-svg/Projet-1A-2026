import pandas as pd

from match import Match

pd.options.display.max_columns = 100


class FootballMatchLoader:
    """Chargeur spécifique au football pour l'extraction et la structuration des données."""

    def __init__(self) -> None:
        """Initialise la classe."""
        chemin_match = "data/football_european_leagues_tdd/match.csv"
        chemin_joueur = "data/football_european_leagues_tdd/player.csv"

        self.df_football = pd.read_csv(chemin_match)
        df_joueur = pd.read_csv(chemin_joueur)

        self.df_football.set_index("id", inplace=True)

        self.dict_joueurs = df_joueur.set_index("player_api_id")[
            "player_name"
        ].to_dict()

    def get_match(self, match_id: int) -> Match | None:
        """Récupère et structure les données d'un match spécifique à partir de son ID.

        Parameters
        ----------
        match_id : int
            L'identifiant unique du match à rechercher.

        Returns:
        -------
        Match
            Un objet Match enrichi avec les scores et les listes
            de joueurs (domicile/extérieur).

        None
            Si le match_id est introuvable.

        """
        if match_id not in self.df_football.index:
            print(f"Match {match_id} introuvable.")
            return None

        row = self.df_football.loc[match_id]

        match = Match(None, "football", [], [])
        match.id = int(match_id)

        match.home_team_api_id = row["home_team_api_id"]
        match.away_team_api_id = row["away_team_api_id"]
        match.home_team_goal = row["home_team_goal"]
        match.away_team_goal = row["away_team_goal"]
        match.season = row["season"]

        colonnes_home = [f"home_player_{j}" for j in range(1, 12)]
        for col in colonnes_home:
            id_joueur = row[col]
            if pd.notna(id_joueur):
                nom_joueur = self.dict_joueurs.get(int(id_joueur))
                if nom_joueur:
                    match.list_home_player.append(nom_joueur)

        colonnes_away = [f"away_player_{j}" for j in range(1, 12)]
        for col in colonnes_away:
            id_joueur = row[col]
            if pd.notna(id_joueur):
                nom_joueur = self.dict_joueurs.get(int(id_joueur))
                if nom_joueur:
                    match.list_away_player.append(nom_joueur)

        return match

    def load_all_match(self) -> list[Match]:
        """Charge et instancie l'ensemble des matchs de football du jeu de données.

        Returns:
        -------
        list[Match]
            Contient tous les objets Match instancier.
        """
        res = []
        for match_id in self.df_football.index:
            res.append(self.get_match(match_id))
        return res
