import pandas as pd

def lire_donnees(nom_fichier):
    df = pd.read_csv(nom_fichier, encoding='utf-8')
    print(f"Lecture réussie : le tableau contient {len(df)} lignes de données.")
    
    return df

def ajouter_donnees(nom_fichier, nouvelles_donnees):
    df_nouveau = pd.DataFrame([nouvelles_donnees])
        df_nouveau.to_csv(nom_fichier, mode='a', header=False, index=False, encoding='utf-8')
        print("Nouvelles données ajoutées avec succès.")

