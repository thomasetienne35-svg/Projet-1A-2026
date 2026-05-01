import pandas as pd


class ChampionshipPointsCalculator:
    def __init__(
        self,
        sport_name: str,
        matches_df: pd.DataFrame,
        liste_equipes_foot: list,
        liste_matchs_foot: list,
    ):
        """
        Initialise le calculateur avec le nom du sport et le DataFrame des matchs.
        """
        self.liste_equipes_foot = liste_equipes_foot
        self.liste_matchs_foot = liste_matchs_foot
        self.sport_name = sport_name.lower()
        self.matches_df = matches_df
 
    def get_team_points(self, nom_equipe: str, saison: str | None = None, genre: str | None = None) -> dict:
        """
        Méthode principale qui agit comme un "aiguilleur".
        Elle redirige vers la bonne méthode de calcul selon le sport.
 
        Parameters
        ----------
        nom_equipe : str
            Nom de l'équipe dont on veut les statistiques.
        saison : str, optional
            La saison souhaitée au format "YYYY/YYYY" (ex: "2008/2009").
            Si None, toutes les saisons sont prises en compte.
 
        Returns
        -------
        dict
            Statistiques de l'équipe pour la saison donnée.
        """
        if self.sport_name == "football":
            return self._calculate_football_points(nom_equipe, saison)
        elif self.sport_name == "basketball":
            return self._calculate_basketball_points(nom_equipe, saison)
        elif self.sport_name == "tennis":
            return self._calculate_tennis_points(nom_equipe, saison)
        elif self.sport_name in ["volley", "volleyball"]:
            return self._calculate_volley_points(nom_equipe, saison, genre)
        elif self.sport_name == "lol":
            return self._calculate_lol_points(nom_equipe, saison)
        else:
            raise ValueError(
                f"Statistiques non implémentées pour le sport : {self.sport_name}"
            )
 
    # ------------------------------------------------------------------
    # FOOTBALL
    # ------------------------------------------------------------------
 
    def _calculate_football_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        
        # --- Résolution de l'équipe ---
        team_id = None
        nom_recherche = str(nom_equipe).strip().lower()
        vrai_nom_equipe = nom_equipe

        # 1. Recherche exacte
        for equipe in self.liste_equipes_foot:
            if equipe.name is not None and str(equipe.name).strip().lower() == nom_recherche:
                team_id = equipe.id
                vrai_nom_equipe = str(equipe.name).strip()
                break
 
        # 2. Recherche partielle
        if team_id is None:
            equipes_proches = [
                eq for eq in self.liste_equipes_foot 
                if eq.name is not None and nom_recherche in str(eq.name).strip().lower()
            ]

            if len(equipes_proches) == 1:
                team_id = equipes_proches[0].id
                vrai_nom_equipe = str(equipes_proches[0].name).strip()
            elif len(equipes_proches) > 1:
                noms = ", ".join([str(eq.name).strip() for eq in equipes_proches])
                return f"Erreur : '{nom_equipe}' est ambigu. Voulez-vous dire : {noms} ?"
            else:
                return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        # VÉRIFICATION CRITIQUE : L'ID de l'équipe est-il bien là ?
        if team_id is None:
            return f"Erreur : L'équipe '{vrai_nom_equipe}' a été trouvée, mais son ID est manquant dans la base de données."

        # --- Filtrage des matchs par saison ---
        matchs_filtres = self.liste_matchs_foot
        if saison is not None:
            matchs_filtres = [
                m for m in self.liste_matchs_foot 
                if getattr(m, "season", None) == saison
            ]
            if not matchs_filtres:
                return f"Erreur : Aucun match trouvé pour la saison '{saison}'."
 
        # --- Calcul des statistiques ---
        victoires_dom = victoires_ext = nuls = 0
        defaites_dom = defaites_ext = 0
        buts_marques = buts_encaisses = nb_matchs = 0
 
        # On est maintenant certain que team_id n'est pas None
        t_id = float(team_id)

        for match in matchs_filtres:
            try:
                # getattr permet d'éviter l'erreur si l'attribut n'existe pas
                h_id = getattr(match, "home_team_api_id", None)
                a_id = getattr(match, "away_team_api_id", None)
                h_goals = getattr(match, "home_team_goal", None)
                a_goals = getattr(match, "away_team_goal", None)

                # Si l'une des données essentielles est vide (None), on ignore ce match
                if None in (h_id, a_id, h_goals, a_goals):
                    continue

                home_id = float(h_id)
                away_id = float(a_id)
                home_goals = int(h_goals)
                away_goals = int(a_goals)
            except Exception:
                # Toute autre erreur (texte illisible, etc.) fera ignorer le match
                continue
                
            if home_id == t_id:
                nb_matchs += 1
                buts_marques += home_goals
                buts_encaisses += away_goals
                if home_goals > away_goals: victoires_dom += 1
                elif home_goals == away_goals: nuls += 1
                else: defaites_dom += 1
 
            elif away_id == t_id:
                nb_matchs += 1
                buts_marques += away_goals
                buts_encaisses += home_goals
                if away_goals > home_goals: victoires_ext += 1
                elif away_goals == home_goals: nuls += 1
                else: defaites_ext += 1
 
        victoires_total = victoires_dom + victoires_ext
        defaites_total = defaites_dom + defaites_ext
        points_totaux = victoires_total * 3 + nuls * 1
 
        return {
            "equipe": vrai_nom_equipe,
            "saison": saison if saison else "Toutes saisons",
            "matchs_joues": nb_matchs,
            "points": points_totaux,
            "victoires": victoires_total,
            "victoires_domicile": victoires_dom,
            "victoires_exterieur": victoires_ext,
            "nuls": nuls,
            "defaites": defaites_total,
            "defaites_domicile": defaites_dom,
            "defaites_exterieur": defaites_ext,
            "buts_marques": buts_marques,
            "buts_encaisses": buts_encaisses,
            "difference_buts": buts_marques - buts_encaisses,
        }
 
    # ------------------------------------------------------------------
    # BASKETBALL  
    # ------------------------------------------------------------------
 
    def _calculate_basketball_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        # --- Résolution de l'équipe ---
        team_id = None
        nom_recherche = str(nom_equipe).strip().lower()
        vrai_nom_equipe = nom_equipe

        # 1. Recherche exacte
        for equipe in self.liste_equipes_foot:
            if equipe.name is not None and str(equipe.name).strip().lower() == nom_recherche:
                team_id = equipe.id
                vrai_nom_equipe = str(equipe.name).strip()
                break
 
        # 2. Recherche partielle
        if team_id is None:
            equipes_proches = [
                eq for eq in self.liste_equipes_foot 
                if eq.name is not None and nom_recherche in str(eq.name).strip().lower()
            ]

            if len(equipes_proches) == 1:
                team_id = equipes_proches[0].id
                vrai_nom_equipe = str(equipes_proches[0].name).strip()
            elif len(equipes_proches) > 1:
                noms = ", ".join([str(eq.name).strip() for eq in equipes_proches])
                return f"Erreur : '{nom_equipe}' est ambigu. Voulez-vous dire : {noms} ?"
            else:
                return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        if team_id is None:
            return f"Erreur : L'équipe '{vrai_nom_equipe}' a été trouvée, mais son ID est manquant."

        # --- Filtrage des matchs par saison ---
        matchs_filtres = self.liste_matchs_foot
        if saison is not None:
            matchs_filtres = [
                m for m in self.liste_matchs_foot 
                if getattr(m, "season", None) == saison
            ]
            if not matchs_filtres:
                return f"Erreur : Aucun match trouvé pour la saison '{saison}'."

       
        # --- Calcul des statistiques ---
        victoires_dom = victoires_ext = 0
        defaites_dom = defaites_ext = 0
        points_marques = points_encaisses = nb_matchs = 0
 
        t_id = float(team_id)

        for match in matchs_filtres:
            try:
                # On essaie les noms exacts du CSV, et on ajoute un plan B
                h_id = getattr(match, "team_id_home", getattr(match, "home_team_id", None))
                a_id = getattr(match, "team_id_away", getattr(match, "away_team_id", None))
                h_pts = getattr(match, "pts_home", getattr(match, "home_team_score", getattr(match, "home_team_goal", None)))
                a_pts = getattr(match, "pts_away", getattr(match, "away_team_score", getattr(match, "away_team_goal", None)))

                if None in (h_id, a_id, h_pts, a_pts):
                    continue

                home_id = float(str(h_id).strip())
                away_id = float(str(a_id).strip())
                home_pts = int(float(str(h_pts).strip()))
                away_pts = int(float(str(a_pts).strip()))

            except Exception:
                continue
                
            if home_id == t_id:
                nb_matchs += 1
                points_marques += home_pts
                points_encaisses += away_pts
                if home_pts > away_pts: victoires_dom += 1
                elif home_pts < away_pts: defaites_dom += 1
 
            elif away_id == t_id:
                nb_matchs += 1
                points_marques += away_pts
                points_encaisses += home_pts
                if away_pts > home_pts: victoires_ext += 1
                elif away_pts < home_pts: defaites_ext += 1
 
        victoires_total = victoires_dom + victoires_ext
        defaites_total = defaites_dom + defaites_ext
        points_totaux = (victoires_total * 2) + (defaites_total * 1)
 
        return {
            "equipe": vrai_nom_equipe,
            "saison": saison if saison else "Toutes saisons",
            "matchs_joues": nb_matchs,
            "points_championnat": points_totaux,
            "victoires": victoires_total,
            "victoires_domicile": victoires_dom,
            "victoires_exterieur": victoires_ext,
            "defaites": defaites_total,
            "defaites_domicile": defaites_dom,
            "defaites_exterieur": defaites_ext,
            "points_marques": points_marques,
            "points_encaisses": points_encaisses,
            "difference_points": points_marques - points_encaisses,
        }
 
    # ------------------------------------------------------------------
    # TENNIS  
    # ------------------------------------------------------------------
 
    def _calculate_tennis_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> str:
        """
        Le tennis est un sport individuel.
        Renvoie simplement un message explicatif.
        """
        return "Le tennis est un sport individuel. Il n'y a donc pas de statistiques d'équipe disponibles pour ce sport."
 
    # ------------------------------------------------------------------
    # VOLLEYBALL  
    # ------------------------------------------------------------------
 
    def _calculate_volley_points(
        self, nom_equipe: str, saison: str | None = None, genre: str | None = None
    ) -> dict:
        """
        Bilan de tournoi pour le volley-ball.
        Ignore les points de championnat et se concentre sur le parcours (victoires, sets, stade final).
        """
        
        # --- Résolution de l'équipe ---
        team_id = None
        nom_recherche = str(nom_equipe).strip().lower()
        vrai_nom_equipe = nom_equipe

        for equipe in self.liste_equipes_foot:
            if equipe.name is not None and str(equipe.name).strip().lower() == nom_recherche:
                team_id = equipe.id if equipe.id else equipe.name 
                vrai_nom_equipe = str(equipe.name).strip()
                break
 
        if team_id is None:
            equipes_proches = [
                eq for eq in self.liste_equipes_foot 
                if eq.name is not None and nom_recherche in str(eq.name).strip().lower()
            ]

            if len(equipes_proches) == 1:
                team_id = equipes_proches[0].id if equipes_proches[0].id else equipes_proches[0].name
                vrai_nom_equipe = str(equipes_proches[0].name).strip()
            elif len(equipes_proches) > 1:
                noms = ", ".join([str(eq.name).strip() for eq in equipes_proches])
                return f"Erreur : '{nom_equipe}' est ambigu. Voulez-vous dire : {noms} ?"
            else:
                return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        if team_id is None:
            return f"Erreur : L'équipe '{vrai_nom_equipe}' a été trouvée, mais son identifiant est manquant."

        # --- Filtrage des matchs par saison/date ---
        matchs_filtres = self.liste_matchs_foot
        if saison is not None:
            matchs_filtres = [
                m for m in self.liste_matchs_foot 
                if getattr(m, "season", getattr(m, "date", None)) == saison
            ]
            if not matchs_filtres:
                return f"Erreur : Aucun match trouvé pour la saison/date '{saison}'."
 
        # --- Calcul du bilan de tournoi ---
        victoires_total = defaites_total = 0
        sets_gagnes = sets_perdus = nb_matchs = 0
        stade_final = "Aucun match joué"
 
        t_id = str(team_id).strip().upper()

        nb_hommes = sum(1 for m in matchs_filtres if getattr(m, 'genre', None) == 'Homme')
        nb_femmes = sum(1 for m in matchs_filtres if getattr(m, 'genre', None) == 'Femme')
        nb_sans_genre = len(matchs_filtres) - nb_hommes - nb_femmes
        
        print(f"4. Répartition en mémoire -> Hommes: {nb_hommes} | Femmes: {nb_femmes} | Sans genre: {nb_sans_genre}")
        print("="*45 + "\n")
        # =========================================================

        for match in matchs_filtres:
            try:
                match_genre = getattr(match, "genre", None)
                if genre is not None and match_genre != genre:
                    continue

                h_id = getattr(match, "country_code_1", None)
                a_id = getattr(match, "country_code_2", None)
                h_sets = getattr(match, "set_country_1", None)
                a_sets = getattr(match, "set_country_2", None)

                if None in (h_id, a_id, h_sets, a_sets):
                    continue

                home_id = str(h_id).strip().upper()
                away_id = str(a_id).strip().upper()
                home_sets = int(h_sets)
                away_sets = int(a_sets)
            except Exception:
                continue
                
            if home_id == t_id or away_id == t_id:
                nb_matchs += 1
                
                # Comme les données sont chronologiques, le dernier match écrasera cette variable
                # et nous donnera le stade maximum atteint par l'équipe !
                stade_final = getattr(match, "stage", "Stade inconnu")

                if home_id == t_id:
                    sets_gagnes += home_sets
                    sets_perdus += away_sets
                    if home_sets > away_sets: victoires_total += 1
                    else: defaites_total += 1
                else:
                    sets_gagnes += away_sets
                    sets_perdus += home_sets
                    if away_sets > home_sets: victoires_total += 1
                    else: defaites_total += 1
 
        return {
            "equipe": vrai_nom_equipe,
            "tournoi": saison if saison else "Toutes compétitions",
            "stade_atteint": stade_final,
            "matchs_joues": nb_matchs,
            "victoires": victoires_total,
            "defaites": defaites_total,
            "sets_gagnes": sets_gagnes,
            "sets_perdus": sets_perdus,
            "difference_sets": sets_gagnes - sets_perdus,
        }
 
    # ------------------------------------------------------------------
    # LOL  (à compléter)
    # ------------------------------------------------------------------
 
    def _calculate_lol_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        
        team_id = None
        vrai_nom_equipe = nom_equipe
        nom_recherche = str(nom_equipe).strip().lower()

        # 1. On cherche l'équipe (par son nom ou son abréviation)
        for equipe in self.liste_equipes_foot:
            nom = str(equipe.name).strip().lower() if equipe.name else ""
            abbr = str(equipe.id).strip().lower() if equipe.id else ""
            
            if nom_recherche == nom or nom_recherche == abbr:
                team_id = str(equipe.id).strip().lower() # On garde "vit" pour les calculs
                vrai_nom_equipe = str(equipe.name).strip() # On garde "Team Vitality" pour l'affichage
                break

        if team_id is None:
            return f"Erreur : L'équipe '{nom_equipe}' est introuvable."

        # 2. On filtre par saison
        matchs_filtres = self.liste_matchs_foot
        if saison is not None:
            matchs_filtres = [m for m in self.liste_matchs_foot if getattr(m, "season", getattr(m, "date", getattr(m, "patch", None))) == saison]

        # 3. On calcule les stats en utilisant team_id ("vit")
        nb_matchs = victoires = defaites = 0
        total_kills = total_deaths = total_assists = 0

        for match in matchs_filtres:
            try:
                t_blue = str(getattr(match, "team_blue", "")).strip().lower()
                t_red = str(getattr(match, "team_red", "")).strip().lower()
                winner = str(getattr(match, "winner", "")).strip().lower()

                is_blue = (t_blue == team_id)
                is_red = (t_red == team_id)

                if not is_blue and not is_red:
                    continue 

                nb_matchs += 1
                
                # Victoire ou Défaite ?
                if winner == team_id or (is_blue and winner in ["blue", "team_blue"]) or (is_red and winner in ["red", "team_red"]):
                    victoires += 1
                else:
                    defaites += 1

                # Récupération des Kills / Deaths / Assists
                side = "blue" if is_blue else "red"
                total_kills += int(float(str(getattr(match, f"kills_team_{side}", 0)).strip()))
                total_deaths += int(float(str(getattr(match, f"deaths_team_{side}", 0)).strip()))
                total_assists += int(float(str(getattr(match, f"assists_team_{side}", 0)).strip()))

            except Exception:
                continue

        # 4. Affichage
        win_rate = round((victoires / nb_matchs) * 100, 1) if nb_matchs > 0 else 0
        kda = round((total_kills + total_assists) / total_deaths, 2) if total_deaths > 0 else "Parfait (0 mort)"

        return {
            "equipe": vrai_nom_equipe, # Affiche "Team Vitality"
            "periode": saison if saison else "Toutes périodes",
            "matchs_joues": nb_matchs,
            "victoires": victoires,
            "defaites": defaites,
            "win_rate": f"{win_rate}%",
            "kda_global": kda,
            "total_kills": total_kills,
            "total_morts": total_deaths,
            "total_assists": total_assists,
        }
 
    # ------------------------------------------------------------------
    # UTILITAIRE : lister les saisons disponibles
    # ------------------------------------------------------------------
 
    def get_available_seasons(self) -> list:
        """
        Retourne la liste des saisons disponibles dans les données.
        Utile pour guider l'utilisateur dans son choix.
        """
        saisons = set()
        for match in self.liste_matchs_foot:
            if hasattr(match, "season") and match.season:
                saisons.add(match.season)
        return sorted(saisons)
 