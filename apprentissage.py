import random

import numpy as np

TAILLE = 3
NB_ETATS = TAILLE * TAILLE
NB_ACTIONS = 4
DEPART = 0
ARRIVEE = NB_ETATS - 1

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1
NB_EPISODES = 500
MAX_PAS = 50

NOMS_ACTIONS = ["Haut", "Bas", "Gauche", "Droite"]


def etat_suivant(etat, action):
    ligne = etat // TAILLE
    colonne = etat % TAILLE

    if action == 0:
        ligne = ligne - 1
    elif action == 1:
        ligne = ligne + 1
    elif action == 2:
        colonne = colonne - 1
    else:
        colonne = colonne + 1

    if ligne < 0 or ligne >= TAILLE or colonne < 0 or colonne >= TAILLE:
        return etat
    return ligne * TAILLE + colonne


def recompense(etat):
    if etat == ARRIVEE:
        return 1.0
    return -0.1


def choisir_action(Q, etat):
    if random.random() < EPSILON:
        return random.randint(0, NB_ACTIONS - 1)
    return int(np.argmax(Q[etat]))


def apprendre():
    Q = np.zeros((NB_ETATS, NB_ACTIONS))

    for episode in range(NB_EPISODES):
        etat = DEPART

        for pas in range(MAX_PAS):
            action = choisir_action(Q, etat)
            suivant = etat_suivant(etat, action)
            r = recompense(suivant)

            Q[etat][action] = Q[etat][action] + ALPHA * (
                r + GAMMA * Q[suivant].max() - Q[etat][action])

            etat = suivant
            if etat == ARRIVEE:
                break

    return Q


if __name__ == "__main__":
    Q = apprendre()

    print("etat      Haut       Bas    Gauche    Droite   meilleure")
    for etat in range(NB_ETATS):
        if etat == ARRIVEE:
            meilleure = "arrivee"
        else:
            meilleure = NOMS_ACTIONS[int(np.argmax(Q[etat]))]
        print("{:4d}  {:8.3f}  {:8.3f}  {:8.3f}  {:8.3f}   {}".format(
            etat, Q[etat][0], Q[etat][1], Q[etat][2], Q[etat][3], meilleure))

    etat = DEPART
    chemin = [etat]
    while etat != ARRIVEE and len(chemin) <= MAX_PAS:
        etat = etat_suivant(etat, int(np.argmax(Q[etat])))
        chemin.append(etat)

    print()
    print("chemin :", chemin)
