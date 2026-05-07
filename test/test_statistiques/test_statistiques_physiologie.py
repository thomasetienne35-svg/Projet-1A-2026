import os
from types import SimpleNamespace
from src.statistiques.statistiques_physiologie import AnalysePhysiologique
from pathlib import Path


def test_extraire_tailles_conversions() -> None:
    """Vérifie que le traducteur transforme bien tous les formats en cm.
    """
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
    """Vérifie que le code crée bien un fichier image .png.

    Parameters
    ----------
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    os.chdir(tmp_path)
    
    p = SimpleNamespace(height=180)
    analyse = AnalysePhysiologique(liste_joueurs=[p], sport="tennis")
    
    analyse.generer_graphique_taille()
    nom_attendu = "distribution_taille_tennis.png"
    
    assert os.path.exists(nom_attendu)


def test_heatmap_pas_assez_de_donnees() -> None:
    """Vérifie que le code prévient s'il n'y a pas assez de données.
    """
    p = SimpleNamespace(prenom_nom="Petit Joueur", height=170)
    m = SimpleNamespace(list_home_player=["Petit Joueur"], home_team_score=1, away_team_score=0)
    
    analyse = AnalysePhysiologique(liste_joueurs=[p], sport="foot")
    analyse.generer_heatmap_taille_victoire(matchs=[m])
    
    assert "Pas assez de données croisées (Taille + Minimum 3 matchs joués) pour générer la Heatmap"