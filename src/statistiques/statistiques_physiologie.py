from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from sport import Sport
from .match_par_joueur import PlayerStatsCalculator


class AnalysePhysiologique:
    """Classe responsable de l'analyse et de la visualisation des données morphologiques des joueurs."""
    
    def __init__(self, liste_joueurs: list[Any], sport: Sport) -> None:
        self.liste_joueurs = liste_joueurs
        self.sport = sport

    def _extraire_tailles(self) -> list[float]:
        """Méthode interne pour chercher, nettoyer et convertir toutes les tailles.

        Returns:
        -------
        list[float]
            Une liste de tailles converties en cm.
        """
        tailles = []
        for p in self.liste_joueurs:
            h_brut = getattr(p, "height", getattr(p, "taille", getattr(p, "size", 0)))
            
            if h_brut is None or str(h_brut).strip() in ["", "nan", "None"]:
                continue

            h_str = str(h_brut).replace('"', '').replace(',', '.').strip()
            
            try:
                if "-" in h_str or "'" in h_str:
                    parts = h_str.replace("'", "-").split("-")
                    if len(parts) == 2:
                        pieds = float(parts[0])
                        pouces = float(parts[1])
                        #1 pied = 30.48 cm, 1 pouce = 2.54 cm
                        h_cm = (pieds * 30.48) + (pouces * 2.54)
                        if h_cm > 140:
                            tailles.append(h_cm)
                    continue

                h = float(h_str)
                
                if 0 < h < 3: 
                    h = h * 100
                elif 50 < h < 100:
                    h = h * 2.54
                    
                if h > 140:  
                    tailles.append(h)
                    
            except (ValueError, TypeError):
                continue
                
        return tailles

    def generer_graphique_taille(self) -> None:
        """Génère l'histogramme des tailles et le sauvegarde."""
        tailles = self._extraire_tailles()

        if not tailles:
            print(f"\n❌ Aucune donnée de taille valide trouvée pour : {self.sport.name.capitalize()}")
            return

        plt.figure(figsize=(10, 6))
        
        # Création de l'histogramme
        plt.hist(tailles, bins=15, color='#3498db', edgecolor='white', alpha=0.8)
        
        plt.title(f"Distribution des tailles - {self.sport.name.capitalize()}", fontsize=14, 
                  fontweight='bold')
        plt.xlabel("Taille (cm)", fontweight='bold')
        plt.ylabel("Nombre de joueurs", fontweight='bold')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Calcul et affichage de la moyenne
        moyenne = np.mean(tailles)
        plt.axvline(moyenne, color='red', linestyle='dashed', linewidth=2, 
                    label=f'Moyenne: {moyenne:.1f} cm')
        plt.legend()

        plt.tight_layout()

        # Sauvegarde
        nom_fichier = f"distribution_taille_{self.sport.name.lower()}.png"
        plt.savefig(nom_fichier)
        plt.close()
        
        print(f"\n✅ Analyse terminée ! Taille moyenne : {moyenne:.1f} cm.")
        print(f"👉 Le graphique a été sauvegardé sous : '{nom_fichier}'")

    def generer_heatmap_taille_victoire(self, matchs: list[Any]) -> None:
        """Croise la taille des joueurs avec leur Win Rate pour générer une Heatmap.

        Parameters
        ----------
        matchs : list[Any]
            La liste des matchs pour calculer le Win Rate de chaque joueur.
        """
        print("\n⏳ Calcul des Win Rates pour tous les joueurs... " \
              "Cela peut prendre quelques secondes.")
        
        tailles_valides = []
        win_rates_valides = []

        calculateur = PlayerStatsCalculator(self.sport, matchs)

        for p in self.liste_joueurs:
            h_brut = getattr(p, "height", getattr(p, "taille", getattr(p, "size", 0)))
            if h_brut is None or str(h_brut).strip() in ["", "nan", "None"]: continue
            h_str = str(h_brut).replace('"', '').replace(',', '.').strip()
            
            h_cm = None
            try:
                if "-" in h_str or "'" in h_str:
                    parts = h_str.replace("'", "-").split("-")
                    if len(parts) == 2:
                        h_cm = (float(parts[0]) * 30.48) + (float(parts[1]) * 2.54)
                else:
                    h = float(h_str)
                    if 0 < h < 3 : 
                        h = h * 100
                    elif 50 < h < 100 : 
                        h = h * 2.54
                    h_cm = h
            except (ValueError, TypeError):
                continue
                
            if h_cm and h_cm > 140:
                nom_joueur = str(getattr(p, "prenom_nom", getattr(p, "name", "")))
                if not nom_joueur: continue
                
                stats = calculateur.obtenir_bilan(nom_joueur)
                
                if not isinstance(stats, str): 
                    if stats.get("matchs_joues", 0) >= 3:
                        wr_str = stats.get("win_rate", "0%")
                        wr_float = float(wr_str.replace("%", ""))
                        
                        tailles_valides.append(h_cm)
                        win_rates_valides.append(wr_float)

        if not tailles_valides:
            print("\n❌ Pas assez de données croisées (Taille + " \
                  "Minimum 3 matchs joués) pour générer la Heatmap.")
            return

        plt.figure(figsize=(10, 6))
        
        heatmap = plt.hexbin(tailles_valides, win_rates_valides, gridsize = 15, 
                             cmap='YlOrRd', mincnt=1)
        
        # Barre de légende sur le côté
        cbar = plt.colorbar(heatmap)
        cbar.set_label('Concentration de joueurs', rotation = 270, labelpad = 15)
        
        plt.title(f"Heatmap : Taille vs Win Rate - {self.sport.name.capitalize()}", 
                  fontsize = 14, fontweight='bold')
        plt.xlabel("Taille (cm)", fontweight='bold')
        plt.ylabel("Win Rate (%)", fontweight='bold')
        plt.grid(alpha = 0.3)
        
        plt.tight_layout()
        nom_fichier = f"heatmap_taille_wr_{self.sport.name.lower()}.png"
        plt.savefig(nom_fichier)
        plt.close()
        
        print("\n✅ Heatmap générée avec succès !")
        print(f"👉 Le graphique a été sauvegardé sous : '{nom_fichier}'")