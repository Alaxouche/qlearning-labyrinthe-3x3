"""Crée l'environnement et l'agent, puis lance un entraînement Q-learning.

Depuis la racine du projet :
    py -m experiences.q_learning_tabulaire.entrainement
    py -m experiences.q_learning_tabulaire.entrainement --visuel
"""

from src.environnements.labyrinthe import Labyrinthe
from src.algorithmes.tabulaire.q_learning import QLearning


def main(visuel=False):
    """Construit l'agent ; entraîne normalement ou ouvre le suivi Tkinter."""

    # 1. Création de l'environnement dans lequel l'agent va apprendre.
    lab = Labyrinthe(taille=3)

    # 2. Création de l'agent : les hyperparamètres de cette expérience
    # sont définis ici et non dans la classe générique QLearning.
    agent = QLearning(
        environnement=lab,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        epsilon_min=0.05,
        decroissance=0.99,
        nb_episodes=1000,
        max_pas=30
    )

    # 3. Un seul jeu d'hyperparamètres pour les deux modes.
    if visuel:
        # La fenêtre gère elle-même les pas de l'entraînement en direct.
        from src.visualisation.simulation_labyrinthe import lancer_simulation
        lancer_simulation(lab, agent)
    else:
        # Mode classique, sans interface graphique.
        agent.apprendre()

    # Permet de récupérer l'agent entraîné si main() est appelée ailleurs.
    return agent


if __name__ == "__main__":
    import sys
    main(visuel="--visuel" in sys.argv)
