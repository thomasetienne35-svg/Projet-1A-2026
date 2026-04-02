import csv
import os
import pickle

import numpy as np
import pandas as pd
pd.options.display.max_columns = 100

class Player:
    def __init__(self, age, taille, date_naissance):
        df_player = pd.read_csv(os.path.join(path, "wta_players_2024.csv"))