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
 
    def get_team_points(self, nom_equipe: str, saison: str | None = None) -> dict:
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
            return self._calculate_volley_points(nom_equipe, saison)
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
    # BASKETBALL  (à compléter selon la structure de vos données)
    # ------------------------------------------------------------------
 
    def _calculate_basketball_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        """
        Calcul des points pour le basketball.
        Victoire = 2 pts, Défaite = 1 pt (format championnat européen classique).
        """
        # TODO : adapter selon la structure réelle de vos objets Match basket
        raise NotImplementedError(
            "Le calcul pour le basketball n'est pas encore implémenté."
        )
 
    # ------------------------------------------------------------------
    # TENNIS  (à compléter)
    # ------------------------------------------------------------------
 
    def _calculate_tennis_points(
        self, nom_joueur: str, saison: str | None = None
    ) -> dict:
        """
        Calcul des points ATP/WTA pour un joueur sur une saison.
        """
        raise NotImplementedError(
            "Le calcul pour le tennis n'est pas encore implémenté."
        )
 
    # ------------------------------------------------------------------
    # VOLLEYBALL  (à compléter)
    # ------------------------------------------------------------------
 
    def _calculate_volley_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        """
        Calcul des points pour le volleyball.
        Victoire 3-0 / 3-1 = 3 pts, Victoire 3-2 = 2 pts,
        Défaite 2-3 = 1 pt, Défaite 0/1-3 = 0 pt.
        """
        raise NotImplementedError(
            "Le calcul pour le volleyball n'est pas encore implémenté."
        )
 
    # ------------------------------------------------------------------
    # LOL  (à compléter)
    # ------------------------------------------------------------------
 
    def _calculate_lol_points(
        self, nom_equipe: str, saison: str | None = None
    ) -> dict:
        """
        Calcul des points pour League of Legends (victoire = 1 pt).
        """
        raise NotImplementedError(
            "Le calcul pour LoL n'est pas encore implémenté."
        )
 
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
 