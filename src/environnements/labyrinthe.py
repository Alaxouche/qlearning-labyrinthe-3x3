class Labyrinthe:
    """Environnement simple : grille carrée sans mur ni feu pour commencer."""

    def __init__(self, taille=3):
        self.taille = taille
        self.nb_etats = taille * taille
        self.depart = 0
        self.arrivee = self.nb_etats - 1

        # Les actions sont numérotées : 0=haut, 1=bas, 2=gauche, 3=droite
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.noms_actions = ["Haut", "Bas", "Gauche", "Droite"]
        self.nb_actions = len(self.actions)

        self.murs = []
        self.feux = []
        self.etat = self.depart

    def reset(self):
        """Replace le robot au départ et renvoie cet état (int)."""
        self.etat = self.depart
        return self.etat

    def actions_possibles(self, etat):
        """Renvoie les numéros des actions autorisées depuis etat (list[int])."""
        if etat == self.arrivee or etat in self.murs:
            return []

        ligne, colonne = divmod(etat, self.taille)
        possibles = []

        for action in range(self.nb_actions):
            dl, dc = self.actions[action]
            nouvelle_ligne, nouvelle_colonne = ligne + dl, colonne + dc

            # Pas de sortie de grille ni d'entrée dans un mur
            if 0 <= nouvelle_ligne < self.taille and 0 <= nouvelle_colonne < self.taille:
                suivant = nouvelle_ligne * self.taille + nouvelle_colonne
                if suivant not in self.murs:
                    possibles.append(action)

        return possibles

    def etat_suivant(self, etat, action):
        """Calcule la case atteinte ; une action impossible ne déplace pas le robot."""
        if action not in self.actions_possibles(etat):
            return etat

        ligne, colonne = divmod(etat, self.taille)
        dl, dc = self.actions[action]
        return (ligne + dl) * self.taille + (colonne + dc)

    def recompense(self, etat):
        """Renvoie +1 à l'arrivée et -0.1 sur une case ordinaire."""
        return 1.0 if etat == self.arrivee else -0.1

    def step(self, action):
        """Exécute une action et renvoie (nouvel_etat, recompense, termine)."""
        if action not in self.actions_possibles(self.etat):
            raise ValueError("Cette action est impossible dans l'état actuel.")

        self.etat = self.etat_suivant(self.etat, action)
        recompense = self.recompense(self.etat)
        termine = self.etat == self.arrivee
        return self.etat, recompense, termine
