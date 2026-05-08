from player import Player
from sport import Sport

from .basketball_player_loader import BasketballPlayerLoader
from .football_player_loader import FootballPlayerLoader
from .league_of_legends_loader import LeagueOfLegendsLoader
from .tennis_loader import TennisPlayerLoader
from .volley_player_loader import VolleyPlayerLoader


class PlayerLoader:
    """Chargement centralisée pour les joueurs de tous les sports."""

    def __init__(self, sport: Sport) -> None:
        """Initialise la classe."""
        self.sport = sport

    def charger_player(self, sport: Sport) -> list[Player]:
        """Chargement des joueurs vers le chargeur spécifique au sport.

        Parameters
        ----------
        sport : Sport
            L'objet Sport définissant la discipline à charger.

        Returns:
        -------
        list[Player]
            La collection complète des joueurs pour le sport demandé.

        Raises:
        ------
        ValueError
            Si le nom du sport fourni n'est pas reconnu.
        """
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
