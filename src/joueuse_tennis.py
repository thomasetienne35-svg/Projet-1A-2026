import csv
import os
import pickle

import numpy as np
import pandas as pd
pd.options.display.max_columns = 100

path = os.path.join("datasets", "tennis")

df_player = pd.read_csv(os.path.join(path, "wta_players_2024.csv"))
df_player.head(2)

df_player.isna().any(axis=0)

import datetime


class Player:
    def __init__(
        self,
        lastname: str,
        firstname: str,
        birthdate: datetime.date | None,
        country: str,
        hand: str,
        height: int | None
    ) -> None:
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.country = country
        self.hand = hand
        self.height = height
        self.statistiques = {}
            
    def ajouter_statistiques(self, annee: str, statistiques: dict) -> None:
        self.statistiques[annee] = statistiques

df_match = pd.read_csv(os.path.join(path, "wta_matches_2024.csv"))
df_match.head()

def calculer_nombre_tournois_gagnes() -> pd.Series:
    # Récupération de toutes les joueuses
    players = pd.concat([df_match["winner_id"], df_match["loser_id"]]).unique()

    # Initialisation du résultat renvoyé : 0 tournoi gagné pour chaque joueuse
    res = pd.Series(data=0, index=players, name="n_tournaments_won")

    # Calcul du nombre de tournois gagnés pour les joueuses ayant gagné au moins 1 tournoi
    winners = (
        df_match
        .loc[df_match["round"] == "F", ["winner_id", "tourney_id"]]
        .groupby("winner_id")["tourney_id"].nunique()
    )

    # Mise à jour du résultat renvoyé
    res.loc[winners.index] = winners

    # Renvoi du résultat
    return res

def calculer_taux_victoires() -> pd.Series:
    # Récupérer toutes les joueuses
    players = pd.concat([df_match["winner_id"], df_match["loser_id"]]).unique()

    # Initialisation du nombre de vcitoires et de défaites par joueuse à 0
    wins = pd.Series(data=0, index=players)
    losses = pd.Series(data=0, index=players)
    
    # Calcul du nombre de victoires et de défaites par joueuse
    wins_actual = df_match["winner_id"].value_counts()
    losses_actual = df_match["loser_id"].value_counts()
    
    # Mise à jour des objets initiaux
    wins.loc[wins_actual.index] = wins_actual
    losses.loc[losses_actual.index] = losses_actual
    
    # Renvoi du résultat
    res = wins / (wins + losses)
    res.name = "winning_ratio"
    return res

def calculer_meilleur_resultat_grand_chelem() -> pd.Series:
    # Initialisation du résultat renvoyé
    players = pd.concat([df_match["winner_id"], df_match["loser_id"]]).unique()
    res = pd.Series(data=None, index=players, dtype=str, name="best_grand_chelem_result")
    
    # Sélection des matchs en grand chelem
    df_match_g = df_match[df_match["tourney_level"] == "G"].copy()
    
    # Correspondances entre les tours et leurs niveaux
    mapping_round_int = {"R128": 0, "R64": 1, "R32": 2, "R16": 3, "QF": 4, "SF": 5, "F": 6}
    mapping_int_round = {value: key for key, value in mapping_round_int.items()}
    
    # Création d'une variable temporaire pour ordonner les tours
    df_match_g["round_int"] = df_match_g["round"].map(mapping_round_int)
    
    # Récupération du meilleur résultat pour les joueuses ayant participé à un grand chelem
    # (hors victoire d'un tournoi)
    best_results = (
        df_match_g[df_match_g["tourney_level"] == "G"]
        .groupby("loser_id")["round_int"].max()
        .map(mapping_int_round)
    )

    # Récupération des vainqueuses des tournois du grand chelem
    winners = df_match_g.loc[df_match_g["round"] == "F", "winner_id"].to_numpy()

    # Mise à jour du résultat renvoyé
    res.loc[best_results.index] = best_results
    res.loc[winners] = "W"

    # Renvoi du résultat
    return res

def creer_objets_joueuses() -> dict[int, Player]:
    df_player = pd.read_csv(os.path.join(path, "wta_players_2024.csv"))
    df_match = pd.read_csv(os.path.join(path, "wta_matches_2024.csv"))
    
    df_statistics = pd.concat([
        calculer_nombre_tournois_gagnes(),
        calculer_taux_victoires(),
        calculer_meilleur_resultat_grand_chelem(),
    ], axis=1)
    
    mapping_hand = {"L": "gauche", "R": "droite", "U": "inconnue"}
    
    res = {}
    for record in df_player.to_dict("records"):
        
        # Date de naissance
        if not np.isnan(record["dob"]):
            birthdate = datetime.datetime.strptime(f"{record["dob"]:.0f}", "%Y%m%d")
            birthdate = datetime.date(birthdate.year, birthdate.month, birthdate.day)
        else:
            birthdate = None
        
        # Taille
        height = int(record["height"]) if not np.isnan(record["height"]) else None

        res[record["player_id"]] = Player(
            lastname=record["name_first"],
            firstname=record["name_last"],
            birthdate=birthdate,
            country=record["ioc"],
            hand=mapping_hand[record["hand"]],
            height=height,
        )
        
        res[record["player_id"]]

    dict_statistics = df_statistics.to_dict("index")
    for key, value in dict_statistics.items():
        res[key].ajouter_statistiques(2024, value)

    return res

if not os.path.isdir(os.path.join("objets", "tennis")):
    os.makedirs(os.path.join("objets", "tennis"))

with open(os.path.join("objets", "tennis", "wta_players_2024.p"), 'wb') as fp:
    pickle.dump(creer_objets_joueuses(), fp)