"""Test classe sport."""
import pytest

from src.sport import Sport


def test_sport_creation_valide() -> None:
    """Vérifie qu'on peut créer un sport autorisé."""
    sport = Sport("football")
    assert sport.name == "football"

def test_sport_creation_invalide() -> None:
    """Vérifie que le système rejette un sport non reconnu."""
    with pytest.raises(ValueError, match="Ce sport n'est pas pris en charge"):
        Sport("A")
        