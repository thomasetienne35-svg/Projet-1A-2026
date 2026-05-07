from team import Team
import pandas as pd

pd.options.display.max_columns = 100

class VolleyTeamLoader:
    """Chargeur spécifique pour l'extraction et la structuration des équipes de volley.
    """
    def __innit__(self) -> None:
        pass

    def load_all_team(self) -> list[Team]:
        """Charge et instancie l'ensemble des équipes de LoL.

        Returns
        -------
        list[Team]
            Une liste d'objets Team contenant les informations extraites.
        """
        res = []
        df_volley = pd.read_csv(
            "data/volleyball_tdd/country.csv" 
        )
        for i in range(len(df_volley)):
            equipe = Team(None, None, None)
            
            equipe.id = df_volley.loc[i, "code"]
            equipe.name = df_volley.loc[i, "country"]
            equipe.short_name = df_volley.loc[i, "country"]
            
            res.append(equipe)
            
        return res
        