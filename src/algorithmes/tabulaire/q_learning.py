import numpy as np


class QLearning:
    """Q-learning tabulaire pour un environnement à états et actions finis."""

    def __init__(self, environnement, alpha=0.1, gamma=0.9, epsilon=1.0,
                 epsilon_min=0.05, decroissance=0.99, nb_episodes=1000, max_pas=200):

        # Paramètres de notre agent
        self.env = environnement
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decroissance = decroissance
        self.nb_episodes = nb_episodes
        self.max_pas = max_pas

        # Table Q : une ligne par état, une colonne par action
        self.Q = np.zeros((self.env.nb_etats, self.env.nb_actions))

        # Récompense totale de chaque épisode
        self.recompenses = []

    def meilleure_action(self, etat):
        """Renvoie l'action autorisée ayant la meilleure Q-value."""
        actions = list(self.env.actions_possibles(etat))
        if not actions:
            raise ValueError("Aucune action possible dans cet état.")
        indice = np.argmax(self.Q[etat, actions])
        return int(actions[indice])

    def choisir_action(self, etat):
        """Explore au hasard avec probabilité epsilon, sinon exploite Q."""
        actions = list(self.env.actions_possibles(etat))
        if not actions:
            raise ValueError("Aucune action possible dans cet état.")

        if np.random.random() < self.epsilon:
            return int(np.random.choice(actions))

        return self.meilleure_action(etat)

    def apprendre(self):
        """Met à jour la table Q au fil des épisodes."""
        self.recompenses = []

        for episode in range(self.nb_episodes):
            etat = self.env.reset()
            total = 0.0

            for pas in range(self.max_pas):
                action = self.choisir_action(etat)
                nouvel_etat, recompense, termine = self.env.step(action)

                # La valeur future est nulle si l'épisode est terminé.
                if termine:
                    valeur_future = 0.0
                else:
                    actions_futures = list(self.env.actions_possibles(nouvel_etat))
                    if actions_futures:
                        valeur_future = np.max(self.Q[nouvel_etat, actions_futures])
                    else:
                        valeur_future = 0.0

                # Formule du Q-learning (Bellman)
                cible = recompense + self.gamma * valeur_future
                self.Q[etat, action] += self.alpha * (cible - self.Q[etat, action])

                total += recompense
                etat = nouvel_etat

                if termine or (not self.env.actions_possibles(etat)):
                    break

            self.recompenses.append(total)
            self.epsilon = max(self.epsilon_min, self.epsilon * self.decroissance)

        return self.Q
