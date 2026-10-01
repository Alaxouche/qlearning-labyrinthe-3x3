"""Première expérience : apprentissage sur un labyrinthe 3 x 3."""
from src.environnements.labyrinthe import Labyrinthe
from src.algorithmes.tabulaire.q_learning import QLearning


def main():
    lab = Labyrinthe(3)
    agent = QLearning(lab)
    agent.apprendre()
    agent.afficher_q()
    print("\nChemin :", agent.chemin())


if __name__ == "__main__":
    main()
