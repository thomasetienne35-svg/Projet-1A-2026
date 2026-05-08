import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from src.match import Match
from src.sport import Sport


def test_match_has_player() -> None:
    """Vérifie que la méthode trouve bien les joueurs à domicile et à l'extérieur."""
    tennis = Sport("tennis")
    match = Match(
        id=101, sport=tennis, list_home_player=[10, 11], list_away_player=[20, 21]
    )

    assert match.has_player(10) is True
    assert match.has_player(21) is True
    assert match.has_player(99) is False
