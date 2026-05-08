class Player:
    """Modèle de données représentant un joueur."""

    def __init__(
        self, prenom_nom, nationalite, date_naissance, genre, taille, poids, team
    ) -> None:
        """Initialise la classe."""
        self.prenom_nom = prenom_nom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.genre = genre
        self.taille = taille
        self.poids = poids
        self.team = team
