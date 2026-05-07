# Projet de Traitement de Données

Ce projet est une application de traitement de données développée en Python, reposant sur les principes de la Programmation Orientée Objet (POO). 

---

## Version de Python

- **Python :** Version **3.13.12** 

---

## Dépendances

Les paquets nécessaires pour exécuter cette application (ainsi que pour le développement) sont listés dans le fichier `requirements.txt` situé à la racine du projet.

**Dépendances :**
- `pandas == 2.1.0`
- `pytest == 7.4.2`

---

## Installation

Pour faire fonctionner ce projet sur votre machine locale, veuillez suivre les étapes ci-dessous. Elles incluent la création d'un environnement virtuel afin d'isoler les dépendances du projet. Ces commandes sont à exécuter dans le terminal.

```bash
# 1. Cloner le dépôt
git clone https://github.com/thomasetienne35-svg/Projet-1A-2026.git

# 2. Entrer dans le dossier du projet
cd Projet-1A-2026

# 3. Créer l'environnement virtuel (nommé .venv)
python -m venv .venv

# 4. Activer l'environnement virtuel
# - Si vous êtes sur Windows, utilisez la commande suivante à la place : .venv\Scripts\activate
source .venv/bin/activate

# 5. Installer les dépendances du projet
pip install -r requirements.txt

# 6. Lancer l'application
python -m src
```

---

---

##  Tests

Ce projet utilise `pytest` pour les tests unitaires. Pour exécuter l'ensemble des tests, assurez-vous d'être dans votre environnement virtuel et lancez la commande suivante depuis la racine du projet :

```bash
python -m pytest
```