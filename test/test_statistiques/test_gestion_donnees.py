from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd

from src.statistiques.gestion_donnees import DataUpdater


def test_mettre_a_jour_tout_joueurs_et_matchs(tmp_path: Path) -> None:
    """Vérifie que les matchs sont ajoutés et les joueurs mis à jour sans doublons.

    Parameters
    ----------
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    faux_sport = SimpleNamespace(name="tennis")
    updater = DataUpdater(sport_obj=faux_sport)

    fichier_matchs = tmp_path / "matchs_actuels.csv"
    fichier_matchs.write_text("id,score\n1,3-0\n")
    
    fichier_joueurs = tmp_path / "joueurs_actuels.csv"
    fichier_joueurs.write_text("player_name,age,taille\nFederer,41,185\nNadal,36,185\n")

    updater.path_matches = str(fichier_matchs)
    updater.path_players = str(fichier_joueurs)

    nouveaux_matchs = tmp_path / "new_matchs.csv"
    nouveaux_matchs.write_text("id,score\n2,2-1\n") 
    
    nouveaux_joueurs = tmp_path / "new_joueurs.csv"
    nouveaux_joueurs.write_text("player_name,age,taille\nNadal,37,185\nAlcaraz,20,183\n")

    updater.mettre_a_jour_tout(
        chemin_nouveaux_matchs=str(nouveaux_matchs),
        chemin_nouveaux_joueurs=str(nouveaux_joueurs)
    )
    df_matchs = pd.read_csv(fichier_matchs)
    assert len(df_matchs) == 2
    assert df_matchs.iloc[1]['score'] == "2-1" 
  
    df_joueurs = pd.read_csv(fichier_joueurs)
    assert len(df_joueurs) == 3 

    age_nadal = df_joueurs.loc[df_joueurs['player_name'] == 'Nadal', 'age'].values[0]
    assert age_nadal == 37
    
    assert "Alcaraz" in df_joueurs['player_name'].values


@patch('builtins.input')
def test_editer_joueur_manuellement_succes(mock_input: MagicMock, 
                                           tmp_path: Path) -> None:
    """Simule une modification avec succès d'un joueur via la console.

    Parameters
    ----------
    mock_input : MagicMock
        Objet de simulation remplaçant la fonction native 'input' pour injecter 
        automatiquement des réponses clavier durant le test.
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    faux_sport = SimpleNamespace(name="basketball")
    updater = DataUpdater(sport_obj=faux_sport)
    
    fichier_csv = tmp_path / "basket_players.csv"
    fichier_csv.write_text("player_name,points_par_match\nLebron,25.0\nCurry,29.0\n")
    
    mock_input.side_effect = [
        str(fichier_csv),     
        "Lebron",             
        "0",                  
        "points_par_match",  
        "27.5"               
    ]
    
    resultat = updater.editer_joueur_manuellement()
    assert resultat is True
    df = pd.read_csv(fichier_csv)
    assert df.loc[0, 'points_par_match'] == 27.5


@patch('builtins.input')
def test_editer_equipe_manuellement_succes(mock_input: MagicMock, 
                                           tmp_path: Path) -> None:
    """Simule une modification avec succès d'une équipe via la console.

    Parameters
    ----------
    mock_input : MagicMock
        Objet de simulation remplaçant la fonction native 'input' pour injecter 
        automatiquement des réponses clavier durant le test.
    tmp_path : Path
        Chemin vers un répertoire temporaire unique à cette exécution de test.
    """
    faux_sport = SimpleNamespace(name="football")
    updater = DataUpdater(sport_obj=faux_sport)
    
    fichier_csv = tmp_path / "foot_teams.csv"
    fichier_csv.write_text("team_id,team_name,stade\n101,Paris SG,Parc\n102,Marseille,Velodrome\n")

    mock_input.side_effect = [
        str(fichier_csv),    
        "Paris SG",          
        "0",                 
        "stade",             
        "Parc des Princes"    
    ]
    
    resultat = updater.editer_equipe_manuellement()
    
    assert resultat is True
    df = pd.read_csv(fichier_csv)
    assert df.loc[0, 'stade'] == "Parc des Princes"


@patch('builtins.input')
def test_editer_joueur_fichier_introuvable(mock_input: MagicMock) -> None:
    """Vérifie que la fonction s'arrête si on se trompe de chemin.

    Parameters
    ----------
    mock_input : MagicMock
        Objet de simulation remplaçant la fonction native 'input' pour injecter 
        automatiquement des réponses clavier durant le test.
    """
    faux_sport = SimpleNamespace(name="tennis")
    updater = DataUpdater(sport_obj=faux_sport)
    
    mock_input.side_effect = ["/chemin/totalement/invente/qui/n_existe_pas.csv"]
    
    resultat = updater.editer_joueur_manuellement()
    assert resultat is False