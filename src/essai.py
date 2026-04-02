import csv
import os
import pickle

import numpy as np
import pandas as pd
pd.options.display.max_columns = 100

df_match = pd.read_csv("/home/onyxia/work/Projet-1A-2026/data/football_european_leagues_tdd/match.csv")
liste_id_home_player = []
for i in range (1,12):
    col_name = f"home_player_{i}"
    liste_id_home_player.append(int(df_match.loc[173,col_name]))
print(liste_id_home_player)

df_player = pd.read_csv("/home/onyxia/work/Projet-1A-2026/data/football_european_leagues_tdd/player.csv")
liste_nom_home_player = []


for player_id in liste_id_home_player:
    joueur_filtre = df_player.loc[df_player["player_api_id"] == player_id, "player_name"]