"""Visualisation pédagogique du Q-learning : entraînement puis parcours appris."""

import tkinter as tk


def lancer_simulation(lab, agent):
    """Ouvre les deux modes dans une fenêtre, avec UN seul agent QLearning.

    1. Entraînement en direct : chaque appel à next(generateur) joue un
       événement de apprendre_pas_a_pas() sans bloquer l'interface.
    2. Parcours appris : l'agent choisit la meilleure action de sa table Q,
       qui ne change plus. Les deux modes partagent le même environnement.
    """

    fenetre = tk.Tk()
    fenetre.title("Q-learning — Apprentissage et parcours")
    fenetre.geometry("1000x680")

    taille_case = 110
    generateur = agent.apprendre_pas_a_pas()
    mode = "entrainement"
    lecture_auto = False
    rappel_auto = None  # Identifiant du prochain appel Tkinter, annulable avec Pause.
    fini_entrainement = False
    nb_pas = 0
    score = 0.0
    etat_affiche = lab.depart

    noms = getattr(lab, "noms_actions", [str(i) for i in range(lab.nb_actions)])
    titre = tk.StringVar(value="Mode 1 — Entraînement en direct (épisode 1)")
    details = tk.StringVar(value="Appuie sur « Pas suivant » ou « Lecture auto ».")
    vitesse = tk.IntVar(value=80)  # Durée entre deux événements, en millisecondes.

    gauche = tk.Frame(fenetre, padx=12, pady=12)
    gauche.pack(side="left", fill="y")
    droite = tk.Frame(fenetre, padx=12, pady=12)
    droite.pack(side="left", fill="both", expand=True)

    tk.Label(gauche, textvariable=titre, font=("Arial", 12, "bold"),
             wraplength=380, justify="left").pack(anchor="w", pady=(0, 12))

    # Le canevas ne fait qu'afficher la position ; les règles restent dans Labyrinthe.
    canevas = tk.Canvas(gauche, width=taille_case * lab.taille,
                        height=taille_case * lab.taille, bg="white")
    canevas.pack()

    tk.Label(gauche, textvariable=details, justify="left", anchor="w",
             wraplength=370, height=7).pack(fill="x", pady=10)

    controles = tk.Frame(gauche)
    controles.pack(fill="x")
    bouton_pas = tk.Button(controles, text="Pas suivant", width=14)
    bouton_pas.grid(row=0, column=0, padx=3, pady=3)
    bouton_auto = tk.Button(controles, text="Lecture auto", width=14)
    bouton_auto.grid(row=0, column=1, padx=3, pady=3)
    bouton_pause = tk.Button(controles, text="Pause", width=14)
    bouton_pause.grid(row=1, column=0, padx=3, pady=3)
    bouton_parcours = tk.Button(controles, text="Parcours appris", width=14,
                               state="disabled")
    bouton_parcours.grid(row=1, column=1, padx=3, pady=3)
    bouton_reprise = tk.Button(controles, text="Recommencer parcours", width=30,
                              state="disabled")
    bouton_reprise.grid(row=2, column=0, columnspan=2, padx=3, pady=3)

    tk.Label(gauche, text="Délai automatique (ms) :").pack(anchor="w", pady=(12, 0))
    tk.Scale(gauche, from_=10, to=500, orient="horizontal",
             variable=vitesse).pack(fill="x")

    tk.Label(droite, text="Table Q en cours (Haut / Bas / Gauche / Droite)",
             font=("Arial", 11, "bold")).pack(anchor="w")
    tableau = tk.Label(droite, font=("Consolas", 10), justify="left", anchor="nw")
    tableau.pack(fill="x", pady=8)

    tk.Label(droite, text="Journal des décisions", font=("Arial", 11, "bold")
             ).pack(anchor="w", pady=(8, 0))
    journal = tk.Text(droite, height=18, width=65, state="disabled",
                      font=("Consolas", 10), wrap="word")
    journal.pack(fill="both", expand=True)
    tk.Label(droite,
             text="En entraînement, Q change après chaque action. En parcours, Q reste fixe.",
             wraplength=550, justify="left").pack(anchor="w", pady=5)

    def noter(message):
        """Ajoute une ligne au journal ; conserve seulement les 350 dernières."""
        journal.config(state="normal")
        journal.insert("end", message + "\n")
        if int(journal.index("end-1c").split(".")[0]) > 350:
            journal.delete("1.0", "2.0")
        journal.see("end")
        journal.config(state="disabled")

    def afficher_q():
        """Affiche les neuf lignes de Q, actualisées pendant l'apprentissage."""
        lignes = ["État    H       B       G       D"]
        for i in range(lab.nb_etats):
            valeurs = " ".join(f"{q:7.3f}" for q in agent.Q[i])
            lignes.append(f"{i:>4}  {valeurs}")
        tableau.config(text="\n".join(lignes))

    def dessiner():
        """Dessine la grille et le robot à l'état actuellement affiché."""
        canevas.delete("all")
        for case in range(lab.nb_etats):
            ligne, colonne = divmod(case, lab.taille)
            x, y = colonne * taille_case, ligne * taille_case
            if case == lab.depart:
                couleur = "#c8e6c9"
            elif case == lab.arrivee:
                couleur = "#ffe082"
            elif case in lab.murs:
                couleur = "#424242"
            elif case in lab.feux:
                couleur = "#ef5350"
            else:
                couleur = "white"
            canevas.create_rectangle(x, y, x + taille_case, y + taille_case,
                                     fill=couleur, outline="gray")
            canevas.create_text(x + 13, y + 13, text=str(case), fill="#555555")

        ligne, colonne = divmod(etat_affiche, lab.taille)
        x = (colonne + 0.5) * taille_case
        y = (ligne + 0.5) * taille_case
        rayon = taille_case / 5
        canevas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                            fill="#1976d2", outline="#0d47a1")

    def prochain_evenement():
        """Fait avancer d'un événement l'entraînement OU le parcours appris."""
        nonlocal mode, fini_entrainement, nb_pas, score, etat_affiche

        if mode == "entrainement":
            try:
                evenement = next(generateur)
            except StopIteration:
                evenement = {"type": "fin"}

            if evenement["type"] == "pas":
                etat_affiche = evenement["nouvel_etat"]
                titre.set(f"Mode 1 — Épisode {evenement['episode']}/{agent.nb_episodes}, "
                          f"pas {evenement['pas']}")
                action = evenement["action"]
                details.set(
                    f"État : {evenement['etat_depart']} → {evenement['nouvel_etat']}\n"
                    f"Action : {noms[action]} ({action})\n"
                    f"Récompense : {evenement['recompense']:+.2f} | "
                    f"Score épisode : {evenement['total']:+.2f}\n"
                    f"Epsilon : {evenement['epsilon']:.3f}\n"
                    f"Cible Bellman : {evenement['cible']:.3f}\n"
                    f"Q avant : {evenement['q_avant']:.3f} → "
                    f"Q après : {evenement['q_apres']:.3f}"
                )
                noter(f"E{evenement['episode']:04} P{evenement['pas']:02} "
                      f"{evenement['etat_depart']} -> {evenement['nouvel_etat']} "
                      f"{noms[action]:7} r={evenement['recompense']:+.1f} "
                      f"Q={evenement['q_avant']:.3f}->{evenement['q_apres']:.3f}")
            elif evenement["type"] == "fin_episode":
                etat_affiche = lab.etat
                titre.set(f"Fin de l'épisode {evenement['episode']}/{agent.nb_episodes}")
                details.set(f"Score de l'épisode : {evenement['total']:+.2f}\n"
                            f"Nouvel epsilon : {evenement['epsilon']:.3f}\n"
                            "Le prochain événement recommence au départ.")
                noter(f"--- Fin E{evenement['episode']} : "
                      f"score={evenement['total']:+.2f} ---")
            else:
                fini_entrainement = True
                titre.set("Entraînement terminé !")
                details.set(f"{agent.nb_episodes} épisodes terminés. "
                            "Clique sur « Parcours appris » pour tester la politique "
                            "sans modifier la table Q.")
                noter("=== APPRENTISSAGE TERMINÉ : Q est maintenant fixée ===")
                bouton_parcours.config(state="normal")
                return False

            afficher_q()
            dessiner()
            return True

        if mode == "parcours":
            if etat_affiche == lab.arrivee or nb_pas >= agent.max_pas:
                return False
            actions = lab.actions_possibles(etat_affiche)
            if not actions:
                details.set("Plus aucune action autorisée.")
                return False

            precedent = etat_affiche
            action = agent.meilleure_action(precedent)  # Aucune exploration ici.
            etat_affiche, recompense, termine = lab.step(action)
            nb_pas += 1
            score += recompense
            titre.set(f"Mode 2 — Parcours appris, pas {nb_pas}")
            details.set(f"État : {precedent} → {etat_affiche}\n"
                        f"Meilleure action Q : {noms[action]} ({action})\n"
                        f"Récompense : {recompense:+.2f} | Score : {score:+.2f}\n"
                        f"Q[{precedent}, {action}] = {agent.Q[precedent, action]:.3f}\n"
                        "La table Q ne change pas pendant ce test.")
            noter(f"TEST P{nb_pas:02} {precedent} -> {etat_affiche} "
                  f"{noms[action]:7} r={recompense:+.1f}")
            dessiner()
            if termine:
                noter("=== OBJECTIF ATTEINT ===")
                return False
            if nb_pas >= agent.max_pas:
                noter("=== LIMITE DE PAS ATTEINTE ===")
                return False
            return True

        return False

    def pas_suivant():
        """Avance manuellement d’un événement sans laisser de rappel automatique."""
        arreter()
        prochain_evenement()

    def boucle_auto():
        """Planifie le prochain mouvement sans bloquer la fenêtre Tkinter."""
        nonlocal rappel_auto
        rappel_auto = None  # Le rappel courant vient de se déclencher.
        if not lecture_auto:
            return
        encore = prochain_evenement()
        if encore:
            rappel_auto = fenetre.after(vitesse.get(), boucle_auto)
        else:
            arreter()

    def demarrer_auto():
        nonlocal lecture_auto, rappel_auto
        if not lecture_auto and (mode == "parcours" or not fini_entrainement):
            lecture_auto = True
            rappel_auto = fenetre.after(0, boucle_auto)

    def arreter():
        nonlocal lecture_auto, rappel_auto
        lecture_auto = False
        if rappel_auto is not None:
            fenetre.after_cancel(rappel_auto)
            rappel_auto = None

    def parcours_appris():
        """Passe au test : on conserve les valeurs apprises et repart de zéro."""
        nonlocal mode, nb_pas, score, etat_affiche, lecture_auto
        if not fini_entrainement:
            return
        arreter()  # Annule aussi un éventuel rappel de l’ancien mode.
        mode = "parcours"
        etat_affiche = lab.reset()
        nb_pas, score = 0, 0.0
        titre.set("Mode 2 — Parcours après apprentissage")
        details.set("La table Q est fixée. Observe les meilleures actions de l'agent.")
        bouton_reprise.config(state="normal")
        noter("=== TEST DE LA POLITIQUE APPRISE ===")
        dessiner()

    # Les callbacks sont associés aux boutons APRÈS définition des fonctions.
    bouton_pas.config(command=pas_suivant)
    bouton_auto.config(command=demarrer_auto)
    bouton_pause.config(command=arreter)
    bouton_parcours.config(command=parcours_appris)
    bouton_reprise.config(command=parcours_appris)

    afficher_q()
    dessiner()
    fenetre.mainloop()
