def calculer_stats_joueur(nom_joueur: str, sport: str, matchs: list):
    """
    Parcourt les matchs pour trouver le joueur et calcule son bilan.
    """
    nom_recherche = nom_joueur.strip().lower()
    nb_matchs = victoires = defaites = nuls = 0
    vrai_nom = nom_joueur

    for match in matchs:
        is_home = False
        is_away = False

        # 1. On cherche le joueur dans l'équipe Home (recherche partielle)
        for p_home in getattr(match, "list_home_player", []):
            if nom_recherche in str(p_home).lower():
                is_home = True
                vrai_nom = str(p_home) # On récupère la belle orthographe
                break
                
        # 2. On cherche le joueur dans l'équipe Away
        for p_away in getattr(match, "list_away_player", []):
            if nom_recherche in str(p_away).lower():
                is_away = True
                vrai_nom = str(p_away)
                break

        # Si le joueur n'est pas dans ce match, on passe au suivant
        if not is_home and not is_away:
            continue

        nb_matchs += 1

        # 3. Calcul de la victoire selon le sport
        try:
            if sport == "tennis":
                # Au tennis, le gagnant est toujours mis dans Home par notre Loader
                if is_home: victoires += 1
                else: defaites += 1
                
            elif sport == "lol":
                winner = str(getattr(match, "winner", "")).strip().lower()
                b_name = str(getattr(match, "team_blue_name", getattr(match, "team_blue", ""))).strip().lower()
                
                team_won = (is_home and winner in [b_name, "blue", "team_blue"]) or \
                           (is_away and winner not in [b_name, "blue", "team_blue"])
                if team_won: victoires += 1
                else: defaites += 1
                
            elif sport in ["basketball", "football"]:
                # On récupère les scores (points ou buts)
                h_score = float(getattr(match, "home_team_score", getattr(match, "home_team_goal", 0)))
                a_score = float(getattr(match, "away_team_score", getattr(match, "away_team_goal", 0)))
                
                if h_score == a_score: nuls += 1
                elif (is_home and h_score > a_score) or (is_away and a_score > h_score): victoires += 1
                else: defaites += 1
                
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