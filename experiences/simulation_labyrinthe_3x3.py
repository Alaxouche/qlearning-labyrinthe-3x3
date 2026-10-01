"""Visualisation de la première expérience (labyrinthe 3 x 3)."""
from src.environnements.labyrinthe import Labyrinthe
from src.agents.q_learning import QLearning
from src.visualisation.simulation_labyrinthe import lancer_simulation


def main():
    lab = Labyrinthe(3)
    agent = QLearning(lab)
    lancer_simulation(lab, agent)


if __name__ == "__main__":
    main()
