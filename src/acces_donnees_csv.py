import csv
import os
import pickle

import numpy as np
import pandas as pd
pd.options.display.max_columns = 100

df_match = pd.read_csv("/home/onyxia/work/Projet-1A-2026/data/football_european_leagues_tdd/match.csv")
valeur = df_match.loc[173,"home_team_api_id"]


df_joueur = pd.read_csv("/home/onyxia/work/Projet-1A-2026/data/football_european_leagues_tdd/player.csv")

home_team_joueur = []
for i in range (12):
    home_team_joueur.append(df_joueur.loc[valeur,"player_name"])

print(home_team_joueur)