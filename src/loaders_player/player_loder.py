<<<<<<< HEAD:src/loaders_player/player_loder.py
from player import Player
from tennis_loader import TennisPlayerLoader
from basketball_player_loader import BasketballPlayerLoader
from league_of_legends_loader import LeagueOfLegendsLoader
from football_player_loader import FootballPlayerLoader

=======
from sport import Sport
from player import Player
from football_player_loader import load_all_players
>>>>>>> 4afc8a17d8eef91bc36d3062ae95ffae9cbb771e:src/loaders_player/playerloder.py


class PlayerLoader:
    def __init__(self, sport: Sport):
        self.sport = sport

    def charger_player(self, sport) -> list[Player]:
        if sport.name == "football":
            return FootballPlayerLoader().load_all_players()
        if sport.name == "volley":
            return VolleyPlayerLoader().load_all_players()
        if sport.name == "tennis":
            return TennisPlayerLoader().load_all_players()
        if sport.name == "lol":
            return LeagueOfLegendsLoader().load_all_players()
        if sport.name == "basketball":
            return BasketballPlayerLoader().load_all_players()
        else:
            raise ValueError(
                "Le sport précisé n'est pas présent dans la base de donnée"
            )
