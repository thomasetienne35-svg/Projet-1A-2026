import os
from typing import Any

import pandas as pd


class DataUpdater:
    """Classe responsable de la mise à jour des bases de données CSV (matchs et joueurs)."""
    def __init__(self, sport_obj: Any) -> None:
        self.sport = sport_obj.name
        self.path_matches = f"data/{self.sport}/matchs.csv"
        self.path_players = f"data/{self.sport}/player.csv"


    def mettre_a_jour_tout(self, chemin_nouveaux_matchs: str, 
                           chemin_nouveaux_joueurs: str | None = None) -> None:
        """Méthode principale pour importer une compétition et mettre à jour les profils.

        Parameters
        ----------
        chemin_nouveaux_matchs : str
            Chemin vers le fichier CSV contenant les nouveaux matchs.
        chemin_nouveaux_joueurs : str | None, optional
            Chemin vers le fichier CSV des nouveaux joueurs, par défaut None.
        """
        print(f"\n🔄 Début de la mise à jour pour le {self.sport}...")
        if os.path.exists(chemin_nouveaux_matchs):
            df_nouveaux = pd.read_csv(chemin_nouveaux_matchs)
            df_nouveaux.to_csv(self.path_matches, mode='a', header=False, index=False)
            print(f"✅ {len(df_nouveaux)} nouveaux matchs ajoutés.")

        if chemin_nouveaux_joueurs and os.path.exists(chemin_nouveaux_joueurs):
            self._update_player_characteristics(chemin_nouveaux_joueurs)


    def _update_player_characteristics(self, path_updates: str) -> None:
        """Fusionne les nouvelles infos joueurs avec l'ancien fichier sans créer de doublons.

        Parameters
        ----------
        path_updates : str
            Chemin vers le CSV contenant les mises à jour de caractéristiques.
        """
        df_actuel = pd.read_csv(self.path_players)
        df_updates = pd.read_csv(path_updates)

        for i, row in df_updates.iterrows():
            nom = row['player_name']
            if nom in df_actuel['player_name'].values:
                for col in df_updates.columns:
                    if col in df_actuel.columns and col != 'player_name':
                        df_actuel.loc[df_actuel['player_name'] == nom, col] = row[col]
            else:
                df_actuel = pd.concat([df_actuel, pd.DataFrame([row])], 
                                      ignore_index=True)

        # Sauvegarde du fichier mis à jour
        df_actuel.to_csv(self.path_players, index=False)
        print("✅ Caractéristiques des joueurs mises à jour "
        "(nouvelles tailles, nouveaux joueurs).")
    
    
    def editer_joueur_manuellement(self) -> bool:
        """Permet de chercher un joueur dans un CSV et de modifier une caractéristique via la console.

        Returns:
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        print(f"\n📁 Fichiers de données détectés pour {self.sport.capitalize()} :")
        if self.sport == "football": 
            print("👉 data/football_european_leagues_tdd/player.csv")
        elif self.sport == "basketball": 
            print("👉 data/basketball/player.csv")
        elif self.sport == "tennis": 
            print("👉 data/tennis_tdd/atp_players_2024.csv (ou wta_players_2024.csv)")
        elif self.sport == "volley": 
            print("👉 data/volleyball_tdd/player_men.csv (ou player_women.csv)")
        
        chemin_csv = input("\nEntrez le chemin exact du fichier CSV à modifier "
        "(ou Entrée pour annuler) : ").strip()

        if not chemin_csv:
            return False

        if not os.path.exists(chemin_csv):
            print("❌ Fichier introuvable à ce chemin. Vérifiez l'orthographe.")
            return False

        df = pd.read_csv(chemin_csv)

        colonnes_noms = [col for col in df.columns if "name" in col.lower() or 
                         "nom" in col.lower()]
        
        if not colonnes_noms:
            print("❌ Impossible d'identifier les colonnes de noms pour ce CSV.")
            return False

        nom_recherche = input("\nEntrez le nom (ou une partie du nom) du joueur " \
        "à modifier : ").strip()
        
        masque = pd.Series(False, index=df.index)
        for col in colonnes_noms:
            masque = masque | df[col].astype(str).str.contains(nom_recherche, case=False
                                                               , na=False)
            
        resultats = df[masque]
        
        if resultats.empty:
            print("❌ Joueur introuvable dans ce fichier.")
            return False
            
        print("\n=== Joueur(s) trouvé(s) ===")
        print(resultats)
        
        index_str = input("\nEntrez le numéro de la ligne à modifier "
        "(le nombre tout à gauche) : ")
        try:
            index_ligne = int(index_str)
            if index_ligne not in resultats.index:
                raise ValueError
        except ValueError:
            print("❌ Numéro de ligne invalide.")
            return False
            
        print("\nColonnes disponibles :", ", ".join(df.columns))
        colonne = input("Entrez le nom exact de la colonne à modifier : ").strip()
        
        if colonne not in df.columns:
            print("❌ Colonne introuvable.")
            return False
            
        nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{colonne}' : ")
        
        df.loc[index_ligne, colonne] = nouvelle_valeur
        df.to_csv(chemin_csv, index=False)
        
        print("✅ Modification effectuée ! Le fichier a bien été mis à jour.")
        return True
    

    def editer_equipe_manuellement(self) -> bool:
        """Permet de chercher une équipe dans un CSV et de modifier une caractéristique via la console.

        Returns:
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        print(f"\n📁 Fichiers d'équipes détectés pour {self.sport.capitalize()} :")
        if self.sport == "football":
            print("👉 data/football_european_leagues_tdd/team.csv")
        elif self.sport == "basketball": 
            print("👉 data/basketball/team.csv")
        elif self.sport == "lol": 
            print("👉 data/lol_tdd/team.csv")
        else: 
            print(
                f"👉 Cherchez le fichier contenant les équipes dans data/{self.sport}/")
        
        chemin_csv = input("\nEntrez le chemin exact du fichier CSV de l'équipe "
        "(ou Entrée pour annuler) : ").strip()

        if not chemin_csv:
            return False

        if not os.path.exists(chemin_csv):
            print("❌ Fichier introuvable à ce chemin. Vérifiez l'orthographe.")
            return False

        df = pd.read_csv(chemin_csv)

        colonnes_noms = [
            col for col in df.columns 
            if ("name" in col.lower() or "nom" in col.lower() or "equipe" in col.lower()
                or "team" in col.lower())
            and "id" not in col.lower()
        ]
        
        if not colonnes_noms:
            print("❌ Impossible d'identifier les colonnes de noms pour ce CSV.")
            return False

        nom_recherche = input("\nEntrez le nom (ou une partie du nom) " \
        "de l'équipe à modifier : ").strip()
        
        noms_complets_virtuels = df[colonnes_noms].astype(str).agg(' '.join, axis=1)
        
        masque = noms_complets_virtuels.str.contains(nom_recherche, 
                                                     case=False, na=False)
        resultats = df[masque]
        
        if resultats.empty:
            print("❌ Équipe introuvable dans ce fichier.")
            return False
            
        print("\n=== Équipe(s) trouvée(s) ===")
        print(resultats)
        
        index_str = input("\nEntrez le numéro de la ligne à modifier "
        "(le nombre tout à gauche) : ")
        try:
            index_ligne = int(index_str)
            if index_ligne not in resultats.index:
                raise ValueError
        except ValueError:
            print("❌ Numéro de ligne invalide.")
            return False
            
        print("\nColonnes disponibles :", ", ".join(df.columns))
        colonne = input("Entrez le nom exact de la colonne à modifier : ").strip()
        
        if colonne not in df.columns:
            print("❌ Colonne introuvable.")
            return False
            
        nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{colonne}' : ")
        
        df.loc[index_ligne, colonne] = nouvelle_valeur
        df.to_csv(chemin_csv, index=False)
        
        print("✅ Modification effectuée ! Le fichier de l'équipe " \
        "a bien été mis à jour.")
        return True