import sys
import os

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader


def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]
    # il reste à charger les données de player et team
    print("Chargement initial de toutes les données en cours... Veuillez patienter.")
    
    # 1. On charge TOUS les matchs de TOUS les sports dès le début
    tous_les_matchs = {}
    loader = MatchLoader()
    
    for nom_sport in sports_disponibles:
        try:
            sport_obj = Sport(nom_sport)
            tous_les_matchs[nom_sport] = loader.load_all_matches(sport_obj)
        except Exception as e:
            print(f"Avertissement : Impossible de charger les données pour {nom_sport} ({e})")
            tous_les_matchs[nom_sport] = [] # On initialise une liste vide si le chargement échoue

    print("\n=== Chargement terminé ! ===")

    # 2. Affichage et choix du sport par l'utilisateur
    print("\n=== Sports disponibles ===")
    for i, s in enumerate(sports_disponibles, 1):
        print(f"{i}. {s}")

    choix = input("\nEntrez le numéro du sport : ")
    try:
        nom_sport_choisi = sports_disponibles[int(choix) - 1]
        sport = Sport(nom_sport_choisi)
    except (ValueError, IndexError):
        print("Sport invalide.")
        return

    # 3. Récupération instantanée des matchs depuis le dictionnaire (pas de nouveau chargement)
    matchs = tous_les_matchs[nom_sport_choisi]
    
    if not matchs:
        print(f"\nAucun match disponible pour {sport.name}.")
        return

    # 4. Choix du match
    choix_match = input(f"\nEntrez le numéro du match (1 à {len(matchs)}) : ")
    try:
        match = matchs[int(choix_match) - 1]
    except (ValueError, IndexError):
        print("Match invalide.")
        return

    # 5. Affichage des résultats
    print(f"\n=== Match ID: {match.id} ===")
    print(f"Sport : {match.sport}")
    print(f"Joueurs domicile : {[str(j) for j in match.list_home_player]}")
    print(f"Joueurs extérieur : {[str(j) for j in match.list_away_player]}")


if __name__ == "__main__":
    main()