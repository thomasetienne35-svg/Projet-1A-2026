from .match import Match


class MatchLoader():
    def load_all_matches(sport: Sport) -> list[Match]:
        if sport.name == "football":
            return FootballMatchLoader().load_all_match()
        if sport.name == "basketball":
            return VolleyMatchLoader().load_all_match()
        if sport.name == "tennis":
            return TennisMatchLoader().load_all_match()
        if sport.name == "lol":
            return LolMatchLoader().load_all_match()
        if sport.name == "basketball":
            return BasketballMatchLoader().load_all_match()
        else:
            raise ValueError("Sport non valide")
