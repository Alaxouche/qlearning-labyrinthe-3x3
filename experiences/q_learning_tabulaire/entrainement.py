"""Point de départ de l'expérience : création du labyrinthe et de l'agent.

Commande depuis la racine : py -m experiences.q_learning_tabulaire.entrainement
"""

from src.environnements.labyrinthe import Labyrinthe
from src.algorithmes.tabulaire.q_learning import QLearning
from src.visualisation.simulation_labyrinthe import lancer_simulation


def main():
    """Entraîne une fois, affiche la table Q, le chemin et la simulation. Retour : aucun."""
    # 1. Création du problème : un labyrinthe de taille 3 x 3
    lab = Labyrinthe(taille=3)

    # 2. On TRANSMET l'objet lab à QLearning : dans sa classe, self.env = lab.
    # Les hyperparamètres de cette expérience sont définis ici, pas dans l'algorithme.
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

    # 3. Cette méthode fait interagir agent et lab, puis remplit agent.Q.
    agent.apprendre()

    # 4. Affichage lisible de la table Q
    print("État    Haut      Bas    Gauche   Droite")
    # On parcourt une ligne de Q par état ; les 4 colonnes sont les actions.
    for etat in range(lab.nb_etats):
        valeurs = " ".join(f"{valeur:8.3f}" for valeur in agent.Q[etat])
        print(f"{etat:>4} {valeurs}")

    # 5. Test : l'agent suit uniquement les meilleures actions apprises.
    etat = lab.reset()  # Réinitialiser le labyrinthe APRÈS l'entraînement.
    chemin = [etat]

    for pas in range(agent.max_pas):
        if etat == lab.arrivee:
            break

        action = agent.meilleure_action(etat)  # Plus d'exploration : on teste la politique apprise.
        etat, recompense, termine = lab.step(action)  # Le labyrinthe exécute le déplacement.
        chemin.append(etat)

        if termine:
            break

    print("\nChemin suivi :", " -> ".join(map(str, chemin)))

    # 6. Ouvrir la fenêtre avec le MÊME agent et sa table Q déjà entraînée.
    # On ne recrée pas QLearning et on ne relance pas apprendre().
    lancer_simulation(lab, agent)


# Ce bloc lance main() seulement si l'on exécute ce fichier comme programme.
if __name__ == "__main__":
    main()
