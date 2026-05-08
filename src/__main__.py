import sys
import os

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader
from loaders_player.player_loader import PlayerLoader
from loaders_team.team_loader import TeamLoader
from statistiques.nbre_de_points import ChampionshipPointsCalculator
from statistiques.match_par_joueur import PlayerStatsCalculator  
from statistiques.visualisation import VisualisationComparateur
from statistiques.details_match import MatchFormatter
from statistiques.statistiques_physiologie import AnalysePhysiologique
from statistiques.gestion_donnees import DataUpdater

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
            sport_obj = Sport(nom_sport_choisi)
        except (ValueError, IndexError):
            print("\n/!\\ Choix invalide.")
            continue

        matchs = tous_les_matchs.get(nom_sport_choisi, [])
        joueurs = tous_les_joueurs.get(nom_sport_choisi, [])
        
        if not matchs and not joueurs:
            print(f"\n❌ Aucune donnée (ni match, ni joueur) disponible pour {nom_sport_choisi.capitalize()}.")
            continue
            
        if not matchs:
            print(f"\n⚠️ Attention : Aucun match pour {nom_sport_choisi.capitalize()}. Certaines actions seront limitées.")

        while True:
            print("\n" + "-"*40)
            print(f"=== Actions pour {nom_sport_choisi.capitalize()} ===")
            print("1. Consulter les détails d'un match précis")
            print("2. Consulter les statistiques d'une équipe")
            print("3. Consulter les statistiques d'un joueur")
            print("4. Comparateur graphique")
            print("5. Statistique physiologique")
            print("6. Importer des données (Nouvelle compétition par CSV)")
            print("7. Éditer une donnée existante manuellement") 
            print("8. Retourner au choix des sports") 
            
            choix_action = input("\nVotre choix (1 à 8) ? (0 pour quitter) : ")

            if choix_action == "0": return
            if choix_action == "8": break

            # --- ACTION 1 : DÉTAILS D'UN MATCH ---
            if choix_action == "1":
                try:
                    saisons_dispo = sorted(list(set(str(getattr(m, "season", "")) for m in matchs if getattr(m, "season", None))))
                    saison_choisie = None
                    
                    if saisons_dispo:
                        print("\n--- ÉTAPE 1 : CHOIX DE LA SAISON ---")
                        for idx, s in enumerate(saisons_dispo, 1):
                            print(f"{idx}. {s}")
                        
                        choix_s = input("\nChoisissez le numéro de la saison (ou Entrée pour toutes) : ")
                        if choix_s.strip() and choix_s != "0":
                            saison_choisie = saisons_dispo[int(choix_s) - 1]

                    print("\n--- ÉTAPE 2 : CHOIX DU DUEL ---")
                    nom_e1 = input("Entrez le nom de la première équipe : ").strip().lower()
                    nom_e2 = input("Entrez le nom de la deuxième équipe : ").strip().lower()

                    id_e1, id_e2 = None, None
                    for eq in toutes_les_equipes[nom_sport_choisi]:
                        nom_eq = str(getattr(eq, "name", "")).lower()
                        if nom_e1 == nom_eq: id_e1 = str(eq.id)
                        if nom_e2 == nom_eq: id_e2 = str(eq.id)

                    matchs_trouves = []
                    for m in matchs:
                        if saison_choisie and str(getattr(m, "season", "")) != saison_choisie:
                            continue
                        
                        m_h_id = str(getattr(m, "home_team_api_id", getattr(m, "team_id_home", "")))
                        m_a_id = str(getattr(m, "away_team_api_id", getattr(m, "team_id_away", "")))
                        m_h_name = str(getattr(m, "home_team_name", "")).lower()
                        m_a_name = str(getattr(m, "away_team_name", "")).lower()

                        match_ok = False
                        if id_e1 and id_e2:
                            if (m_h_id == id_e1 and m_a_id == id_e2) or (m_h_id == id_e2 and m_a_id == id_e1):
                                match_ok = True
                        elif (nom_e1 in m_h_name and nom_e2 in m_a_name) or (nom_e2 in m_h_name and nom_e1 in m_a_name):
                            match_ok = True

                        if match_ok:
                            matchs_trouves.append(m)

                    if not matchs_trouves:
                        print(f"\n❌ Aucun match trouvé entre ces deux équipes.")
                    else:
                        print(f"\n✅ {len(matchs_trouves)} match(s) trouvé(s) :")
                        for m_trouve in matchs_trouves:
                            formateur = MatchFormatter(m_trouve, toutes_les_equipes[nom_sport_choisi])
                            print(formateur.generer_texte_console())

                except Exception as e:
                    print(f"\nErreur lors de la recherche : {e}")

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

                    saisons_dispo = sorted(list(calculateur.get_available_seasons()))
                    saison_choisie = None
                    
                    if saisons_dispo:
                        print("\nSaisons/Tournois disponibles :")
                        for idx, s in enumerate(saisons_dispo, 1):
                            print(f"{idx}. {s}")
                        print("0. Toutes les saisons")
                        
                        choix_s = input("\nChoisissez le numéro de la saison : ")
                        if choix_s != "0" and choix_s.strip():
                            try:
                                saison_choisie = saisons_dispo[int(choix_s) - 1]
                            except:
                                print("Choix invalide, calcul sur tout.")

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
                
                calculateur = PlayerStatsCalculator(sport_obj, matchs)
                resultat_joueur = calculateur.obtenir_bilan(nom_joueur)
                
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

            # --- ACTION 4 : 
            elif choix_action == "4":
                print("\n=== SUPER COMPARATEUR ===")
                print("1. Comparer deux joueurs")
                print("2. Comparer deux équipes")
                choix_comp = input("Votre choix (1 ou 2) : ")

                if choix_comp == "1":
                    nom_j1 = input("Nom exact du premier joueur : ")
                    nom_j2 = input("Nom exact du deuxième joueur : ")
                    
                    saisons_brutes = set()
                    for m in matchs:
                        s = getattr(m, "season", None)
                        if s is not None and str(s).strip() != "":
                            saisons_brutes.add(str(s))
                    saisons_dispo = sorted(list(saisons_brutes))
                    
                    saison_choisie = None
                    matchs_filtres = matchs
                    
                    if saisons_dispo:
                        print("\nSaisons disponibles :")
                        for idx, s in enumerate(saisons_dispo, 1):
                            print(f"{idx}. {s}")
                        print("0. Toutes les saisons")
                        
                        choix_s = input("\nChoisissez le numéro de la saison : ")
                        if choix_s != "0" and choix_s.strip():
                            try:
                                saison_choisie = saisons_dispo[int(choix_s) - 1]
                                matchs_filtres = [m for m in matchs if str(getattr(m, "season", "")) == saison_choisie]
                            except Exception:
                                print("Choix invalide, calcul sur toutes les saisons.")
                    
                    res_j1 = calculer_stats_joueur(nom_j1, nom_sport_choisi, matchs_filtres)
                    res_j2 = calculer_stats_joueur(nom_j2, nom_sport_choisi, matchs_filtres)
                    
                    if isinstance(res_j1, str): print(f"\n❌ Erreur Joueur 1 : {res_j1}")
                    elif isinstance(res_j2, str): print(f"\n❌ Erreur Joueur 2 : {res_j2}")
                    else:
                        print("\nGénération du graphique... Veuillez patienter.")
                        if saison_choisie:
                            res_j1["sport"] += f" - {saison_choisie}"
                        
                        comparateur = VisualisationComparateur()
                        comparateur.comparer_joueurs(res_j1, res_j2)

                elif choix_comp == "2":
                    nom_e1 = input("Nom exact de la première équipe : ")
                    nom_e2 = input("Nom exact de la deuxième équipe : ")

                    genre_choisi = "Homme" if nom_sport_choisi == "volley" else None
                    calculateur = ChampionshipPointsCalculator(
                        sport_name=nom_sport_choisi, matches_df=None,
                        liste_equipes_foot=toutes_les_equipes[nom_sport_choisi], liste_matchs_foot=matchs
                    )
                    
                    saisons_dispo = sorted(list(calculateur.get_available_seasons()))
                    saison_choisie = None
                    
                    if saisons_dispo:
                        print("\nSaisons disponibles :")
                        for idx, s in enumerate(saisons_dispo, 1):
                            print(f"{idx}. {s}")
                        print("0. Toutes les saisons")
                        
                        choix_s = input("\nChoisissez le numéro de la saison : ")
                        if choix_s != "0" and choix_s.strip():
                            try:
                                saison_choisie = saisons_dispo[int(choix_s) - 1]
                            except Exception:
                                print("Choix invalide, calcul sur toutes les saisons.")
                    
                    try:
                        res_e1 = calculateur.get_team_points(nom_e1, saison_choisie, genre=genre_choisi)
                        res_e2 = calculateur.get_team_points(nom_e2, saison_choisie, genre=genre_choisi)
                        
                        if isinstance(res_e1, str): print(f"\n❌ Erreur Équipe 1 : {res_e1}")
                        elif isinstance(res_e2, str): print(f"\n❌ Erreur Équipe 2 : {res_e2}")
                        else:
                            print("\nGénération du graphique... Veuillez patienter.")
                            if saison_choisie:
                                res_e1["equipe"] += f" ({saison_choisie})"
                                res_e2["equipe"] += f" ({saison_choisie})"
                            
                            comparateur = VisualisationComparateur()
                            comparateur.comparer_equipes(res_e1, res_e2)
                    except Exception as e:
                        print(f"\nErreur lors du calcul : {e}")
                        
            # --- ACTION 5 : PHYSIOLOGIE ---
            elif choix_action == "5":
                print(f"\nAnalyse de la morphologie des joueurs de {nom_sport_choisi.capitalize()}...")
                
                if not joueurs:
                    print("❌ Aucun joueur chargé pour ce sport.")
                else:
                    # Bien passé "sport_obj" et non la string
                    analyseur = AnalysePhysiologique(joueurs, sport_obj)
                    
                    print("\nOptions d'analyse :")
                    print("1. Distribution des tailles (Histogramme)")
                    print("2. Taille vs Win Rate (Heatmap)")
                    choix_graph = input("Votre choix (1 ou 2) : ")
                    
                    if choix_graph == "2":
                        analyseur.generer_heatmap_taille_victoire(matchs)
                    else:
                        analyseur.generer_graphique_taille()   
                        
            # --- ACTION 6 : 
            elif choix_action == "6":
                print("\n--- MODULE DE MISE À JOUR DYNAMIQUE ---")
                print("Entrez les chemins relatifs vers vos nouveaux fichiers CSV.")
                print("Laissez vide (appuyez sur Entrée) si vous ne voulez pas mettre à jour l'un des deux.")
                
                csv_matchs = input("1. CSV des nouveaux matchs : ").strip()
                csv_joueurs = input("2. CSV des profils de joueurs : ").strip()
                
                if not csv_matchs and not csv_joueurs:
                    print("❌ Opération annulée, aucune donnée fournie.")
                else:
                    updater = DataUpdater(sport_obj)
                    
                    path_m = csv_matchs if csv_matchs else None
                    path_j = csv_joueurs if csv_joueurs else None
                    
                    updater.mettre_a_jour_tout(path_m, path_j)
                    
                    print("\n🔄 Rechargement de l'application en mémoire...")
                    try:
                        tous_les_matchs[nom_sport_choisi] = loader_match.load_all_matches(sport_obj)
                        
                        loader_player = PlayerLoader(sport_obj)
                        tous_les_joueurs[nom_sport_choisi] = loader_player.charger_player(sport_obj)
                        
                        toutes_les_equipes[nom_sport_choisi] = loader_team.load_all_teams(sport_obj)
                        
                        matchs = tous_les_matchs[nom_sport_choisi]
                        joueurs = tous_les_joueurs[nom_sport_choisi]
                        
                        print("✨ Tout est à jour ! Les nouvelles stats sont immédiatement disponibles.")
                    except Exception as e:
                        print(f"❌ Erreur lors du rechargement des données : {e}")

            # --- ACTION 7 : ÉDITEUR MANUEL ---
            elif choix_action == "7":
                print("\n--- ÉDITEUR DE DONNÉES MANUEL ---")
                print("Que souhaitez-vous modifier ?")
                print("1. Un joueur / Une joueuse")
                print("2. Une équipe")
                choix_edition = input("Votre choix (1 ou 2) : ")

                updater = DataUpdater(sport_obj)
                succes = False
                type_modif = ""

                if choix_edition == "1":
                    succes = updater.editer_joueur_manuellement()
                    type_modif = "joueurs"
                elif choix_edition == "2":
                    succes = updater.editer_equipe_manuellement()
                    type_modif = "equipes"
                else:
                    print("❌ Choix invalide.")
                
                if succes:
                    print("\n🔄 Rechargement des données en mémoire...")
                    try:
                        if type_modif == "joueurs":
                            loader_player = PlayerLoader(sport_obj)
                            tous_les_joueurs[nom_sport_choisi] = loader_player.charger_player(sport_obj)
                            joueurs = tous_les_joueurs[nom_sport_choisi]
                        elif type_modif == "equipes":
                            toutes_les_equipes[nom_sport_choisi] = loader_team.load_all_teams(sport_obj)
                            
                        print("✨ L'application est à jour avec vos corrections !")
                    except Exception as e:
                        print(f"❌ Erreur lors du rechargement : {e}")

            else:
                if choix_action not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
                    print("\n/!\\ Choix invalide.")

            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()