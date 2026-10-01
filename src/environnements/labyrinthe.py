class Labyrinthe:
    """Décrit les règles d'une grille carrée, indépendamment du Q-learning.

    'self' désigne ici l'objet Labyrinthe (et non l'objet QLearning).
    Les cases sont numérotées de 0 à taille*taille - 1, ligne par ligne.
    """

    def __init__(self, taille=3):
        """Crée une grille de taille x taille. Retour : aucun."""
        # Attributs propres à CE labyrinthe : 'self' permet de les réutiliser.
        self.taille = taille
        self.nb_etats = taille * taille

        # Première case = départ, dernière case = objectif.
        self.depart = 0
        self.arrivee = self.nb_etats - 1

        # Actions : 0=haut, 1=bas, 2=gauche, 3=droite.
        # Chaque paire indique (variation de ligne, variation de colonne).
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.noms_actions = ["Haut", "Bas", "Gauche", "Droite"]
        self.nb_actions = len(self.actions)

        #aucun obstacle pour l'instant.
        self.murs = []
        self.feux = []

        # Position courante du robot : le labyrinthe la mémorise lui-même.
        self.etat = self.depart

    def reset(self):
        """Recommence un épisode : position du robot = départ.

        Retour : int, numéro de la case de départ.
        QLearning appelle cette méthode au début de chaque épisode.
        """
        self.etat = self.depart
        return self.etat

    def actions_possibles(self, etat):
        """Cherche les déplacements autorisés depuis la case 'etat'.

        Paramètre : etat (int), numéro de la case à examiner.
        Retour : list[int], numéros des actions autorisées (pas des cases !).
        Exemple au coin supérieur gauche : [1, 3] = bas, droite.
        """
        # L'arrivée termine l'épisode ; une case mur n'est pas traversable.
        if etat == self.arrivee or etat in self.murs:
            return []

        # divmod donne (quotient, reste) : numéro de case -> (ligne, colonne).
        # Exemple : divmod(5, 3) donne (1, 2).
        ligne, colonne = divmod(etat, self.taille)
        possibles = []  # On ajoutera les numéros des déplacements valides.

        # On essaie successivement haut, bas, gauche et droite.
        for action in range(self.nb_actions):
            dl, dc = self.actions[action]  # Variation de ligne et de colonne.
            nouvelle_ligne, nouvelle_colonne = ligne + dl, colonne + dc

            # Le déplacement doit rester à l'intérieur de la grille.
            if 0 <= nouvelle_ligne < self.taille and 0 <= nouvelle_colonne < self.taille:
                suivant = nouvelle_ligne * self.taille + nouvelle_colonne

                # On accepte aussi seulement les cases qui ne sont pas des murs.
                if suivant not in self.murs:
                    possibles.append(action)  # Ajouter l'ACTION, pas la case suivante.

        return possibles  # Exemple : [1, 3] = bas et droite.

    def etat_suivant(self, etat, action):
        """Calcule la case après une action, sans modifier self.etat.

        Paramètres : etat (int), action (int).
        Retour : int, numéro de la case atteinte ; état inchangé si interdit.
        """
        if action not in self.actions_possibles(etat):
            return etat

        ligne, colonne = divmod(etat, self.taille)
        dl, dc = self.actions[action]

        # Conversion des nouvelles coordonnées en numéro de case.
        return (ligne + dl) * self.taille + (colonne + dc)

    def recompense(self, etat):
        """Calcule la récompense associée à une case.

        Paramètre : etat (int), numéro de la case atteinte.
        Retour : float, +1.0 à la sortie et -0.1 sinon.
        """
        return 1.0 if etat == self.arrivee else -0.1

    def step(self, action):
        """Effectue un déplacement et mémorise la nouvelle position.

        Paramètre : action (int), numéro de l'action choisie par QLearning.
        Retour : (nouvel_etat, recompense, termine) = (int, float, bool).
        'termine' vaut True si le robot atteint l'arrivée.
        """
        # Une action interdite ne doit pas être exécutée.
        if action not in self.actions_possibles(self.etat):
            raise ValueError("Cette action est impossible dans l'état actuel.")

        # IMPORTANT : c'est ici qu'on change réellement la position du robot.
        self.etat = self.etat_suivant(self.etat, action)
        recompense = self.recompense(self.etat)
        termine = self.etat == self.arrivee  # True ou False

        # Ces trois résultats seront récupérés par l'objet QLearning.
        return self.etat, recompense, termine
