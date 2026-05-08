import os
from typing import Any

import pandas as pd

# Chemins réels lus par les loaders
CHEMINS_PAR_SPORT: dict[str, dict[str, str]] = {
    "football": {
        "matchs": "data/football_european_leagues_tdd/match.csv",
        "joueurs": "data/football_european_leagues_tdd/player.csv",
    },
    "basketball": {
        "matchs": "data/basketball/game.csv",
        "joueurs": "data/basketball/player.csv",
    },
    "lol": {
        "matchs": "data/league_of_legends_tdd/match.csv",
        "joueurs": "data/league_of_legends_tdd/player.csv",
    },
    "tennis_atp": {
        "matchs": "data/tennis_tdd/atp_matches_2024.csv",
        "joueurs": "data/tennis_tdd/atp_players_2024.csv",
    },
    "tennis_wta": {
        "matchs": "data/tennis_tdd/wta_matches_2024.csv",
        "joueurs": "data/tennis_tdd/wta_players_2024.csv",
    },
    "volley_hommes": {
        "matchs": "data/volleyball_tdd/match_men.csv",
        "joueurs": "data/volleyball_tdd/player_men.csv",
    },
    "volley_femmes": {
        "matchs": "data/volleyball_tdd/match_women.csv",
        "joueurs": "data/volleyball_tdd/player_women.csv",
    },
}


class DataUpdater:
    """Classe responsable de la mise à jour des bases de données CSV (matchs et joueurs)."""

    def __init__(self, sport_obj: Any, sous_type: str | None = None) -> None:
        """Initialise la classe.

        Parameters
        ----------
        sport_obj : Any
            Objet Sport avec attribut .name ('football', 'tennis', 'volley', etc.)
        sous_type : str | None
            Pour tennis : 'atp' ou 'wta'.
            Pour volley : 'hommes' ou 'femmes'.
            Ignoré pour les autres sports.
        """
        sport = sport_obj.name

        if sport == "tennis":
            cle = f"tennis_{sous_type}" if sous_type in ("atp", "wta") else "tennis_atp"
        elif sport == "volley":
            cle = (
                f"volley_{sous_type}"
                if sous_type in ("hommes", "femmes")
                else "volley_hommes"
            )
        else:
            cle = sport

        self.sport = sport
        self.sous_type = sous_type
        self.path_matches = CHEMINS_PAR_SPORT.get(cle, {}).get("matchs")
        self.path_players = CHEMINS_PAR_SPORT.get(cle, {}).get("joueurs")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def valider_csv(
        self, chemin_utilisateur: str, type_fichier: str
    ) -> tuple[bool, str]:
        """Valide le format d'un CSV fourni par l'utilisateur.

        La validation compare les colonnes (noms + nombre) avec celles
        du fichier de référence présent dans le repo.

        Parameters
        ----------
        chemin_utilisateur : str
            Chemin vers le fichier CSV à importer.
        type_fichier : str
            'matchs' ou 'joueurs' — détermine le fichier de référence.

        Returns:
        -------
        tuple[bool, str]
            (True, 'OK') si le fichier est valide, (False, message) sinon.
        """
        # 1. Extension
        if not chemin_utilisateur.lower().endswith(".csv"):
            return False, "Le fichier doit être au format CSV (extension .csv)."

        # 2. Existence du fichier utilisateur
        if not os.path.exists(chemin_utilisateur):
            return False, f"Fichier introuvable : {chemin_utilisateur}"

        # 3. Fichier de référence
        chemin_ref = (
            self.path_matches if type_fichier == "matchs" else self.path_players
        )
        if not chemin_ref or not os.path.exists(chemin_ref):
            return False, f"Fichier de référence introuvable : {chemin_ref}"

        # 4. Lecture des en-têtes uniquement (nrows=0 = rapide)
        try:
            cols_user = list(pd.read_csv(chemin_utilisateur, nrows=0).columns)
            cols_ref = list(pd.read_csv(chemin_ref, nrows=0).columns)
        except Exception as e:
            return False, f"Erreur de lecture du CSV : {e}"

        # 5. Nombre de colonnes
        if len(cols_user) != len(cols_ref):
            return (
                False,
                f"Nombre de colonnes incorrect.\n"
                f"  Attendu : {len(cols_ref)} colonnes\n"
                f"  Reçu    : {len(cols_user)} colonnes",
            )

        # 6. Noms des colonnes
        manquantes = set(cols_ref) - set(cols_user)
        en_trop = set(cols_user) - set(cols_ref)
        if manquantes or en_trop:
            msg = "Les noms de colonnes ne correspondent pas."
            if manquantes:
                msg += f"\n  Manquantes  : {', '.join(sorted(manquantes))}"
            if en_trop:
                msg += f"\n  Inattendues : {', '.join(sorted(en_trop))}"
            return False, msg

        return True, "OK"

    # ------------------------------------------------------------------
    # Mise à jour principale
    # ------------------------------------------------------------------

    def mettre_a_jour_tout(
        self,
        chemin_nouveaux_matchs: str | None,
        chemin_nouveaux_joueurs: str | None = None,
    ) -> bool:
        """Valide puis importe les nouveaux fichiers CSV.

        Parameters
        ----------
        chemin_nouveaux_matchs : str | None
            Chemin vers le CSV des nouveaux matchs (None = ignoré).
        chemin_nouveaux_joueurs : str | None, optional
            Chemin vers le CSV des nouveaux joueurs (None = ignoré).

        Returns:
        -------
        bool
            True si au moins un fichier a été importé avec succès.
        """
        print(f"\n🔄 Début de la mise à jour pour {self.sport}...")
        au_moins_un_succes = False

        # --- Matchs ---
        if chemin_nouveaux_matchs:
            valide, msg = self.valider_csv(chemin_nouveaux_matchs, "matchs")
            if not valide:
                print(f"\n❌ Import des matchs refusé :\n  {msg}")
                print("⚠️  Corrigez votre fichier et relancez l'import.")
            else:
                df_nouveaux = pd.read_csv(chemin_nouveaux_matchs)
                df_nouveaux.to_csv(
                    self.path_matches, mode="a", header=False, index=False
                )
                print(
                    f"✅ {len(df_nouveaux)} nouveau(x) match(s) ajouté(s) → {self.path_matches}"
                )
                au_moins_un_succes = True

        # --- Joueurs ---
        if chemin_nouveaux_joueurs:
            valide, msg = self.valider_csv(chemin_nouveaux_joueurs, "joueurs")
            if not valide:
                print(f"\n❌ Import des joueurs refusé :\n  {msg}")
                print("⚠️  Corrigez votre fichier et relancez l'import.")
            else:
                self._update_player_characteristics(chemin_nouveaux_joueurs)
                au_moins_un_succes = True

        return au_moins_un_succes

    def _update_player_characteristics(self, path_updates: str) -> None:
        """Fusionne les nouvelles infos joueurs sans créer de doublons.

        Parameters
        ----------
        path_updates : str
            Chemin vers le CSV des mises à jour joueurs.
        """
        df_actuel = pd.read_csv(self.path_players)
        df_updates = pd.read_csv(path_updates)

        # Colonne identifiant (première colonne dont le nom contient 'name' ou 'nom')
        col_id = next(
            (c for c in df_actuel.columns if "name" in c.lower() or "nom" in c.lower()),
            df_actuel.columns[0],
        )

        for _, row in df_updates.iterrows():
            val_id = row[col_id]
            if val_id in df_actuel[col_id].values:
                for col in df_updates.columns:
                    if col in df_actuel.columns and col != col_id:
                        df_actuel.loc[df_actuel[col_id] == val_id, col] = row[col]
            else:
                df_actuel = pd.concat(
                    [df_actuel, pd.DataFrame([row])], ignore_index=True
                )

        df_actuel.to_csv(self.path_players, index=False)
        print(f"✅ Joueurs mis à jour → {self.path_players}")

    # ------------------------------------------------------------------
    # Éditeurs manuels (inchangés dans leur logique)
    # ------------------------------------------------------------------

    def editer_joueur_manuellement(self) -> bool:
        """Permet de modifier une caractéristique d'un joueur via la console.

        Returns:
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        print(f"\n📁 Fichiers joueurs pour {self.sport.capitalize()} :")
        if self.sport == "football":
            print("  👉 data/football_european_leagues_tdd/player.csv")
        elif self.sport == "basketball":
            print("  👉 data/basketball/player.csv")
        elif self.sport == "tennis":
            print("  👉 data/tennis_tdd/atp_players_2024.csv")
            print("  👉 data/tennis_tdd/wta_players_2024.csv")
        elif self.sport == "volley":
            print("  👉 data/volleyball_tdd/player_men.csv")
            print("  👉 data/volleyball_tdd/player_women.csv")
        elif self.sport == "lol":
            print("  👉 data/league_of_legends_tdd/player.csv")

        chemin_csv = input(
            "\nEntrez le chemin exact du fichier CSV à modifier (Entrée pour annuler) : "
        ).strip()
        if not chemin_csv:
            return False
        if not os.path.exists(chemin_csv):
            print("❌ Fichier introuvable.")
            return False

        df = pd.read_csv(chemin_csv)
        colonnes_noms = [
            c for c in df.columns if "name" in c.lower() or "nom" in c.lower()
        ]
        if not colonnes_noms:
            print("❌ Impossible d'identifier la colonne de noms.")
            return False

        nom_recherche = input(
            "\nNom (ou partie du nom) du joueur à modifier : "
        ).strip()
        masque = pd.Series(False, index=df.index)
        for col in colonnes_noms:
            masque |= (
                df[col].astype(str).str.contains(nom_recherche, case=False, na=False)
            )
        resultats = df[masque]

        if resultats.empty:
            print("❌ Joueur introuvable.")
            return False

        print("\n=== Joueur(s) trouvé(s) ===")
        print(resultats)

        try:
            index_ligne = int(input("\nNuméro de ligne à modifier : "))
            if index_ligne not in resultats.index:
                raise ValueError
        except ValueError:
            print("❌ Numéro invalide.")
            return False

        print("Colonnes disponibles :", ", ".join(df.columns))
        colonne = input("Colonne à modifier : ").strip()
        if colonne not in df.columns:
            print("❌ Colonne introuvable.")
            return False

        nouvelle_valeur = input(f"Nouvelle valeur pour '{colonne}' : ")
        df.loc[index_ligne, colonne] = nouvelle_valeur
        df.to_csv(chemin_csv, index=False)
        print("✅ Modification enregistrée.")
        return True

    def editer_equipe_manuellement(self) -> bool:
        """Permet de modifier une caractéristique d'une équipe via la console.

        Returns:
        -------
        bool
            True si la modification a réussi, False sinon.
        """
        print(f"\n📁 Fichiers équipes pour {self.sport.capitalize()} :")
        if self.sport == "football":
            print("  👉 data/football_european_leagues_tdd/team.csv")
        elif self.sport == "basketball":
            print("  👉 data/basketball/team.csv")
        elif self.sport == "lol":
            print("  👉 data/league_of_legends_tdd/team.csv")
        else:
            print(f"  👉 Cherchez dans data/{self.sport}/")

        chemin_csv = input(
            "\nEntrez le chemin exact du fichier CSV de l'équipe (Entrée pour annuler) : "
        ).strip()
        if not chemin_csv:
            return False
        if not os.path.exists(chemin_csv):
            print("❌ Fichier introuvable.")
            return False

        df = pd.read_csv(chemin_csv)
        colonnes_noms = [
            c
            for c in df.columns
            if ("name" in c.lower() or "nom" in c.lower() or "team" in c.lower())
            and "id" not in c.lower()
        ]
        if not colonnes_noms:
            print("❌ Impossible d'identifier la colonne de noms.")
            return False

        nom_recherche = input(
            "\nNom (ou partie du nom) de l'équipe à modifier : "
        ).strip()
        noms_virtuels = df[colonnes_noms].astype(str).agg(" ".join, axis=1)
        resultats = df[noms_virtuels.str.contains(nom_recherche, case=False, na=False)]

        if resultats.empty:
            print("❌ Équipe introuvable.")
            return False

        print("\n=== Équipe(s) trouvée(s) ===")
        print(resultats)

        try:
            index_ligne = int(input("\nNuméro de ligne à modifier : "))
            if index_ligne not in resultats.index:
                raise ValueError
        except ValueError:
            print("❌ Numéro invalide.")
            return False

        print("Colonnes disponibles :", ", ".join(df.columns))
        colonne = input("Colonne à modifier : ").strip()
        if colonne not in df.columns:
            print("❌ Colonne introuvable.")
            return False

        nouvelle_valeur = input(f"Nouvelle valeur pour '{colonne}' : ")
        df.loc[index_ligne, colonne] = nouvelle_valeur
        df.to_csv(chemin_csv, index=False)
        print("✅ Modification enregistrée.")
        return True
