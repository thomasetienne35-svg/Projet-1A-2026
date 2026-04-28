import sys
import os
import traceback

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader
# J'adapte l'import selon la structure de tes dossiers vue sur tes captures d'écran
from loaders_player.player_loader import PlayerLoader


def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]
    
    print("Chargement initial de toutes les données en cours... Veuillez patienter.")
    
    # 1. On prépare les dictionnaires pour stocker TOUTES les données
    tous_les_matchs = {}
    tous_les_joueurs = {}
    
    loader_match = MatchLoader()
    
    for nom_sport in sports_disponibles:
        sport_obj = Sport(nom_sport)
        
        # --- A. Chargement des MATCHS ---
        try:
            tous_les_matchs[nom_sport] = loader_match.load_all_matches(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR MATCHS {nom_sport.upper()} ---")
            traceback.print_exc() 
            print("-----------------------------------------\n")
            tous_les_matchs[nom_sport] = []

        # --- B. Chargement des JOUEURS ---
        try:
            # On instancie le loader de joueurs (ta classe attend le sport à l'initialisation)
            loader_player = PlayerLoader(sport_obj)
            # Et ta méthode attend aussi le sport en argument
            tous_les_joueurs[nom_sport] = loader_player.charger_player(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR JOUEURS {nom_sport.upper()} ---")
            traceback.print_exc() 
            print("------------------------------------------\n")
            tous_les_joueurs[nom_sport] = []

    print("\n=== Chargement terminé ! ===")
    
    # Petit résumé pour t'aider à debugger visuellement
    for s in sports_disponibles:
        nb_matchs = len(tous_les_matchs[s])
        nb_joueurs = len(tous_les_joueurs[s])
        print(f"- {s.capitalize():<10} : {nb_matchs} matchs | {nb_joueurs} joueurs")


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

    # 3. Récupération instantanée des matchs depuis le dictionnaire
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