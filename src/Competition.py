from Date import date


class Compétition:
    def __init__(
        self, id_compet: int, nom: str, date_debut: date, dateFin: date, lieu: str
    ) -> None:
        if not isinstance(id_compet, int):
            raise ValueError("L'identifiant doit être un entier")
        else:
            self.id_compet = id_compet

        if not isinstance(nom, str):
            raise ValueError("Le nom doit être une chaîne de caractères")
        else:
            self.nom = nom

        if not isinstance(lieu, str):
            raise ValueError("Le lieu doit être une chaîne de caractères")
        else:
            self.lieu = lieu

        if not isinstance(date_debut, date):
            raise ValueError("Rentrer une date")
        else:
            self.date_debut = date_debut

        if not isinstance(dateFin, date):
            raise ValueError("Rentrer une date")
        else:
            self.dateFin = dateFin

    def ajouter_epreuve(epreuve: epreuve) -> None:
        
