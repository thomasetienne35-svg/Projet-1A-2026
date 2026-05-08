import os
import sys
import os

# On force Python à chercher les modules directement dans le dossier "src"
sys.path.insert(0, os.path.abspath("src"))

from types import SimpleNamespace

from src.statistiques.details_match import MatchFormatter


def test_trouver_nom_equipe_par_nom_direct() -> None:
    """Cas 1: Le nom de l'équipe est directement écrit dans les attributs du match."""
    faux_match = SimpleNamespace(team_blue_name="Fnatic", sport="lol", season="2024")
    formatter = MatchFormatter(match=faux_match)

    noms_possibles = ["team_blue_name", "home_team_name"]
    ids_possibles = ["team_id"]

    resultat = formatter._trouver_nom_equipe(
        noms_possibles, ids_possibles, "Equipe Defaut"
    )
    assert resultat == "Fnatic"


def test_trouver_nom_equipe_par_id_croise() -> None:
    """Cas 2: Pas de nom, on utilise l'ID pour chercher dans liste_equipes."""
    faux_match = SimpleNamespace(
        home_team_api_id="9987", sport="football", season="2023"
    )
    fausse_equipe = SimpleNamespace(team_api_id="9987", team_long_name="KRC Genk")

    formatter = MatchFormatter(match=faux_match, liste_equipes=[fausse_equipe])

    noms_possibles = ["home_team_name"]
    ids_possibles = ["home_team_api_id"]

    resultat = formatter._trouver_nom_equipe(
        noms_possibles, ids_possibles, "Equipe Defaut"
    )
    assert resultat == "KRC Genk"


def test_trouver_nom_equipe_ignore_les_nan() -> None:
    """Cas 3: Vérifier que les valeurs vides ou 'nan' sont bien ignorées."""
    faux_match = SimpleNamespace(
        home_team_name="nan", home_team_api_id="None", sport="tennis"
    )
    formatter = MatchFormatter(match=faux_match)

    resultat = formatter._trouver_nom_equipe(
        ["home_team_name"], ["home_team_api_id"], "Equipe Inconnue"
    )
    assert resultat == "Equipe Inconnue"


def test_recuperer_score_sport_a_points() -> None:
    """Cas 4: Formatage classique avec points (Football, Basket, Volley)."""
    faux_match = SimpleNamespace(
        sport="Basketball", season="2023", home_team_score="110", away_team_score="98"
    )
    formatter = MatchFormatter(match=faux_match)
    formatter.nom_home = "Lakers"
    formatter.nom_away = "Bulls"

    score_texte = formatter._recuperer_score()

    assert score_texte == "\n📊 Score : Lakers 110 - 98 Bulls"


def test_recuperer_score_esport_lol() -> None:
    """Cas 5: Formatage spécifique pour League of Legends (vainqueur)."""
    faux_match = SimpleNamespace(sport="lol", winner="Fnatic")
    formatter = MatchFormatter(match=faux_match)

    score_texte = formatter._recuperer_score()

    assert score_texte == "\n🏆 Vainqueur : Fnatic"


def test_recuperer_score_tennis() -> None:
    """Cas 6: Formatage spécifique pour le Tennis."""
    faux_match = SimpleNamespace(sport="tennis")
    formatter = MatchFormatter(match=faux_match)

    score_texte = formatter._recuperer_score()

    assert score_texte == "\n🏆 Résultat : Vainqueur Domicile"


def test_formater_joueurs_liste_valide() -> None:
    """Cas 7: Une liste normale de joueurs est bien fusionnée avec des virgules."""
    faux_match = SimpleNamespace(sport="football")
    formatter = MatchFormatter(match=faux_match)

    resultat = formatter._formater_joueurs(["Messi", "Mbappe", "Neymar"])
    assert resultat == "Messi, Mbappe, Neymar"


def test_formater_joueurs_vide_ou_nan():
    """Cas 8: Une liste vide ou la valeur 'nan' renvoie 'Non renseigné'."""
    faux_match = SimpleNamespace(sport="football")
    formatter = MatchFormatter(match=faux_match)

    assert formatter._formater_joueurs([]) == "Non renseigné"
    assert formatter._formater_joueurs("nan") == "Non renseigné"


def test_generer_texte_console_complet() -> None:
    """Cas 9: Le test ultime, on vérifie que tout s'assemble sans erreur."""
    faux_match = SimpleNamespace(
        id="M123",
        sport="football",
        season="2024",
        home_team_name="PSG",
        away_team_name="OM",
        home_team_goal="3",
        away_team_goal="0",
        list_home_player=["Joueur A", "Joueur B"],
        list_away_player=["Joueur C"],
    )
    formatter = MatchFormatter(match=faux_match)
    texte_final = formatter.generer_texte_console()

    assert "=== DÉTAILS DU MATCH M123 ===" in texte_final
    assert "📌 Sport  : Football" in texte_final
    assert "📅 Saison : 2024" in texte_final
    assert "📊 Score : PSG 3 - 0 OM" in texte_final
    assert "🏠 PSG :\n> Joueur A, Joueur B" in texte_final
    assert "✈️ OM :\n> Joueur C" in texte_final
