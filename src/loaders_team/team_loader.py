from team import Team
from sport import Sport
from .football_team_loader import FootballTeamLoader
from .basketball_team_loader import BasketballTeamLoader
from .volley_team_loader import VolleyTeamLoader
from .tennis_team_loader import TennisTeamLoader
from .lol_team_loader import LolTeamLoader


class TeamLoader:
    def load_all_teams(self, sport: Sport) -> list[Team]:
        if sport.name == "football":
            return FootballTeamLoader().load_all_team()
        elif sport.name == "volley":  
            return VolleyTeamLoader().load_all_team()
        elif sport.name == "tennis":
            return TennisTeamLoader().load_all_team()
        elif sport.name == "lol":
            return LolTeamLoader().load_all_team()
        elif sport.name == "basketball": 
            return BasketballTeamLoader().load_all_team()
        else:
            raise ValueError(f"Sport non valide : {sport.name}")