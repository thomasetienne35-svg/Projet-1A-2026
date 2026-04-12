import sys
import os

sys.path.append(os.path.dirname(__file__))

from sport import Sport
from loaders_match.match_loader import MatchLoader


def main():
    sports_disponibles = ["football", "tennis", "volley", "basketball", "lol"]

    print("\n=== Sports disponibles ===")
    for i, s in enumerate(sports_disponibles, 1):
        print(f"{i}. {s}")

    choix = input("\nEntrez le numéro du sport : ")
    try:
        sport = Sport(sports_disponibles[int(choix) - 1])
    except (ValueError, IndexError):
        print("Sport invalide.")
        return

    print(f"\nChargement des matchs de {sport.name}...")
    try:
        matchs = MatchLoader().load_all_matches(sport)
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return

    print(f"\n=== Matchs disponibles ({sport.name}) ===")
    for i, match in enumerate(matchs, 1):
        print(f"{i}. Match ID: {match.id}")

    choix_match = input("\nEntrez le numéro du match : ")
    try:
        match = matchs[int(choix_match) - 1]
    except (ValueError, IndexError):
        print("Match invalide.")
        return

    print(f"\n=== Match ID: {match.id} ===")
    print(f"Sport : {match.sport.name}")
    print(f"Joueurs domicile : {[str(j) for j in match.list_home_player]}")
    print(f"Joueurs extérieur : {[str(j) for j in match.list_away_player]}")


if __name__ == "__main__":
    main()
