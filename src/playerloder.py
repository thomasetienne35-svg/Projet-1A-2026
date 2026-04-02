

class PlayerLoader ():
    def __init__(self, sport: Sport):
        self.sport = sport

    def charger_player(self, sport) -> Player:
        if sport.name == "football":
            return FootballPlayerLoader().load_all_players()
        if sport.name == "volley":
            return VolleyPlayerLoader().load_all_players()
        if sport.name == "tennis":
            return TennisPlayerLoader().load_all_players()
        if sport.name == "lol":
            return LolPlayerLoader().load_all_players()
        if sport.name == "basketball":
            return BasketballPlayerLoader().load_all_players()
        else:
            raise ValueError("Le sport précisé n'est pas présent dans la base de donnée")