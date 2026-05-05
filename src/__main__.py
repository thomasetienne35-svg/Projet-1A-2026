import sys
import os

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader
from loaders_player.player_loader import PlayerLoader
from loaders_team.team_loader import TeamLoader
from statistiques.nbre_de_points import ChampionshipPointsCalculator
from statistiques.match_par_joueur import calculer_stats_joueur  # <-- NOUVEL IMPORT ICI

def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]
    
    print("Chargement initial des données... Veuillez patienter.")
    
    tous_les_matchs = {}
    tous_les_joueurs = {}
    toutes_les_equipes = {}
    
    loader_match = MatchLoader()
    loader_team = TeamLoader() 
    
    for nom_sport in sports_disponibles:
        sport_obj = Sport(nom_sport)
        try:
            tous_les_matchs[nom_sport] = loader_match.load_all_matches(sport_obj)
            loader_player = PlayerLoader(sport_obj)
            tous_les_joueurs[nom_sport] = loader_player.charger_player(sport_obj)
            toutes_les_equipes[nom_sport] = loader_team.load_all_teams(sport_obj)
        except Exception as e:
            print(f"\n--- ERREUR CRITIQUE SUR {nom_sport.upper()} : {e} ---")
            tous_les_matchs[nom_sport] = []
            tous_les_joueurs[nom_sport] = []
            toutes_les_equipes[nom_sport] = []

    print("\n=== Chargement terminé ! ===")
    
    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL : SPORTS ===")
        print("="*30)
        for i, s in enumerate(sports_disponibles, 1):
            print(f"{i}. {s.capitalize()}")
        print("0. Quitter le programme")

        choix = input("\nEntrez le numéro du sport (ou 0 pour quitter) : ")
        if choix == "0": break
            
        try:
            nom_sport_choisi = sports_disponibles[int(choix) - 1]
        except (ValueError, IndexError):
            print("\n/!\\ Choix invalide.")
            continue

        matchs = tous_les_matchs[nom_sport_choisi]
        if not matchs:
            print(f"\nAucun match disponible pour {nom_sport_choisi}.")
            continue

        while True:
            print("\n" + "-"*40)
            print(f"=== Actions pour {nom_sport_choisi.capitalize()} ===")
            print("1. Consulter les détails d'un match précis")
            print("2. Consulter les statistiques d'une équipe")
            print("3. Consulter les statistiques d'un joueur")
            print("4. Retourner au choix des sports")
            
            choix_action = input("\nVotre choix (1, 2, 3 ou 4) ? (0 pour quitter) : ")

            if choix_action == "0": return
            if choix_action == "4": break

            # --- ACTION 1 : DÉTAILS ---
            if choix_action == "1":
                choix_match = input(f"Entrez le numéro du match (1 à {len(matchs)}) : ")
                try:
                    m = matchs[int(choix_match) - 1]
                    print(f"\n=== Match {m.id} ===\nSport: {m.sport}\nHome: {m.list_home_player}\nAway: {m.list_away_player}")
                except: print("Match invalide.")

            # --- ACTION 2 : STATISTIQUES ÉQUIPE ---
            elif choix_action == "2":
                genre_choisi = None
                if nom_sport_choisi == "volley":
                    print("\n1. Hommes\n2. Femmes")
                    genre_choisi = "Homme" if input("Catégorie (1 ou 2) : ") == "1" else "Femme"

                calculateur = ChampionshipPointsCalculator(
                    sport_name=nom_sport_choisi,
                    matches_df=None,
                    liste_equipes_foot=toutes_les_equipes[nom_sport_choisi],
                    liste_matchs_foot=matchs
                )

                try:
                    nom_equipe = input("\nEntrez le nom de l'équipe (ex: France, Lakers...) : ")
                    if nom_equipe == "0": return

                    saison_choisie = None
                    saisons_dispo = sorted(list(calculateur.get_available_seasons()))
                    
                    if saisons_dispo:
                        print("\nSaisons/Tournois disponibles :")
                        for idx, s in enumerate(saisons_dispo, 1):
                            print(f"{idx}. {s}")
                        print("0. Toutes les saisons")
                        
                        choix_s = input("\nChoisissez le numéro de la saison : ")
                        if choix_s == "0" or not choix_s.strip():
                            saison_choisie = None
                        else:
                            try:
                                saison_choisie = saisons_dispo[int(choix_s) - 1]
                            except:
                                print("Choix invalide, calcul sur tout.")
                                saison_choisie = None

                    resultat = calculateur.get_team_points(nom_equipe, saison_choisie, genre=genre_choisi)
                    
                    if isinstance(resultat, str):
                        print(f"\n{resultat}")
                    else:
                        print(f"\n=== BILAN : {resultat['equipe']} ===")
                        for k, v in resultat.items():
                            print(f"{k.replace('_', ' ').capitalize()} : {v}")

                except Exception as e:
                    print(f"\nErreur : {e}")
            
            # --- ACTION 3 : STATISTIQUES JOUEUR ---
            elif choix_action == "3":
                nom_joueur = input("\nEntrez le nom ou prénom du joueur (ex: Jannik Sinner, Faker) : ")
                if nom_joueur == "0": return
                
                resultat_joueur = calculer_stats_joueur(nom_joueur, nom_sport_choisi, matchs)
                
                if isinstance(resultat_joueur, str):
                    print(f"\n❌ {resultat_joueur}")
                else:
                    print(f"\n=== BILAN JOUEUR : {resultat_joueur['joueur']} ===")
                    print(f"Sport : {resultat_joueur['sport']}")
                    print(f"Matchs joués : {resultat_joueur['matchs_joues']}")
                    print(f"Victoires : {resultat_joueur['victoires']}")
                    if nom_sport_choisi not in ["tennis", "lol"]: 
                        print(f"Nuls : {resultat_joueur['nuls']}")
                    print(f"Défaites : {resultat_joueur['defaites']}")
                    print(f"Win Rate : {resultat_joueur['win_rate']}")

            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()