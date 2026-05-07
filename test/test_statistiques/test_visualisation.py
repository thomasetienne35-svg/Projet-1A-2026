import os
from pathlib import Path

from src.statistiques.visualisation import (
    afficher_comparateur_equipes,
    afficher_comparateur_joueurs,
)


def test_comparateur_joueurs_genere_image(tmp_path: Path) -> None:
    """Vérifie que le graphique de comparaison des joueurs est bien créé.

    Parameters
    ----------
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    os.chdir(tmp_path)
    
    joueur_1 = {"joueur": "Federer", "sport": "Tennis", "matchs_joues": 10, 
                "victoires": 8, "defaites": 2, "win_rate": "80%"}
    joueur_2 = {"joueur": "Nadal", "sport": "Tennis", "matchs_joues": 10, 
                "victoires": 7, "defaites": 3, "win_rate": "70%"}
    
    afficher_comparateur_joueurs(joueur_1, joueur_2)
    
    assert os.path.exists("comparaison_joueurs.png")


def test_comparateur_equipes_genere_image(tmp_path: Path) -> None:
    """Vérifie que le graphique de comparaison des équipes est bien créé.

    Parameters
    ----------
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    os.chdir(tmp_path)
    
    equipe_1 = {"equipe": "PSG", "matchs_joues": 5, "victoires": 4, "defaites": 1, 
                "buts_marques": 12, "buts_encaisses": 4}
    equipe_2 = {"equipe": "OM", "matchs_joues": 5, "victoires": 2, "defaites": 3, 
                "buts_marques": 6, "buts_encaisses": 8}
    
    afficher_comparateur_equipes(equipe_1, equipe_2)
    
    assert os.path.exists("comparaison_equipes.png")