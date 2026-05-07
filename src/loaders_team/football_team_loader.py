import pandas as pd

from team import Team

pd.options.display.max_columns = 100

class FootballTeamLoader:
    """Chargeur spécifique pour l'extraction et la structuration des équipes de football."""
    def __init__(self) -> None:
        pass

    def load_all_team(self) -> list[Team]:
        """Charge et instancie l'ensemble des équipes de football.

        Returns:
        -------
        list[Team]
            Une liste d'objets Team contenant les informations extraites.
        """
        res = []
        df_football = pd.read_csv(
            "data/football_european_leagues_tdd/team.csv" 
        )
        
        for i in range(len(df_football)):
            equipe = Team(None, None, None)
            
            equipe.id = df_football.loc[i, "team_api_id"]
            equipe.name = df_football.loc[i, "team_long_name"]
            equipe.short_name = df_football.loc[i, "team_short_name"]
            
            res.append(equipe)
            
        return res