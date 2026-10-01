"""Crée l'environnement et l'agent, puis lance un entraînement Q-learning.

Depuis la racine du projet :
    py -m experiences.q_learning_tabulaire.entrainement
"""

from src.environnements.labyrinthe import Labyrinthe
from src.algorithmes.tabulaire.q_learning import QLearning


def main():
    """Construit et entraîne un agent sur un labyrinthe 3 x 3."""

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

    # 3. Entraînement : cette méthode modifie progressivement agent.Q.
    agent.apprendre()

    # Permet de récupérer l'agent entraîné si main() est appelée ailleurs.
    return agent


if __name__ == "__main__":
    main()
