class Labyrinthe:
    """Labyrinthe simple : une grille carree, sans mur ni feu.

    C'est le modele a suivre pour les autres labyrinthes. La classe QLearning n'utilise
    que ce qui est defini ici :
      - les attributs taille, nb_etats, depart, arrivee, actions, noms_actions
      - les methodes etat_suivant(etat, action) et recompense(etat)
    La simulation utilise en plus les listes murs et feux pour l'affichage.

    Pour un nouveau labyrinthe, on cree une classe fille qui remplit murs
    et/ou feux et qui redefinit etat_suivant et/ou recompense.
    """

    def __init__(self, taille=3):
        self.taille = taille
        self.nb_etats = taille * taille
        self.depart = 0
        self.arrivee = self.nb_etats - 1

        # Haut, Bas, Gauche, Droite : (deplacement en ligne, deplacement en colonne)
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.noms_actions = ["Haut", "Bas", "Gauche", "Droite"]

        # Numeros des cases speciales (vides ici, a remplir dans les classes filles)
        self.murs = []
        self.feux = []

    def etat_suivant(self, etat, action):
        ligne, colonne = divmod(etat, self.taille)
        dl, dc = self.actions[action]
        ligne, colonne = ligne + dl, colonne + dc

        if 0 <= ligne < self.taille and 0 <= colonne < self.taille:
            return ligne * self.taille + colonne
        return etat  # contre un bord : l'agent reste sur place

    def recompense(self, etat):
        return 1.0 if etat == self.arrivee else -0.1
