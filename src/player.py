import csv
import os
import pickle

import numpy as np
import pandas as pd

pd.options.display.max_columns = 100


class Player:
    def __init__(
        self, prenom_nom, nationalite, date_naissance, genre, taille, poids, team
    ) -> None:
        self.prenom_nom = prenom_nom
        self.nationalite = nationalite
        self.date_naissance = date_naissance
        self.genre = genre
        self.taille = taille
        self.poids = poids
        self.team = team
        