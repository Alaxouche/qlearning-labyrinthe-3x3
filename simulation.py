import tkinter as tk

import apprentissage as ap

TAILLE_CASE = 100
DELAI = 400  # millisecondes entre deux pas

Q, _, _ = ap.apprendre()

etat = ap.DEPART
nb_pas = 0
score = 0.0
en_marche = False


def dessiner():
    canevas.delete("all")

    for case in range(ap.NB_ETATS):
        ligne, colonne = divmod(case, ap.TAILLE)
        x, y = colonne * TAILLE_CASE, ligne * TAILLE_CASE

        if case == ap.DEPART:
            couleur = "#c8e6c9"
        elif case == ap.ARRIVEE:
            couleur = "#ffe082"
        else:
            couleur = "white"

        canevas.create_rectangle(x, y, x + TAILLE_CASE, y + TAILLE_CASE,
                                 fill=couleur, outline="gray")
        canevas.create_text(x + 14, y + 14, text=str(case), fill="gray")

    ligne, colonne = divmod(etat, ap.TAILLE)
    x = colonne * TAILLE_CASE + TAILLE_CASE / 2
    y = ligne * TAILLE_CASE + TAILLE_CASE / 2
    canevas.create_oval(x - 22, y - 22, x + 22, y + 22, fill="#1976d2")

    info.set("état : {}    pas : {}    score : {:.1f}".format(etat, nb_pas, score))


def avancer():
    global etat, nb_pas, score, en_marche

    if not en_marche:
        return

    etat = ap.etat_suivant(etat, ap.meilleure_action(Q, etat))
    nb_pas += 1
    score += ap.recompense(etat)
    dessiner()

    # On s'arrete a l'arrivee, ou si l'agent tourne en rond trop longtemps
    if etat == ap.ARRIVEE or nb_pas >= ap.MAX_PAS:
        en_marche = False
    else:
        fenetre.after(DELAI, avancer)


def demarrer():
    global en_marche

    if not en_marche and etat != ap.ARRIVEE:
        en_marche = True
        avancer()


def recommencer():
    global etat, nb_pas, score, en_marche

    en_marche = False
    etat, nb_pas, score = ap.DEPART, 0, 0.0
    dessiner()


fenetre = tk.Tk()
fenetre.title("Q-learning labyrinthe")

cote = ap.TAILLE * TAILLE_CASE
canevas = tk.Canvas(fenetre, width=cote, height=cote)
canevas.pack()

info = tk.StringVar()
tk.Label(fenetre, textvariable=info).pack(pady=5)

tk.Button(fenetre, text="Démarrer", command=demarrer).pack(side="left", padx=20, pady=10)
tk.Button(fenetre, text="Recommencer", command=recommencer).pack(side="right", padx=20, pady=10)

dessiner()
fenetre.mainloop()
