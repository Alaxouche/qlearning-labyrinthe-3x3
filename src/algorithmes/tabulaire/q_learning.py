import numpy as np


class QLearning:
    """Q-learning tabulaire indépendant de l'environnement étudié.

    Interface attendue :
      - env.nb_etats : nombre entier d'états
      - env.nb_actions : nombre entier d'actions
      - env.reset() : retourne l'état initial
      - env.step(action) : retourne (état_suivant, récompense, terminé)
      - env.actions_possibles(etat) : optionnel, retourne les actions autorisées
    Les états et les actions sont numérotés à partir de 0.
    """

    def __init__(
        self,
        environnement,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        epsilon_min=0.05,
        decroissance=0.99,
        nb_episodes=1000,
        max_pas=200,
        graine=0
    ):
        # Environnement et paramètres d'apprentissage
        self.env = environnement
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.decroissance = decroissance
        self.nb_episodes = nb_episodes
        self.max_pas = max_pas

        # Générateur aléatoire reproductible
        self.rng = np.random.default_rng(graine)

        # Une ligne par état et une colonne par action
        self.Q = np.zeros((self.env.nb_etats, self.env.nb_actions))

        # Récompense cumulée obtenue pendant chaque épisode
        self.recompenses = []

    def actions_possibles(self, etat):
        """Récupère les actions autorisées par l'environnement."""
        if hasattr(self.env, "actions_possibles"):
            return list(self.env.actions_possibles(etat))
        return list(range(self.env.nb_actions))

    def meilleure_action(self, etat):
        """Choisit au hasard parmi les actions ayant la Q-value maximale."""
        actions = self.actions_possibles(etat)

        if not actions:
            raise ValueError("Aucune action possible dans cet état.")

        maximum = np.max(self.Q[etat, actions])
        meilleures = [a for a in actions if np.isclose(self.Q[etat, a], maximum)]
        return int(self.rng.choice(meilleures))

    def choisir_action(self, etat):
        """Politique epsilon-greedy : exploration ou exploitation."""
        actions = self.actions_possibles(etat)

        if not actions:
            raise ValueError("Aucune action possible dans cet état.")

        if self.rng.random() < self.epsilon:
            return int(self.rng.choice(actions))

        return self.meilleure_action(etat)

    def apprendre(self):
        """Entraîne la table Q par interaction avec l'environnement."""
        self.recompenses = []

        for episode in range(self.nb_episodes):
            etat = self.env.reset()
            recompense_totale = 0.0

            for pas in range(self.max_pas):
                action = self.choisir_action(etat)
                suivant, recompense, termine = self.env.step(action)

                # Un état terminal ne possède pas de récompense future.
                if termine:
                    cible = recompense
                else:
                    actions_futures = self.actions_possibles(suivant)
                    valeur_future = np.max(self.Q[suivant, actions_futures]) if actions_futures else 0.0
                    cible = recompense + self.gamma * valeur_future

                # Mise à jour de Bellman
                self.Q[etat, action] += self.alpha * (cible - self.Q[etat, action])

                etat = suivant
                recompense_totale += recompense

                if termine or (not self.actions_possibles(etat)):
                    break

            self.recompenses.append(recompense_totale)
            self.epsilon = max(self.epsilon_min, self.epsilon * self.decroissance)

        return self.Q

    def politique(self):
        """Retourne la meilleure action connue pour chaque état."""
        resultat = {}

        for etat in range(self.env.nb_etats):
            actions = self.actions_possibles(etat)
            resultat[etat] = self.meilleure_action(etat) if actions else None

        return resultat
