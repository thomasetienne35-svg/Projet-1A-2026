class MatchFormatter:
    """
    Classe responsable du formatage et de l'affichage des détails d'un match.
    """
    # NOUVEAU : On accepte "liste_equipes" lors de la création
    def __init__(self, match, liste_equipes=None):
        self.match = match
        self.liste_equipes = liste_equipes if liste_equipes else []
        self.sport = str(getattr(match, "sport", "Inconnu")).capitalize()
        self.m_id = getattr(match, "id", "N/A")
        self.saison = getattr(match, "season", "N/A")
        
        # On cherche par Noms directs OU par IDs croisés avec la liste des équipes
        self.nom_home = self._trouver_nom_equipe(
            noms_possibles=["home_team_name", "team_home", "team_blue_name", "home_team", "team_name_home"], 
            ids_possibles=["home_team_api_id", "team_id_home"],
            nom_par_defaut="Équipe Domicile"
        )
        self.nom_away = self._trouver_nom_equipe(
            noms_possibles=["away_team_name", "team_away", "team_red_name", "away_team", "team_name_away"], 
            ids_possibles=["away_team_api_id", "team_id_away"],
            nom_par_defaut="Équipe Extérieure"
        )

    def _trouver_nom_equipe(self, noms_possibles, ids_possibles, nom_par_defaut):
        """Cherche le nom directement, sinon utilise l'ID pour le trouver dans la liste des équipes."""
        # 1. On cherche si le nom est déjà dans le match (LoL, Tennis...)
        for attr in noms_possibles:
            valeur = getattr(self.match, attr, None)
            if valeur is not None and str(valeur).strip() not in ["", "nan", "None"]:
                return str(valeur).strip()
                
        # 2. Sinon, on cherche via l'ID (Football, Basket...)
        id_equipe = None
        for attr in ids_possibles:
            valeur = getattr(self.match, attr, None)
            if valeur is not None and str(valeur).strip() not in ["", "nan", "None"]:
                id_equipe = str(valeur).strip()
                break
                
        if id_equipe:
            # On fouille dans la liste des équipes pour trouver ce numéro
            for equipe in self.liste_equipes:
                e_id = str(getattr(equipe, "id", getattr(equipe, "team_api_id", getattr(equipe, "team_id", "")))).strip()
                if e_id == id_equipe:
                    # On a trouvé l'équipe, on renvoie son nom ! (name ou team_long_name)
                    return str(getattr(equipe, "name", getattr(equipe, "team_long_name", nom_par_defaut))).strip()
                    
        return nom_par_defaut

    def _recuperer_score(self):
        if self.sport.lower() in ["football", "basketball", "volley"]:
            h_score = getattr(self.match, "pts_home", getattr(self.match, "home_team_score", getattr(self.match, "home_team_goal", "?")))
            a_score = getattr(self.match, "pts_away", getattr(self.match, "away_team_score", getattr(self.match, "away_team_goal", "?")))
            return f"\n📊 Score  : {self.nom_home} {h_score} - {a_score} {self.nom_away}"
            
        elif self.sport.lower() == "lol":
            winner = str(getattr(self.match, "winner", "?")).capitalize()
            return f"\n🏆 Vainqueur : {winner}"
            
        elif self.sport.lower() == "tennis":
            return f"\n🏆 Résultat : Vainqueur Domicile"
            
        return ""

    def _formater_joueurs(self, liste_joueurs):
        if isinstance(liste_joueurs, list): 
            texte = ", ".join(map(str, liste_joueurs))
        else: 
            texte = str(liste_joueurs)
        return texte if texte and texte != 'nan' else 'Non renseigné'

    def generer_texte_console(self):
        texte = "\n" + "="*50
        texte += f"\n=== DÉTAILS DU MATCH {self.m_id} ==="
        texte += f"\n📌 Sport  : {self.sport}"
        
        if str(self.saison) not in ["N/A", "None", "", "nan"]:
            texte += f"\n📅 Saison : {self.saison}"

        texte += self._recuperer_score()
        
        texte += f"\n\n🏠 {self.nom_home.upper()} :\n> {self._formater_joueurs(getattr(self.match, 'list_home_player', []))}"
        texte += f"\n\n✈️ {self.nom_away.upper()} :\n> {self._formater_joueurs(getattr(self.match, 'list_away_player', []))}"
        texte += "\n" + "="*50
        
        return texte