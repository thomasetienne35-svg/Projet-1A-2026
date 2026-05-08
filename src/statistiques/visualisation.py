from typing import Any

import matplotlib.pyplot as plt
import numpy as np


class VisualisationComparateur:
    """Service de visualisation pour comparer graphiquement des entités (joueurs ou équipes)."""

    def __init__(self) -> None:
        self.figsize = (10, 6)
        self.largeur_barre = 0.35

    def comparer_joueurs(self, stats_j1: dict[str, Any], stats_j2: dict[str, Any]) -> None:
        """Génère et sauvegarde un diagramme en bâtons comparant les statistiques de deux joueurs."""
        nom1, nom2 = stats_j1["joueur"], stats_j2["joueur"]
        labels = ['Matchs Joués', 'Victoires', 'Défaites', 'Win Rate (%)']
        
        wr1 = float(stats_j1["win_rate"].replace('%', ''))
        wr2 = float(stats_j2["win_rate"].replace('%', ''))
        
        valeurs_j1 = [stats_j1["matchs_joues"], stats_j1["victoires"], stats_j1["defaites"], wr1]
        valeurs_j2 = [stats_j2["matchs_joues"], stats_j2["victoires"], stats_j2["defaites"], wr2]
        
        x = np.arange(len(labels))
        
        fig, ax = plt.subplots(figsize=self.figsize)
        barres1 = ax.bar(x - self.largeur_barre/2, valeurs_j1, self.largeur_barre, label=nom1, color='#4A90E2')
        barres2 = ax.bar(x + self.largeur_barre/2, valeurs_j2, self.largeur_barre, label=nom2, color='#E94A47')
        
        ax.set_ylabel('Statistiques', fontweight='bold')
        ax.set_title(f'Comparaison Joueurs : {nom1} vs {nom2} ({stats_j1["sport"]})', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.bar_label(barres1, padding=3)
        ax.bar_label(barres2, padding=3)
        fig.tight_layout()
        
        nom_fichier = "comparaison_joueurs.png"
        plt.savefig(nom_fichier, bbox_inches='tight')
        plt.close()
        print(f"\n✅ Graphique généré avec succès ! Double-cliquez sur '{nom_fichier}' dans l'explorateur à gauche pour le voir.")

    def comparer_equipes(self, stats_e1: dict[str, Any], stats_e2: dict[str, Any]) -> None:
        """Génère et sauvegarde un diagramme en bâtons comparant les performances de deux équipes."""
        nom1, nom2 = stats_e1.get("equipe", "Eq1"), stats_e2.get("equipe", "Eq2")
        
        pour_e1 = stats_e1.get("buts_pour", stats_e1.get("buts_marques", 
                            stats_e1.get("points_pour", stats_e1.get("points_marques", 0))))
        pour_e2 = stats_e2.get("buts_pour", stats_e2.get("buts_marques", 
                            stats_e2.get("points_pour", stats_e2.get("points_marques", 0))))
        
        contre_e1 = stats_e1.get("buts_contre", stats_e1.get("buts_encaisses", 
                        stats_e1.get("points_contre", stats_e1.get("points_encaisses", 0))))
        contre_e2 = stats_e2.get("buts_contre", stats_e2.get("buts_encaisses", 
                        stats_e2.get("points_contre", stats_e2.get("points_encaisses", 0))))

        labels = ['Matchs', 'Victoires', 'Défaites', 'Marqués', 'Encaissés']
        
        valeurs_e1 = [stats_e1.get("matchs_joues", 0), stats_e1.get("victoires", 0), 
                      stats_e1.get("defaites", 0), pour_e1, contre_e1]
        valeurs_e2 = [stats_e2.get("matchs_joues", 0), stats_e2.get("victoires", 0), 
                      stats_e2.get("defaites", 0), pour_e2, contre_e2]
        
        x = np.arange(len(labels))
        
        fig, ax = plt.subplots(figsize=self.figsize)
        barres1 = ax.bar(x - self.largeur_barre/2, valeurs_e1, self.largeur_barre, label=nom1, color='#2ecc71')
        barres2 = ax.bar(x + self.largeur_barre/2, valeurs_e2, self.largeur_barre, label=nom2, color='#f1c40f')
        
        ax.set_ylabel('Statistiques', fontweight='bold')
        ax.set_title(f'Comparaison Équipes : {nom1} vs {nom2}', fontsize=14, 
                     fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.bar_label(barres1, padding=3)
        ax.bar_label(barres2, padding=3)
        fig.tight_layout()
        
        nom_fichier = "comparaison_equipes.png"
        plt.savefig(nom_fichier, bbox_inches='tight')
        plt.close()
        print(f"\n✅ Graphique généré avec succès ! Double-cliquez sur '{nom_fichier}' dans l'explorateur à gauche pour le voir.")