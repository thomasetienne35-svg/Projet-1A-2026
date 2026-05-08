from typing import Any, List, Union

from src.match import Match


class MatchFormatter:
    """Classe responsable du formatage et de l'affichage des détails d'un match."""

    def __init__(self, match: Match, liste_equipes: List[Any] | None = None) -> None:
        self.match = match
        self.liste_equipes = liste_equipes if liste_equipes else []
        self.sport = str(getattr(match, "sport", "Inconnu")).capitalize()
        self.m_id = getattr(match, "id", "N/A")
        self.saison = getattr(match, "season", "N/A")

        self.nom_home = self._trouver_nom_equipe(
            noms_possibles=[
                "home_team_name",
                "team_home",
                "team_blue_name",
                "home_team",
                "team_name_home",
            ],
            ids_possibles=["home_team_api_id", "team_id_home"],
            nom_par_defaut="Équipe Domicile",
        )
        self.nom_away = self._trouver_nom_equipe(
            noms_possibles=[
                "away_team_name",
                "team_away",
                "team_red_name",
                "away_team",
                "team_name_away",
            ],
            ids_possibles=["away_team_api_id", "team_id_away"],
            nom_par_defaut="Équipe Extérieure",
        )

    def _trouver_nom_equipe(
        self, noms_possibles: list[str], ids_possibles: list[str], nom_par_defaut: str
    ) -> str:
        """Cherche le nom de l'équipe dans l'objet match ou via son ID dans la liste.

        Parameters
        ----------
        noms_possibles : List[str]
            Liste des attributs potentiels contenant le nom en clair.
        ids_possibles : List[str]
            Liste des attributs potentiels contenant l'ID technique.
        nom_par_defaut : str
            Nom à renvoyer si aucune information n'est trouvée.

        Returns:
        -------
        str
            Le nom de l'équipe résolu.
        """
        for attr in noms_possibles:
            valeur = getattr(self.match, attr, None)
            if valeur is not None and str(valeur).strip() not in ["", "nan", "None"]:
                return str(valeur).strip()

        id_equipe = None
        for attr in ids_possibles:
            valeur = getattr(self.match, attr, None)
            if valeur is not None and str(valeur).strip() not in ["", "nan", "None"]:
                id_equipe = str(valeur).strip()
                break

        if id_equipe:
            for equipe in self.liste_equipes:
                e_id = str(
                    getattr(
                        equipe,
                        "id",
                        getattr(equipe, "team_api_id", getattr(equipe, "team_id", "")),
                    )
                ).strip()
                if e_id == id_equipe:
                    return str(
                        getattr(
                            equipe,
                            "name",
                            getattr(equipe, "team_long_name", nom_par_defaut),
                        )
                    ).strip()

        return nom_par_defaut

    def _recuperer_score(self) -> str:
        """Génère la ligne de score formatée selon le sport pratiqué.

        Returns:
        -------
        str
            Une chaîne contenant l'émoji et le score détaillé.
        """
        if self.sport.lower() in ["football", "basketball", "volley"]:
            h_score = getattr(
                self.match,
                "pts_home",
                getattr(
                    self.match,
                    "home_team_score",
                    getattr(self.match, "home_team_goal", "?"),
                ),
            )
            a_score = getattr(
                self.match,
                "pts_away",
                getattr(
                    self.match,
                    "away_team_score",
                    getattr(self.match, "away_team_goal", "?"),
                ),
            )
            return f"\n📊 Score : {self.nom_home} {h_score} - {a_score} {self.nom_away}"

        elif self.sport.lower() == "lol":
            winner = str(getattr(self.match, "winner", "?")).capitalize()
            return f"\n🏆 Vainqueur : {winner}"

        elif self.sport.lower() == "tennis":
            return "\n🏆 Résultat : Vainqueur Domicile"

        return ""

    def _formater_joueurs(self, liste_joueurs: Union[List[Any], str]) -> str:
        """Transforme une liste de joueurs en une chaîne de caractères lisible.

        Parameters
        ----------
        liste_joueurs : Union[List[Any], str]
            La liste des objets joueurs ou une valeur brute.

        Returns:
        -------
        str
            Les noms des joueurs séparés par des virgules ou 'Non renseigné'.
        """
        if isinstance(liste_joueurs, list):
            texte = ", ".join(map(str, liste_joueurs))
        else:
            texte = str(liste_joueurs)
        return texte if texte and texte != "nan" else "Non renseigné"

    def generer_texte_console(self) -> str:
        """Assemble toutes les informations pour créer le rendu final en console.

        Returns:
        -------
        str
            Le bloc de texte complet prêt à être affiché.
        """
        texte = "\n" + "=" * 50
        texte += f"\n=== DÉTAILS DU MATCH {self.m_id} ==="
        texte += f"\n📌 Sport  : {self.sport}"

        if str(self.saison) not in ["N/A", "None", "", "nan"]:
            texte += f"\n📅 Saison : {self.saison}"

        texte += self._recuperer_score()

        texte += f"\n\n🏠 {self.nom_home.upper()} :\n> {
            self._formater_joueurs(getattr(self.match, 'list_home_player', []))
        }"
        texte += f"\n\n✈️ {self.nom_away.upper()} :\n> {
            self._formater_joueurs(getattr(self.match, 'list_away_player', []))
        }"
        texte += "\n" + "=" * 50

        return texte
