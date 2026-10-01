# Projet RL — Apprentissage par renforcement appliqué à la robotique

Ce projet académique étudie les algorithmes d'**apprentissage par renforcement (Reinforcement Learning, RL)**, depuis des environnements élémentaires jusqu'à des applications envisagées en **navigation et robotique autonome**.

Notre premier cas d'étude est la résolution d'un labyrinthe discret par **Q-learning**. Le code sépare volontairement les environnements, les agents, la visualisation et les scripts d'expérience afin de permettre l'ajout progressif de nouveaux problèmes.

## Organisation

```text
reinforcement-learning-robotics/
├── src/
│   ├── environnements/
│   │   └── labyrinthe.py            # Définition des états, actions et récompenses
│   ├── agents/
│   │   └── q_learning.py            # Algorithme générique de Q-learning
│   └── visualisation/
│       └── simulation_labyrinthe.py # Affichage animé avec Tkinter
├── experiences/
│   ├── labyrinthe_3x3.py            # Entraînement et résultats de base
│   └── simulation_labyrinthe_3x3.py # Lancement de l'animation
├── results/
│   ├── figures/
│   └── animations/
├── docs/
├── requirements.txt
└── README.md
```

Chaque sous-dossier Python est un package. Les commandes ci-dessous sont à exécuter **depuis la racine du dépôt**.

## Première expérience : labyrinthe 3 × 3

La classe `Labyrinthe` définit une grille carrée, un départ à l'état `0` et une arrivée au dernier état. L'agent dispose des actions **haut, bas, gauche, droite**. Une action qui sort de la grille laisse l'agent sur place.

La version de départ **ne contient pas encore de murs ni de feux** ; les attributs `murs` et `feux` sont prévus pour de futurs environnements. Les récompenses sont :

| Événement | Récompense |
|---|---:|
| Arrivée atteinte | +1 |
| Autre déplacement | −0,1 |

Le Q-learning estime une valeur pour chaque couple état-action selon la mise à jour de Bellman :

```text
Q(s,a) <- Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))
```

À l'arrivée, la cible vaut simplement `r`, car l'état est terminal. Le choix des actions suit une politique **epsilon-greedy** : l'exploration est importante au départ puis diminue au fil des épisodes.

### Paramètres par défaut

| Paramètre | Valeur | Rôle |
|---|---:|---|
| `alpha` | 0.1 | Taux d'apprentissage |
| `gamma` | 0.9 | Importance du futur |
| `epsilon_debut` | 1.0 | Exploration initiale |
| `epsilon_min` | 0.05 | Exploration minimale |
| `decroissance` | 0.99 | Décroissance d'epsilon par épisode |
| `nb_episodes` | 500 | Nombre d'épisodes |
| `max_pas` | 50 | Nombre maximal de pas par épisode |
| `graine` | 0 | Reproductibilité des tirages |

Ces paramètres peuvent être changés lors de la création de `QLearning(lab, ...)`.

## Installation

Prérequis : **Python 3** (Tkinter est généralement fourni avec Python sur Windows).

```bash
 git clone https://github.com/Alaxouche/qlearning-labyrinthe-3x3.git
 cd qlearning-labyrinthe-3x3
 python -m pip install -r requirements.txt
```

> Le nom affiché du projet a changé ; l'adresse du dépôt reste inchangée tant que son propriétaire ne le renomme pas sur GitHub.

## Lancer les expériences

**Afficher la table Q et le chemin appris :**

```bash
python -m experiences.labyrinthe_3x3
```

**Ouvrir la simulation graphique :**

```bash
python -m experiences.simulation_labyrinthe_3x3
```

La fenêtre Tkinter propose **Démarrer** pour visualiser le parcours de l'agent entraîné, et **Recommencer** pour revenir au départ.

## Roadmap

- [x] Environnement carré simple et paramétrable
- [x] Agent Q-learning avec exploration epsilon-greedy
- [x] Table Q, extraction du chemin et animation Tkinter
- [ ] Labyrinthes avec murs, obstacles et pénalités
- [ ] Étude des hyperparamètres et courbes d'apprentissage
- [ ] Environnements de navigation plus complexes
- [ ] Expérimentations orientées robotique

Les étapes non cochées sont des perspectives, **pas des fonctionnalités déjà implémentées**.
