from sport import Sport
from player import Player


class Match:
    def __init__(self, id : int, sport : Sport, list_home_player : list[int], list_away_player : list[int]) -> None:
        self.id = id
        self.sport = sport
        self.list_home_player = list_home_player
        self.list_away_player = list_away_player
