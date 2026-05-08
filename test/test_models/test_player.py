from src.player import Player


def test_player_creation() -> None:
    """Vérifie que le joueur enregistre bien ses attributs."""
    joueur = Player(
        prenom_nom="Zinedine Zidane", 
        nationalite="Française", 
        date_naissance="1972-06-23", 
        genre="Homme", 
        taille=185, 
        poids=80, 
        team="Real Madrid"
    )
    
    assert joueur.prenom_nom == "Zinedine Zidane"
    assert joueur.taille == 185
    assert joueur.nationalite == "Française"