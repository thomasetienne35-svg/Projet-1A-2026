import csv
import os
import pickle

import numpy as np
import pandas as pd

pd.options.display.max_columns = 100


class Player:
    def __init__(
<<<<<<< HEAD
        self, prenom_nom, nationalite, date_naissance, genre, taille, poids, team
=======
        self, prenom_nom, nationalite, date_naissance, genre, taille, poids, team_id
>>>>>>> 4afc8a17d8eef91bc36d3062ae95ffae9cbb771e
    ) -> None:
        self.prenom_nom = prenom_nom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.genre = genre
        self.taille = taille
        self.poids = poids
<<<<<<< HEAD
        self.team_id = team
=======
        self.team_id = team_id
>>>>>>> 4afc8a17d8eef91bc36d3062ae95ffae9cbb771e
