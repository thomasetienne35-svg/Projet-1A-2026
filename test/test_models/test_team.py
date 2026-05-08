from src.team import Team


def test_team_creation() -> None:
    """Vérifie que l'équipe enregistre bien ses attributs."""
    equipe = Team(team_id=1, name="Paris Saint-Germain", short_name="PSG")

    assert equipe.id == 1
    assert equipe.name == "Paris Saint-Germain"
    assert equipe.short_name == "PSG"
