from match import Match
from sport import Sport
import pandas as pd

pd.options.display.max_columns = 100

class BasketballMatchLoader:
    def __init__(self):
        pass

    def load_all_match(self):
        res = []
        df_basketball = pd.read_csv("data/basketball/game.csv")
        df_basketball_joueurs = pd.read_csv("data/basketball/player.csv")
        
        for i in range(len(df_basketball)):
            match = Match(None, "basketball", None, None)
            
            match.id = df_basketball.loc[i, "game_id"]
            
            id_home = df_basketball.loc[i, "team_id_home"]
            id_away = df_basketball.loc[i, "team_id_away"]
            
            match.team_id_home = id_home
            match.team_id_away = id_away
            match.pts_home = df_basketball.loc[i, "pts_home"]
            match.pts_away = df_basketball.loc[i, "pts_away"]
            match.season = df_basketball.loc[i, "season"]
            
            joueur_home_lignes = df_basketball_joueurs[df_basketball_joueurs["team_id"] == id_home]
            joueur_away_lignes = df_basketball_joueurs[df_basketball_joueurs["team_id"] == id_away]
            
            match.list_home_player = (joueur_home_lignes["first_name"] + " " + joueur_home_lignes["last_name"]).tolist()
            match.list_away_player = (joueur_away_lignes["first_name"] + " " + joueur_away_lignes["last_name"]).tolist()
            
            res.append(match)
            
        return res