from match import Match
from sport import Sport
from .football_match_loader import FootballMatchLoader
from .basketball_match_loader import BasketballMatchLoader
from .volley_match_loader import VolleyMatchLoader
from .tennis_match_loader import TennisMatchLoader
from .lol_match_loader import LolMatchLoader


class MatchLoader:
    def load_all_matches(self, sport: Sport) -> list[Match]:
        if sport.name == "football":
            return FootballMatchLoader().load_all_match()
        elif sport.name == "volley":  
            return VolleyMatchLoader().load_all_match()
        elif sport.name == "tennis":
            return TennisMatchLoader().load_all_match()
        elif sport.name == "lol":
            return LolMatchLoader().load_all_match()
        elif sport.name == "basketball": 
            return BasketballMatchLoader().load_all_match()
        else:
            raise ValueError(f"Sport non valide : {sport.name}")
