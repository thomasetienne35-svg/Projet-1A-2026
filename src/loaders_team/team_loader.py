from sport import Sport
from team import Team

from .basketball_team_loader import BasketballTeamLoader
from .football_team_loader import FootballTeamLoader
from .lol_team_loader import LolTeamLoader
from .tennis_team_loader import TennisTeamLoader
from .volley_team_loader import VolleyTeamLoader


class TeamLoader:
    """Chargement centralisée pour les équipes de tous les sports."""
    def load_all_teams(self, sport: Sport) -> list[Team]:
        """Chargement des équipes vers le chargeur spécifique au sport.

        Parameters
        ----------
        sport : Sport
            L'objet Sport définissant la discipline à charger.

        Returns:
        -------
        list[Team]
            La collection complète des joueurs pour le sport demandé.

        Raises:
        ------
        ValueError
            Si le nom du sport fourni n'est pas reconnu.
        """
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