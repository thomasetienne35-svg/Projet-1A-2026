import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.statistiques.statistiques_physiologie import AnalysePhysiologique


def test_extraire_tailles_conversions() -> None:
    """Vérifie que le traducteur transforme bien tous les formats en cm."""
    p1 = SimpleNamespace(height="6-0")
    p2 = SimpleNamespace(taille="1.90")
    p3 = SimpleNamespace(size="70")

    analyse = AnalysePhysiologique(liste_joueurs=[p1, p2, p3], sport="basket")

    tailles = analyse._extraire_tailles()

    assert len(tailles) == 3
    assert 182 < tailles[0] < 183
    assert tailles[1] == 190.0
    assert 177 < tailles[2] < 178


def test_generer_graphique_cree_fichier(tmp_path: Path) -> None:
    """Vérifie que le code crée bien un fichier image .png."""
    os.chdir(tmp_path)

    p = SimpleNamespace(height=180)

    faux_sport = SimpleNamespace(name="tennis")
    analyse = AnalysePhysiologique(liste_joueurs=[p], sport=faux_sport)

    analyse.generer_graphique_taille()
    nom_attendu = "distribution_taille_tennis.png"

    assert os.path.exists(nom_attendu)


def test_heatmap_pas_assez_de_donnees(capsys: pytest.CaptureFixture[str]) -> None:
    """Vérifie que le code prévient s'il n'y a pas assez de données."""
    p = SimpleNamespace(prenom_nom="Petit Joueur", height=170)

    m = SimpleNamespace(
        list_home_player=["Petit Joueur"],
        list_away_player=[],
        home_team_score=1,
        away_team_score=0,
        team_blue="Vide",
        winner="Vide",
    )

    faux_sport = SimpleNamespace(name="foot")
    analyse = AnalysePhysiologique(liste_joueurs=[p], sport=faux_sport)

    analyse.generer_heatmap_taille_victoire(matchs=[m])

    capture = capsys.readouterr()
    assert "Pas assez de données" in capture.out
