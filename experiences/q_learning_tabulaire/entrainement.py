"""Exemple : entraîner notre Q-learning tabulaire sur une grille 3 x 3."""

from src.environnements.labyrinthe import Labyrinthe
from src.algorithmes.tabulaire.q_learning import QLearning


def main():
    # 1. Création du problème : un labyrinthe de taille 3 x 3
    lab = Labyrinthe(taille=3)

    # 2. Création de l'agent : les paramètres sont fixés ici, pas dans la classe.
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

    # 3. Entraînement : la matrice Q se remplit progressivement.
    agent.apprendre()

    # 4. Affichage lisible de la table Q
    print("État    Haut      Bas    Gauche   Droite")
    for etat in range(lab.nb_etats):
        valeurs = " ".join(f"{valeur:8.3f}" for valeur in agent.Q[etat])
        print(f"{etat:>4} {valeurs}")

    # 5. Test : l'agent suit uniquement les meilleures actions apprises.
    etat = lab.reset()
    chemin = [etat]

    for pas in range(agent.max_pas):
        if etat == lab.arrivee:
            break

        action = agent.meilleure_action(etat)
        etat, recompense, termine = lab.step(action)
        chemin.append(etat)

        if termine:
            break

    print("\nChemin suivi :", " -> ".join(map(str, chemin)))


if __name__ == "__main__":
    main()
