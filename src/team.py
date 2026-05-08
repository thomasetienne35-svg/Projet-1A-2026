class Team:
    """Modèle de données représentant un joueur."""

    def __init__(self, team_id, name, short_name) -> None:
        """Initialise la classe."""
        self.id = team_id
        self.name = name
        self.short_name = short_name
