import pandas as pd

from team import Team

pd.options.display.max_columns = 100

class LolTeamLoader:
    """Chargeur spécifique pour l'extraction et la structuration des équipes de LoL."""
    def __init__(self) -> None:
        pass

    def load_all_team(self) -> list[Team]:
        """Charge et instancie l'ensemble des équipes de LoL.

        Returns:
        -------
        list[Team]
            Une liste d'objets Team contenant les informations extraites.
        """
        res = []
        df_lol = pd.read_csv(
            "data/league_of_legends_tdd/team.csv" 
        )
        for i in range(len(df_lol)):
            equipe = Team(None, None, None)
            
            equipe.id = i+1
            equipe.name = df_lol.loc[i, "team"]
            equipe.short_name = df_lol.loc[i, "team_abbreviation"]
            
            res.append(equipe)
            
        return res