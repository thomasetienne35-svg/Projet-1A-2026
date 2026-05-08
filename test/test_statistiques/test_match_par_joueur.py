from types import SimpleNamespace

from src.statistiques.match_par_joueur import calculer_stats_joueur


def test_joueur_introuvable() -> None:
    """Vérifie le cas où le joueur n'a joué aucun match."""
    resultat = calculer_stats_joueur("A", "football", [])
    assert isinstance(resultat, str)
    assert "Aucune statistique trouvée. Le joueur 'A' n'a joué "
    "aucun match ou est mal orthographié."


def test_stats_sport_a_points_et_nuls() -> None:
    """Vérifie le foot/basket (victoires, défaites, nuls et calcul du win rate)."""
    match_1 = SimpleNamespace(
        list_home_player=["Lebron James"],
        list_away_player=["Curry"],
        home_team_score=110,
        away_team_score=100,
    )
    match_2 = SimpleNamespace(
        list_home_player=["Durant"],
        list_away_player=["Lebron James"],
        home_team_score=110,
        away_team_score=100,
    )
    match_3 = SimpleNamespace(
        list_home_player=["Lebron James"],
        list_away_player=["Jokic"],
        home_team_goal=100,
        away_team_goal=100,
    )

    stats = calculer_stats_joueur("lebron", "basketball", [match_1, match_2, match_3])

    assert type(stats) is dict
    assert stats["joueur"] == "Lebron James"
    assert stats["matchs_joues"] == 3
    assert stats["victoires"] == 1
    assert stats["defaites"] == 1
    assert stats["nuls"] == 1
    assert stats["win_rate"] == "33.3%"


def test_stats_tennis_et_lol() -> None:
    """Vérifie les règles spéciales du Tennis (Home gagne toujours) et LoL."""
    # tennis
    match_tennis_1 = SimpleNamespace(
        list_home_player=["Nadal"], list_away_player=["Federer"]
    )
    match_tennis_2 = SimpleNamespace(
        list_home_player=["Djoko"], list_away_player=["Nadal"]
    )

    stats_tennis = calculer_stats_joueur(
        "Nadal", "tennis", [match_tennis_1, match_tennis_2]
    )

    assert stats_tennis["victoires"] == 1
    assert stats_tennis["defaites"] == 1
    assert stats_tennis["win_rate"] == "50.0%"

    # lol
    match_lol = SimpleNamespace(
        list_home_player=["Fnatic Player"],
        list_away_player=["G2 Player"],
        team_blue="Fnatic",
        winner="Fnatic",
    )

    stats_lol = calculer_stats_joueur("fnatic", "lol", [match_lol])
    assert stats_lol["victoires"] == 1
    assert stats_lol["defaites"] == 0
