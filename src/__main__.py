import sys
import os
import traceback

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader
from loaders_player.player_loader import PlayerLoader
# Import de ta nouvelle classe
from statistiques.nbre_de_points import ChampionshipPointsCalculator


def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]
    
    print("Chargement initial de toutes les données en cours... Veuillez patienter.")
    
    # 1. On prépare les dictionnaires pour stocker TOUTES les données
    tous_les_matchs = {}
    tous_les_joueurs = {}
    
    # TODO: Ajouter plus tard le chargement des équipes ici !
    toutes_les_equipes = {s: [] for s in sports_disponibles} 
    
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
            loader_player = PlayerLoader(sport_obj)
            tous_les_joueurs[nom_sport] = loader_player.charger_player(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR JOUEURS {nom_sport.upper()} ---")
            traceback.print_exc() 
            print("------------------------------------------\n")
            tous_les_joueurs[nom_sport] = []

    print("\n=== Chargement terminé ! ===")
    
    for s in sports_disponibles:
        nb_matchs = len(tous_les_matchs[s])
        nb_joueurs = len(tous_les_joueurs[s])
        print(f"- {s.capitalize():<10} : {nb_matchs} matchs | {nb_joueurs} joueurs")

    # 2. Choix du sport par l'utilisateur
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

    matchs = tous_les_matchs[nom_sport_choisi]
    if not matchs:
        print(f"\nAucun match disponible pour {sport.name}.")
        return

    # 3. NOUVEAU MENU : Choix de l'action
    print(f"\n=== Actions pour {nom_sport_choisi.capitalize()} ===")
    print("1. Consulter les détails d'un match précis")
    print("2. Consulter les statistiques d'une équipe")
    
    choix_action = input("\nQue voulez-vous faire (1 ou 2) ? ")

    # ---------------------------------------------------------
    # ACTION 1 : DÉTAILS DU MATCH (Ton ancien code)
    # ---------------------------------------------------------
    if choix_action == "1":
        choix_match = input(f"\nEntrez le numéro du match (1 à {len(matchs)}) : ")
        try:
            match = matchs[int(choix_match) - 1]
        except (ValueError, IndexError):
            print("Match invalide.")
            return

        print(f"\n=== Match ID: {match.id} ===")
        print(f"Sport : {match.sport}")
        print(f"Joueurs domicile : {[str(j) for j in match.list_home_player]}")
        print(f"Joueurs extérieur : {[str(j) for j in match.list_away_player]}")

    # ---------------------------------------------------------
    # ACTION 2 : STATISTIQUES D'UNE ÉQUIPE (Nouveau code)
    # ---------------------------------------------------------
    elif choix_action == "2":
        # Instanciation du calculateur
        # Note : On passe "None" pour le DataFrame car il n'est pas utilisé pour le football
        calculateur = ChampionshipPointsCalculator(
            sport_name=nom_sport_choisi,
            matches_df=None, 
            liste_equipes_foot=toutes_les_equipes[nom_sport_choisi],
            liste_matchs_foot=matchs
        )

        try:
            # Affichage des saisons dispo pour aider l'utilisateur
            saisons_dispo = calculateur.get_available_seasons()
            if saisons_dispo:
                print(f"\nSaisons disponibles : {', '.join(saisons_dispo)}")
            else:
                print("\nAucune information de saison trouvée dans ces matchs.")

            nom_equipe = input("\nEntrez le nom de l'équipe : ")
            saison_choisie = input("Entrez la saison (ex: 2008/2009) ou appuyez sur Entrée pour toutes les saisons : ")
            
            if not saison_choisie.strip():
                saison_choisie = None

            # Appel de la méthode d'aiguillage
            resultat = calculateur.get_team_points(nom_equipe, saison_choisie)

            # Affichage du résultat (gestion de l'erreur String ou du succès Dict)
            if isinstance(resultat, str):
                print(f"\n{resultat}")
            else:
                print(f"\n=== Statistiques de {resultat['equipe']} ===")
                for cle, valeur in resultat.items():
                    # Formatage esthétique des clés (ex: "victoires_domicile" -> "Victoires domicile")
                    nom_propre = cle.replace("_", " ").capitalize()
                    print(f"{nom_propre} : {valeur}")

        except NotImplementedError as e:
            print(f"\nInformation : {e}")
        except Exception as e:
            print(f"\nErreur inattendue lors du calcul : {e}")

    else:
        print("Action non reconnue. Fin du programme.")


if __name__ == "__main__":
    main()