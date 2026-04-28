from player import Player
from .tennis_loader import TennisPlayerLoader
from .basketball_player_loader import BasketballPlayerLoader
from .league_of_legends_loader import LeagueOfLegendsLoader
from .football_player_loader import FootballPlayerLoader
from .volley_player_loader import VolleyPlayerLoader
from sport import Sport 


class PlayerLoader:
    def __init__(self, sport: Sport):
        self.sport = sport

    def charger_player(self, sport) -> list[Player]:
        if sport.name == "football":
            return FootballPlayerLoader().load_all_player()
        if sport.name == "volley":
            return VolleyPlayerLoader().load_all_player()
        if sport.name == "tennis":
            return TennisPlayerLoader().load_all_player()
        if sport.name == "lol":
            return LeagueOfLegendsLoader().load_all_player()
        if sport.name == "basketball":
            return BasketballPlayerLoader().load_all_player()
        else:
            raise ValueError(
                "Le sport précisé n'est pas présent dans la base de donnée"
            )
