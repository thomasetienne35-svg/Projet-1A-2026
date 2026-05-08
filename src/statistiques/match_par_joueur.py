from types import SimpleNamespace
from typing import Any


class PlayerStatsCalculator:
    """Définit la classe PlayerStatsCalulator."""

    def __init__(self, sport_obj, liste_matchs):
        """On initialise avec l'objet sport et la liste des matchs pour éviter de les repasser en argument à chaque fois."""
        self.sport_name = sport_obj.name.lower()
        self.matchs = liste_matchs

    def obtenir_bilan(self, nom_joueur: str) -> dict | str:
        """Donne le bilan des statistiques d'un joueur."""
        nom_recherche = nom_joueur.strip().lower()
        nb_matchs = victoires = defaites = nuls = 0
        vrai_nom = nom_joueur

        for match in self.matchs:
            is_home = any(
                nom_recherche in str(p).lower()
                for p in getattr(match, "list_home_player", [])
            )
            is_away = any(
                nom_recherche in str(p).lower()
                for p in getattr(match, "list_away_player", [])
            )

            if not is_home and not is_away:
                continue

            if is_home:
                for p in match.list_home_player:
                    if nom_recherche in str(p).lower():
                        vrai_nom = str(p)
                        break
            else:
                for p in match.list_away_player:
                    if nom_recherche in str(p).lower():
                        vrai_nom = str(p)
                        break

            nb_matchs += 1

            try:
                res = self._analyser_victoire(match, is_home, is_away)
                if res == "V":
                    victoires += 1
                elif res == "D":
                    defaites += 1
                elif res == "N":
                    nuls += 1
            except Exception:
                continue

        if nb_matchs == 0:
            return f"Aucune statistique pour '{nom_joueur}'."

        win_rate = round((victoires / nb_matchs) * 100, 1)

        return {
            "joueur": vrai_nom,
            "sport": self.sport_name.capitalize(),
            "matchs_joues": nb_matchs,
            "victoires": victoires,
            "nuls": nuls,
            "defaites": defaites,
            "win_rate": f"{win_rate}%",
        }

    def _analyser_victoire(self, match, is_home, is_away):
        """Méthode privée pour isoler la logique métier par sport."""
        if self.sport_name == "tennis":
            return "V" if is_home else "D"

        elif self.sport_name == "lol":
            winner = str(getattr(match, "winner", "")).lower()
            blue_team = str(getattr(match, "team_blue", "")).lower()
            team_won = (is_home and winner == blue_team) or (
                is_away and winner != blue_team
            )
            return "V" if team_won else "D"

        elif self.sport_name in ["basketball", "football"]:
            h_score = float(
                getattr(match, "home_team_score", getattr(match, "home_team_goal", 0))
            )
            a_score = float(
                getattr(match, "away_team_score", getattr(match, "away_team_goal", 0))
            )
            if h_score == a_score:
                return "N"
            victoire_domicile = h_score > a_score
            return (
                "V"
                if (is_home and victoire_domicile)
                or (is_away and not victoire_domicile)
                else "D"
            )


def calculer_stats_joueur(
    nom_joueur: str, sport: str, matchs: list[Any]
) -> dict[str, Any] | str:
    """Fonction adaptateur (Adapter Pattern) pour maintenir la compatibilité avec les autres modules et les tests existants."""
    sport_obj = SimpleNamespace(name=sport)

    calculateur = PlayerStatsCalculator(sport_obj, matchs)
    return calculateur.obtenir_bilan(nom_joueur)
