from team import Team
import pandas as pd

# pd.options.display.max_columns = 100


class FootballTeamLoader:
    def __init__(self):
        pass

    def load_all_team(self):
        res = []
        df_football = pd.read_csv(
            "data/football_european_leagues_tdd/team.csv" 
        )
        
        for i in range(len(df_football)):
            equipe = Team(None, None, None)
            
            equipe.id = df_football.loc[i, "team_api_id"]
            equipe.nom = df_football.loc[i, "team_long_name"]
            equipe.nom_abrege = df_football.loc[i, "team_short_name"]
            
            res.append(equipe)
            
        return res