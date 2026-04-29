from team import Team
import pandas as pd

# pd.options.display.max_columns = 100

class VolleyTeamLoader:
    def __innit__(self):
        pass

    def load_all_team(self):
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
        