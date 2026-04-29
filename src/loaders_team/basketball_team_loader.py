from team import Team
import pandas as pd

# pd.options.display.max_columns = 100

class BasketballTeamLoader:
    def __init__(self):
        pass

    def load_all_team(self):
        res = []
        df_basketball = pd.read_csv(
            "data/basketball/team.csv" 
        )
        for i in range(len(df_basketball)):
            equipe = Team(None, None, None)
            
            equipe.id = df_basketball.loc[i, "id"]
            equipe.name = df_basketball.loc[i, "full_name"]
            equipe.short_name = df_basketball.loc[i, "abbreviation"]
            
            res.append(equipe)
            
        return res