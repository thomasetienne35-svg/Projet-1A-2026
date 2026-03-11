class Participant:
    def __init__(self, id_participant: int, nom: str, prenom: str, nationalite: str) -> None:
        if not isinstance(id_participant, int):
            raise ValueError("L'id du participant doit être un int")
        else:
            self.id_participant = id_participant
        if not isinstance(nom, str):
            raise ValueError("Le nom doit être un str")
        else:
            self.nom = nom
        if not isinstance(prenom, str):
            raise ValueError("Le nom doit être un str")
        else:
            self.prenom = prenom
        