import pandas as pd

class match_par_joueur:
    def get_player_matches(all_matches: list[Match], player_id: int) -> list[Match]:
        """
        Parcourt une liste de matchs et retourne uniquement ceux joués par le joueur.
        """
        # Utilisation d'une compréhension de liste pour un code concis et rapide
        return [match for match in all_matches if match.has_player(player_id)]



def get_id_from_name(df_players: pd.DataFrame, sport: str, prenom: str = "", nom: str = "", nom_complet_ou_pseudo: str = ""):
    """
    Cherche dans le DataFrame des joueurs et renvoie l'identifiant correct 
    en fonction de l'architecture spécifique de la base de données du sport.
    """
    sport = sport.lower()

    try:
        if sport == "basket":
            # Recherche via first_name et last_name -> renvoie person_id
            mask = (df_players['first_name'].str.lower() == prenom.lower()) & \
                   (df_players['last_name'].str.lower() == nom.lower())
            return df_players.loc[mask, 'person_id'].iloc[0]

        elif sport == "tennis":
            # Recherche via name_first et name_last -> renvoie player_id
            mask = (df_players['name_first'].str.lower() == prenom.lower()) & \
                   (df_players['name_last'].str.lower() == nom.lower())
            return df_players.loc[mask, 'player_id'].iloc[0]

        elif sport == "football":
            # Recherche via player_name -> renvoie player_api_id
            mask = (df_players['player_name'].str.lower() == nom_complet_ou_pseudo.lower())
            return df_players.loc[mask, 'player_api_id'].iloc[0]

        elif sport == "lol":
            # Recherche via pseudo -> renvoie le pseudo lui-même (qui sert d'ID)
            mask = (df_players['pseudo'].str.lower() == nom_complet_ou_pseudo.lower())
            return df_players.loc[mask, 'pseudo'].iloc[0]
            
        elif sport in ["volley", "volleyball"]:
            # Recherche via name -> renvoie le nom (la table volley n'a pas d'ID entier explicite)
            mask = (df_players['name'].str.lower() == nom_complet_ou_pseudo.lower())
            return df_players.loc[mask, 'name'].iloc[0]

        else:
            print(f"Sport '{sport}' non reconnu.")
            return None

    except IndexError:
        # Si le masque ne trouve rien, .iloc[0] va lever une IndexError
        print("Joueur introuvable dans la base de données.")
        return None
