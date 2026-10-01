# Projet RL — Apprentissage par renforcement appliqué à la robotique

Ce projet académique explore progressivement l'**apprentissage par renforcement** (Reinforcement Learning, RL), des premiers algorithmes tabulaires jusqu'à l'utilisation de réseaux de neurones et, à terme, à des applications en robotique.

Le **labyrinthe** est notre premier environnement d'expérimentation, pas la finalité du projet. Nous séparons donc les environnements des algorithmes pour pouvoir comparer différentes méthodes sur un même problème.

## Architecture actuelle

```text
reinforcement-learning-robotics/
├── src/
│   ├── environnements/
│   │   └── labyrinthe.py                # Grille, actions, transitions, récompenses
│   ├── algorithmes/
│   │   └── tabulaire/
│   │       └── q_learning.py            # Q-learning avec table explicite
│   └── visualisation/
│       └── simulation_labyrinthe.py     # Animation Tkinter réutilisable
├── experiences/
│   └── q_learning_tabulaire/
│       └── entrainement.py              # Création de l'agent et lancement de l'apprentissage
├── requirements.txt
├── README.md
└── .gitignore
```

Les répertoires Python utilisent les *namespace packages* de Python 3 : des fichiers `__init__.py` vides ne sont pas indispensables dans cette configuration. Lancer les commandes **depuis la racine du dépôt**.

## Première phase : Q-learning tabulaire

L'environnement initial est un labyrinthe carré **3 × 3, sans mur ni feu**. L'agent part de la case 0, cherche la dernière case et peut tenter de se déplacer en haut, en bas, à gauche ou à droite. Les actions qui sortent de la grille sont exclues de la liste des actions possibles : l'agent ne peut pas les choisir.

| Événement | Récompense |
|---|---:|
| Arrivée | +1 |
| Autre déplacement | −0,1 |

L'algorithme apprend une **table** donnant une valeur pour chaque couple (état, action), à l'aide de la mise à jour de Bellman :

```text
Q(s,a) <- Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))
```

L'état final n'a pas de valeur future. La sélection des actions utilise une stratégie **epsilon-greedy** avec décroissance de l'exploration.

Les hyperparamètres sont indiqués explicitement dans l'unique script d'expérience (et non fixés par défaut dans la classe `QLearning`). Dans cet exemple : `alpha=0.1`, `gamma=0.9`, `epsilon=1.0`, `epsilon_min=0.05`, `decroissance=0.99`, `nb_episodes=1000` et `max_pas=30`. L'environnement fournit `nb_etats`, `nb_actions`, `reset()`, `actions_possibles(etat)` et `step(action)`.

## Déroulement d'un épisode d'apprentissage

Le fichier `experiences/q_learning_tabulaire/entrainement.py` crée le labyrinthe et l'agent, puis lance `agent.apprendre()` (mode classique) ou ouvre Tkinter (option `--visuel`). Les deux modes utilisent le même générateur `agent.apprendre_pas_a_pas()`, défini dans `q_learning.py` : en mode classique, `apprendre()` consomme tous les événements sans affichage ; en mode visuel, Tkinter les traite un par un. Un **épisode** correspond à une partie, depuis le départ jusqu'à sa fin.

1. **Réinitialisation — `etat = self.env.reset()`**  
   L'agent demande à l'environnement de replacer le robot au départ (case 0 pour notre grille 3 × 3). Le score cumulé de cet épisode est initialisé à zéro.

2. **Choix d'une action — `action = self.choisir_action(etat)`**  
   L'agent interroge l'environnement sur les actions autorisées et applique la stratégie *epsilon-greedy* : soit une action aléatoire (exploration), soit la meilleure action connue dans sa table Q (exploitation).

3. **Exécution du déplacement — `nouvel_etat, recompense, termine = self.env.step(action)`**  
   Le labyrinthe exécute l'action choisie et renvoie trois informations : la nouvelle case, la récompense obtenue et un booléen indiquant si l'arrivée est atteinte. Par exemple, descendre de la case 0 à la case 3 renvoie `(3, -0.1, False)`.

4. **Apprentissage — mise à jour de la table Q par Bellman**  
   L'agent calcule la meilleure valeur future parmi les actions autorisées au nouvel état (valeur nulle si l'épisode est terminé), puis corrige **une seule case**, `Q[etat, action]`, selon la formule présentée plus haut.

5. **Répétition ou fin de l'épisode**  
   L'agent ajoute la récompense au score cumulé, remplace `etat` par `nouvel_etat`, puis choisit une autre action. L'épisode s'arrête lorsque l'arrivée est atteinte, qu'aucune action n'est possible ou que le nombre maximal de déplacements (`max_pas`) est atteint.

**Après chaque épisode :** le score cumulé est enregistré dans `self.recompenses` et la probabilité d'exploration `epsilon` diminue progressivement sans passer sous `epsilon_min`. Un nouvel épisode repart ensuite de la case de départ. Dans notre exemple, ce processus est répété `nb_episodes = 1000` fois.

**Répartition des rôles :** `Labyrinthe` gère les règles et les déplacements ; `QLearning` choisit les actions et actualise les connaissances de l'agent.

## Installation

Prérequis : Python 3 et Tkinter (généralement inclus dans Python sur Windows).

```bash
git clone https://github.com/Alaxouche/reinforcement-learning-robotics.git
cd reinforcement-learning-robotics
python -m pip install -r requirements.txt
```

## Exécution

Pour lancer l'entraînement classique, sans fenêtre :

```bash
py -m experiences.q_learning_tabulaire.entrainement
```

Pour ouvrir **la fenêtre pédagogique avec les deux modes** (sans changer les hyperparamètres) :

```bash
py -m experiences.q_learning_tabulaire.entrainement --visuel
```

### Fonctionnement de l'animation Tkinter

**Mode 1 — Entraînement en direct :** les boutons « Pas suivant », « Lecture auto » et « Pause » permettent de suivre chaque événement du générateur. La fenêtre affiche la case du robot, le numéro de l'épisode et du pas, l'action retenue, la récompense, le score cumulé, epsilon, la cible de Bellman et **Q avant / Q après**. La table Q et le journal des décisions se mettent à jour progressivement. Le réglage du délai accélère ou ralentit la lecture automatique. Une fin d'épisode apparaît également dans le journal. L'interface reste réactive grâce à `fenetre.after()`.

**Mode 2 — Parcours après apprentissage :** une fois les épisodes terminés, le bouton « Parcours appris » devient disponible. Le robot repart du départ et suit `agent.meilleure_action(etat)` à chaque déplacement, sans exploration et **sans modifier la table Q**. On peut avancer manuellement, laisser défiler automatiquement, mettre en pause ou recommencer le parcours. La visualisation utilise le **même agent entraîné** : aucun second entraînement n'est lancé.

La fonction Tkinter est conservée dans `src/visualisation/simulation_labyrinthe.py` pour séparer les calculs du Q-learning de l'affichage.

## Progression envisagée

| Phase | Sujet | Statut |
|---|---|---|
| 1 | Q-learning **tabulaire** sur labyrinthe simple | Première version disponible |
| 2 | Environnements avec murs, feux, obstacles et mesures de performance | À développer |
| 3 | **Deep Q-Network (DQN)** : un réseau de neurones approxime les valeurs `Q(s,a; θ)` à la place d'une table explicite | À développer |
| 4 | Navigation dans des environnements plus complexes et robotique simulée | À développer |

À mesure que le projet progressera, les nouveaux algorithmes seront ajoutés dans `src/algorithmes/` (par exemple `profond/dqn.py`) et leurs protocoles dans `experiences/`. **Aucun fichier DQN fictif n'est créé à ce stade.**

> Les modifications pédagogiques de cette version sont effectuées sur la branche `hammou-qlearning`, indépendamment de `main`.
