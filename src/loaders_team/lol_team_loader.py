from team import Team
import pandas as pd

# pd.options.display.max_columns = 100

class LolTeamLoader:
    def __init__(self):
        pass

    def load_all_team(self):
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