class Sport:
    """Modèle de données contenant l'ensemble des noms des sports.
    """
    def __init__(self, name) -> None:
        if name not in ["football", "tennis", "volley", "basketball", "lol"]:
            raise ValueError("Ce sport n'est pas pris en charge")
        self.name = name
