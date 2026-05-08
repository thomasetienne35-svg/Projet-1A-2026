from types import SimpleNamespace

import pandas as pd

from src.statistiques.nbre_de_points import ChampionshipPointsCalculator


def preparer_donnees_test() -> tuple[list[SimpleNamespace], list[SimpleNamespace]]:
    """Crée un petit environnement de test avec 2 équipes."""
    team_1 = SimpleNamespace(id=10, name="Paris SG")
    team_2 = SimpleNamespace(id=20, name="Marseille")

    equipes = [team_1, team_2]

    match_1 = SimpleNamespace(
        season="2024",
        home_team_api_id=10,
        away_team_api_id=20,
        home_team_goal=2,
        away_team_goal=1,
    )
    match_2 = SimpleNamespace(
        season="2024",
        home_team_api_id=20,
        away_team_api_id=10,
        home_team_goal=1,
        away_team_goal=1,
    )

    matchs = [match_1, match_2]
    return equipes, matchs


def test_calcul_football_points() -> None:
    """Vérifie qu'une victoire (3pts) et un nul (1pt) donnent bien 4 points."""
    equipes, matchs = preparer_donnees_test()

    calc = ChampionshipPointsCalculator("football", pd.DataFrame(), equipes, matchs)

    stats = calc.get_team_points("Paris SG", saison="2024")

    assert stats["equipe"] == "Paris SG"
    assert stats["matchs_joues"] == 2
    assert stats["points"] == 4
    assert stats["buts_marques"] == 3
    assert stats["difference_buts"] == 1


def test_calcul_basketball_points() -> None:
    """Vérifie le système de points du basket (2pts victoire, 1pt défaite)."""
    team_1 = SimpleNamespace(id=100, name="Lakers")
    team_2 = SimpleNamespace(id=200, name="Bulls")

    m_basket = SimpleNamespace(
        season="2024", team_id_home=100, team_id_away=200, pts_home=90, pts_away=100
    )

    calc = ChampionshipPointsCalculator(
        "basketball", pd.DataFrame(), [team_1, team_2], [m_basket]
    )

    stats = calc.get_team_points("Lakers")

    assert stats["points_championnat"] == 1
    assert stats["defaites"] == 1


def test_lol_kda_et_winrate() -> None:
    """Vérifie le calcul du KDA et du taux de victoire sur LoL."""
    team_1 = SimpleNamespace(name="Fnatic")

    m_lol = SimpleNamespace(
        team_blue="fnatic",
        team_red="g2",
        winner="fnatic",
        kills_team_blue=10,
        deaths_team_blue=2,
        assists_team_blue=10,
    )

    calc = ChampionshipPointsCalculator("lol", pd.DataFrame(), [team_1], [m_lol])
    stats = calc.get_team_points("Fnatic")

    assert stats["win_rate"] == "100.0%"
    assert stats["kda_global"] == 10.0


def test_equipe_introuvable() -> None:
    """Vérifie que le code renvoie bien une erreur si l'équipe n'existe pas."""
    calc = ChampionshipPointsCalculator("football", pd.DataFrame(), [], [])
    calc.get_team_points("A")

    assert "Erreur : L'équipe 'A' est introuvable. Veuillez saisir son nom complet "
    "(ex: Fnatic, Team Vitality)."
