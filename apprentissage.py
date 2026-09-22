import matplotlib.pyplot as plt
import numpy as np

TAILLE = 3
NB_ETATS = TAILLE * TAILLE
DEPART = 0
ARRIVEE = NB_ETATS - 1

ALPHA = 0.1          # vitesse d'apprentissage
GAMMA = 0.9          # importance du futur
EPSILON_DEBUT = 1.0  # exploration totale au debut
EPSILON_MIN = 0.05   # exploration minimale
DECROISSANCE = 0.99  # epsilon est multiplie par ce nombre a chaque episode
NB_EPISODES = 500
MAX_PAS = 50
GRAINE = 0

# Haut, Bas, Gauche, Droite : (deplacement en ligne, deplacement en colonne)
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
NOMS_ACTIONS = ["Haut", "Bas", "Gauche", "Droite"]

rng = np.random.default_rng()


def etat_suivant(etat, action):
    ligne, colonne = divmod(etat, TAILLE)
    dl, dc = ACTIONS[action]
    ligne, colonne = ligne + dl, colonne + dc

    if 0 <= ligne < TAILLE and 0 <= colonne < TAILLE:
        return ligne * TAILLE + colonne
    return etat  # contre un bord : l'agent reste sur place


def recompense(etat):
    return 1.0 if etat == ARRIVEE else -0.1


def meilleure_action(Q, etat):
    # En cas d'egalite, on tire au hasard parmi les meilleures actions
    meilleures = np.flatnonzero(Q[etat] == Q[etat].max())
    return int(rng.choice(meilleures))


def choisir_action(Q, etat, epsilon):
    if rng.random() < epsilon:
        return int(rng.integers(len(ACTIONS)))
    return meilleure_action(Q, etat)


def apprendre():
    Q = np.zeros((NB_ETATS, len(ACTIONS)))
    epsilon = EPSILON_DEBUT
    pas_par_episode = []
    epsilons = []

    for episode in range(NB_EPISODES):
        etat = DEPART

        for pas in range(1, MAX_PAS + 1):
            action = choisir_action(Q, etat, epsilon)
            suivant = etat_suivant(etat, action)
            r = recompense(suivant)

            if suivant == ARRIVEE:
                cible = r  # etat final : pas de futur
            else:
                cible = r + GAMMA * Q[suivant].max()
            Q[etat, action] += ALPHA * (cible - Q[etat, action])

            etat = suivant
            if etat == ARRIVEE:
                break

        pas_par_episode.append(pas)
        epsilons.append(epsilon)
        epsilon = max(EPSILON_MIN, epsilon * DECROISSANCE)

    return Q, pas_par_episode, epsilons


def chemin(Q):
    etat = DEPART
    parcours = [etat]
    while etat != ARRIVEE and len(parcours) <= MAX_PAS:
        etat = etat_suivant(etat, meilleure_action(Q, etat))
        parcours.append(etat)
    return parcours


def afficher_courbes(pas_par_episode, epsilons):
    episodes = np.arange(1, len(pas_par_episode) + 1)
    fenetre = 20
    moyenne = np.convolve(pas_par_episode, np.ones(fenetre) / fenetre, mode="valid")

    fig, (haut, bas) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

    haut.plot(episodes, pas_par_episode, color="#9ec5e8", linewidth=1,
              label="pas par episode")
    haut.plot(episodes[fenetre - 1:], moyenne, color="#1565c0", linewidth=2,
              label="moyenne sur {} episodes".format(fenetre))
    haut.axhline(4, color="gray", linestyle="--", linewidth=1,
                 label="chemin optimal (4 pas)")
    haut.set_ylabel("nombre de pas")
    haut.set_title("Courbe d'apprentissage")
    haut.legend()
    haut.grid(alpha=0.3)

    bas.plot(episodes, epsilons, color="#1565c0", linewidth=2)
    bas.set_xlabel("episode")
    bas.set_ylabel("epsilon")
    bas.set_title("Exploration (epsilon)")
    bas.grid(alpha=0.3)

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    Q, pas_par_episode, epsilons = apprendre()

    print("etat      Haut       Bas    Gauche    Droite   meilleure")
    for etat in range(NB_ETATS):
        if etat == ARRIVEE:
            meilleure = "arrivee"
        else:
            meilleure = NOMS_ACTIONS[int(np.argmax(Q[etat]))]
        valeurs = "".join("{:10.3f}".format(v) for v in Q[etat])
        print("{:4d}{}   {}".format(etat, valeurs, meilleure))

    print()
    print("chemin :", chemin(Q))

    afficher_courbes(pas_par_episode, epsilons)
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
