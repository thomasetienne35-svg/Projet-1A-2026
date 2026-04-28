import sys
import os
import traceback

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader
from loaders_player.player_loader import PlayerLoader
# Import générique du TeamLoader
from loaders_team.team_loader import TeamLoader
from statistiques.nbre_de_points import ChampionshipPointsCalculator


def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]
    
    print("Chargement initial de toutes les données en cours... Veuillez patienter.")
    
    tous_les_matchs = {}
    tous_les_joueurs = {}
    toutes_les_equipes = {}
    
    # Instanciation de tes chargeurs génériques
    loader_match = MatchLoader()
    loader_team = TeamLoader() 
    
    for nom_sport in sports_disponibles:
        sport_obj = Sport(nom_sport)
        
        # --- A. Chargement des MATCHS ---
        try:
            tous_les_matchs[nom_sport] = loader_match.load_all_matches(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR MATCHS {nom_sport.upper()} ---")
            tous_les_matchs[nom_sport] = []

        # --- B. Chargement des JOUEURS ---
        try:
            loader_player = PlayerLoader(sport_obj)
            tous_les_joueurs[nom_sport] = loader_player.charger_player(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR JOUEURS {nom_sport.upper()} ---")
            tous_les_joueurs[nom_sport] = []

        # --- C. Chargement des ÉQUIPES ---
        try:
            # Appel générique : on passe sport_obj comme pour les autres loaders
            toutes_les_equipes[nom_sport] = loader_team.load_all_teams(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR ÉQUIPES {nom_sport.upper()} ---")
            toutes_les_equipes[nom_sport] = []

    print("\n=== Chargement terminé ! ===")
    
    for s in sports_disponibles:
        nb_matchs = len(tous_les_matchs[s])
        nb_joueurs = len(tous_les_joueurs[s])
        nb_equipes = len(toutes_les_equipes[s])
        print(f"- {s.capitalize():<10} : {nb_matchs} matchs | {nb_joueurs} joueurs | {nb_equipes} équipes")

    # =========================================================
    # BOUCLE PRINCIPALE : Navigation entre les sports
    # =========================================================
    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL : SPORTS ===")
        print("="*30)
        for i, s in enumerate(sports_disponibles, 1):
            print(f"{i}. {s.capitalize()}")
        print("0. Quitter le programme")

        choix = input("\nEntrez le numéro du sport (ou 0 pour quitter) : ")
        
        if choix == "0":
            print("\nMerci d'avoir utilisé le programme. À bientôt !")
            break 
            
        try:
            nom_sport_choisi = sports_disponibles[int(choix) - 1]
            sport = Sport(nom_sport_choisi)
        except (ValueError, IndexError):
            print("\n/!\\ Choix invalide. Veuillez réessayer.")
            continue

        matchs = tous_les_matchs[nom_sport_choisi]
        if not matchs:
            print(f"\nAucun match disponible pour le {sport.name}.")
            input("\nAppuyez sur Entrée pour revenir au menu...")
            continue

        # =========================================================
        # BOUCLE SECONDAIRE : Actions pour le sport choisi
        # =========================================================
        while True:
            print("\n" + "-"*40)
            print(f"=== Actions pour {nom_sport_choisi.capitalize()} ===")
            print("1. Consulter les détails d'un match précis")
            print("2. Consulter les statistiques d'une équipe")
            print("3. Retourner au choix des sports")
            
            choix_action = input("\nQue voulez-vous faire (1, 2 ou 3) ? ")

            if choix_action == "3":
                break

            # ---------------------------------------------------------
            # ACTION 1 : DÉTAILS DU MATCH
            # ---------------------------------------------------------
            elif choix_action == "1":
                choix_match = input(f"\nEntrez le numéro du match (1 à {len(matchs)}) : ")
                try:
                    match = matchs[int(choix_match) - 1]
                    print(f"\n=== Match ID: {match.id} ===")
                    print(f"Sport : {match.sport}")
                    print(f"Joueurs domicile : {[str(j) for j in match.list_home_player]}")
                    print(f"Joueurs extérieur : {[str(j) for j in match.list_away_player]}")
                except (ValueError, IndexError):
                    print("\n/!\\ Match invalide.")

            # ---------------------------------------------------------
            # ACTION 2 : STATISTIQUES D'UNE ÉQUIPE
            # ---------------------------------------------------------
            elif choix_action == "2":
                calculateur = ChampionshipPointsCalculator(
                    sport_name=nom_sport_choisi,
                    matches_df=None, 
                    liste_equipes_foot=toutes_les_equipes[nom_sport_choisi],
                    liste_matchs_foot=matchs
                )

                try:
                    saisons_dispo = calculateur.get_available_seasons()
                    if saisons_dispo:
                        print(f"\nSaisons disponibles : {', '.join(saisons_dispo)}")
                    else:
                        print("\nAucune information de saison trouvée dans ces matchs.")

                    nom_equipe = input("\nEntrez le nom de l'équipe : ")
                    saison_choisie = input("Entrez la saison (ex: 2008/2009) ou appuyez sur Entrée pour toutes les saisons : ")
                    
                    if not saison_choisie.strip():
                        saison_choisie = None

                    resultat = calculateur.get_team_points(nom_equipe, saison_choisie)

                    if isinstance(resultat, str):
                        print(f"\n{resultat}")
                    else:
                        print(f"\n=== Statistiques de {resultat['equipe']} ===")
                        for cle, valeur in resultat.items():
                            nom_propre = cle.replace("_", " ").capitalize()
                            print(f"{nom_propre} : {valeur}")

                except NotImplementedError as e:
                    print(f"\nInformation : {e}")
                except Exception as e:
                    print(f"\nErreur inattendue lors du calcul : {e}")

            else:
                print("\n/!\\ Action non reconnue. Veuillez réessayer.")
            
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()