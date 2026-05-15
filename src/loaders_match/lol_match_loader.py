import pandas as pd

from match import Match

pd.options.display.max_columns = 100


class LolMatchLoader:
    """Chargeur spécifique à League of Legends (LoL) pour l'extraction et la structuration des données."""

    def __init__(self) -> None:
        """Initialise la classe."""
        pass

    def load_all_match(self) -> list[Match]:
        """Charge, traduit et compile l'ensemble des matchs League of Legends.

        Returns:
        -------
        list[Match]
            Une collection complète d'objets Match enrichis avec les données LoL.
        """
        res = []
        df_lol_match = pd.read_csv("data/league_of_legends_tdd/match.csv")
        df_lol_team = pd.read_csv("data/league_of_legends_tdd/team.csv")
        df_lol_player = pd.read_csv("data/league_of_legends_tdd/player.csv")

        dict_equipes = dict(zip(df_lol_team["team_abbreviation"], df_lol_team["team"]))
        dict_ids = dict(zip(df_lol_team["team_abbreviation"], df_lol_team.index + 1)) #La table des matchs de lol n'a pas d'id dans le csv
        #Du coup on lui crée un id car dans le fichier main on utilise une comparaison d'id

        for i in range(len(df_lol_match)):
            match = Match(None, "lol", None, None)
            match.id = i + 2

            abbr_blue = df_lol_match.loc[i, "team_blue"]
            abbr_red = df_lol_match.loc[i, "team_red"]
            winner_raw = df_lol_match.loc[i, "winner"]

            nom_complet_blue = dict_equipes.get(abbr_blue, abbr_blue)
            nom_complet_red = dict_equipes.get(abbr_red, abbr_red)
            nom_winner = dict_equipes.get(winner_raw, winner_raw)

            match.team_blue = str(nom_complet_blue).strip()
            match.team_red = str(nom_complet_red).strip()
            match.home_team_api_id = str(dict_ids.get(abbr_blue, ""))  # On associe l'id à un attribut de match
            match.away_team_api_id = str(dict_ids.get(abbr_red, ""))   
            match.winner = str(nom_winner).strip()

            match.date = df_lol_match.loc[i, "date"] #Ajout de diverse informations sur les matchs
            match.patch = df_lol_match.loc[i, "patch"]

            match.kills_team_blue = df_lol_match.loc[i, "kills_team_blue"]
            match.deaths_team_blue = df_lol_match.loc[i, "deaths_team_blue"]
            match.assists_team_blue = df_lol_match.loc[i, "assists_team_blue"]

            match.kills_team_red = df_lol_match.loc[i, "kills_team_red"]
            match.deaths_team_red = df_lol_match.loc[i, "deaths_team_red"]
            match.assists_team_red = df_lol_match.loc[i, "assists_team_red"]

            if abbr_blue in dict_equipes: #On assigne les équipes domiciles et extérieur aléatoirement en fonction de leur couleur (sur lol il y a pas de domicile ext)
                match.list_home_player = df_lol_player[
                    df_lol_player["team"] == nom_complet_blue
                ]["name"].tolist()
            else: #ça c'est une sécurité pour éviter de faire crash l'appli. Si on a pas l'équipe dans la base de donnée alors ça assigne rien
                match.list_home_player = []

            if abbr_red in dict_equipes:
                match.list_away_player = df_lol_player[
                    df_lol_player["team"] == nom_complet_red
                ]["name"].tolist()
            else:
                match.list_away_player = []

            res.append(match)

        return res
