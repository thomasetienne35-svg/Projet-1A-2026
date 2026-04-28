from sport import Sport
from player import Player


class Match:
    def __init__(self, id : int, sport : Sport, list_home_player : list[int], list_away_player : list[int]) -> None:
        self.id = id
        self.sport = sport
        self.list_home_player = list_home_player
        self.list_away_player = list_away_player

    def has_player(self, player_id: int) -> bool:
        """
        Vérifie si le joueur (via son ID) a participé à ce match, 
        que ce soit à domicile ou à l'extérieur.
        """
        return (player_id in self.list_home_player) or (player_id in self.list_away_player)