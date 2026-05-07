from typing import Any

def calculer_stats_joueur(nom_joueur: str, sport: str, 
                          matchs: list[Any]) -> dict[str, Any] | str:
    """Parcourt une liste de matchs pour identifier un joueur et calculer ses statistiques de performance.

    Parameters
    ----------
    nom_joueur : str
        Le nom (ou une partie du nom) du joueur à rechercher.
    sport : str
        Le sport concerné (détermine la logique de calcul des victoires).
    matchs : list[Any]
        Une liste d'objets matchs à analyser.

    Returns:
    -------
    dict[str, Any] | str
        Un dictionnaire contenant le bilan (victoires, nuls, défaites, win rate) 
        ou un message d'erreur si aucune donnée n'est trouvée.
    """
    nom_recherche = nom_joueur.strip().lower()
    nb_matchs = victoires = defaites = nuls = 0
    vrai_nom = nom_joueur

    for match in matchs:
        is_home = False
        is_away = False

        for p_home in getattr(match, "list_home_player", []):
            if nom_recherche in str(p_home).lower():
                is_home = True
                vrai_nom = str(p_home) 
                break
                
        for p_away in getattr(match, "list_away_player", []):
            if nom_recherche in str(p_away).lower():
                is_away = True
                vrai_nom = str(p_away)
                break

        if not is_home and not is_away:
            continue

        nb_matchs += 1

        try:
            if sport == "tennis":
                if is_home : 
                    victoires += 1
                else : 
                    defaites += 1
                
            elif sport == "lol":
                winner = str(getattr(match, "winner", "")).strip().lower()
                b_name = str(getattr(match, "team_blue_name", getattr(match, "team_blue"
                                                                , ""))).strip().lower()
                
                team_won = (is_home and winner in [b_name, "blue", "team_blue"]) or \
                           (is_away and winner not in [b_name, "blue", "team_blue"])
                if team_won: victoires += 1
                else : 
                    defaites += 1
                
            elif sport in ["basketball", "football"]:
                # On récupère les scores (points ou buts)
                h_score = float(getattr(match, "home_team_score", getattr(match, 
                                                                "home_team_goal", 0)))
                a_score = float(getattr(match, "away_team_score", getattr(match, 
                                                                "away_team_goal", 0)))
                
                if h_score == a_score : 
                    nuls += 1
                elif (is_home and h_score > a_score) or (is_away and 
                                                         a_score > h_score): 
                    victoires += 1
                else : 
                    defaites += 1
                
        except Exception:
            continue

    if nb_matchs == 0:
        return f"Aucune statistique trouvée. Le joueur '{nom_joueur}' n'a joué aucun match ou est mal orthographié."

    win_rate = round((victoires / nb_matchs) * 100, 1)

    return {
        "joueur": vrai_nom,
        "sport": sport.capitalize(),
        "matchs_joues": nb_matchs,
        "victoires": victoires,
        "nuls": nuls,
        "defaites": defaites,
        "win_rate": f"{win_rate}%"
    }