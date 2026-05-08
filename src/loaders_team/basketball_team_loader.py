import pandas as pd

from team import Team

pd.options.display.max_columns = 100


class BasketballTeamLoader:
    """Chargeur spécifique pour l'extraction et la structuration des équipes de basketball."""

    def __init__(self) -> None:
        """Initialise la classe."""
        pass

    def load_all_team(self) -> list[Team]:
        """Charge et instancie l'ensemble des équipes de basketball.

        Returns:
        -------
        list[Team]
            Une liste d'objets Team contenant les informations extraites.
        """
        res = []
        df_basketball = pd.read_csv("data/basketball/team.csv")
        for i in range(len(df_basketball)):
            equipe = Team(None, None, None)

            equipe.id = df_basketball.loc[i, "id"]
            equipe.name = df_basketball.loc[i, "full_name"]
            equipe.short_name = df_basketball.loc[i, "abbreviation"]

            res.append(equipe)

        return res
