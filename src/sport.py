class Sport:
    """Modèle de données contenant l'ensemble des noms des sports."""

    def __init__(self, name) -> None:
        """Initialise la classe."""
        if name not in ["football", "tennis", "volley", "basketball", "lol"]:
            raise ValueError("Ce sport n'est pas pris en charge")
        self.name = name
