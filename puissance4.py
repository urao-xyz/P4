import tkinter as tk
from tkinter import messagebox

LIGNES = 6
COLONNES = 7
TAILLE_CASE = 80
JOUEUR_HUMAIN = 'X'
JOUEUR_IA = 'O'
VIDE = ''
COULEUR_HUMAIN = 'red'
COULEUR_IA = 'yellow'
COULEUR_FOND = 'blue'

class Puissance4:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Puissance 4 - IA Imbattable")
        self.grille = [[VIDE for _ in range(COLONNES)] for _ in range(LIGNES)]
        self.joueur_actuel = JOUEUR_HUMAIN  # Le joueur
        self.canvas = tk.Canvas(racine, width=COLONNES * TAILLE_CASE, height=(LIGNES + 1) * TAILLE_CASE, bg=COULEUR_FOND)
        self.canvas.pack()
        self.dessiner_grille()
        self.canvas.bind("<Button-1>", self.cliquer)

    def dessiner_grille(self):
        """Dessine la grille du Puissance 4."""
        for colonne in range(COLONNES):
            for ligne in range(LIGNES):
                x1 = colonne * TAILLE_CASE
                y1 = (ligne + 1) * TAILLE_CASE
                x2 = x1 + TAILLE_CASE
                y2 = y1 + TAILLE_CASE
                self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='white', outline=COULEUR_FOND)

    def cliquer(self, event):
        """Gestion du clic pour jouer un coup."""
        if self.joueur_actuel == JOUEUR_HUMAIN:
            colonne = event.x // TAILLE_CASE
            if 0 <= colonne < COLONNES:
                if self.jouer_coup(colonne, JOUEUR_HUMAIN):
                    if self.est_gagnant(JOUEUR_HUMAIN):
                        self.afficher_victoire(JOUEUR_HUMAIN)
                        return
                    if self.est_plein():
                        self.afficher_match_nul()
                        return
                    self.joueur_actuel = JOUEUR_IA
                    self.racine.after(500, self.jouer_ia)  # délai pour l'IA

    def jouer_ia(self):
        """IA."""
        colonne, _ = self.minimax(self.grille, 5, -float('inf'), float('inf'), True)
        if colonne is not None:
            if self.jouer_coup(colonne, JOUEUR_IA):
                if self.est_gagnant(JOUEUR_IA):
                    self.afficher_victoire(JOUEUR_IA)
                    return
                if self.est_plein():
                    self.afficher_match_nul()
                    return
                self.joueur_actuel = JOUEUR_HUMAIN

    def jouer_coup(self, colonne, joueur):
        """Joue un coup dans la colonne spécifiée pour le joueur donné."""
        for ligne in reversed(range(LIGNES)):
            if self.grille[ligne][colonne] == VIDE:
                self.grille[ligne][colonne] = joueur
                self.dessiner_jeton(ligne, colonne, joueur)
                return True
        return False

    def dessiner_jeton(self, ligne, colonne, joueur):
        """Dessine un jeton"""
        x1 = colonne * TAILLE_CASE + 5
        y1 = (ligne + 1) * TAILLE_CASE + 5
        x2 = x1 + TAILLE_CASE - 10
        y2 = y1 + TAILLE_CASE - 10
        couleur = COULEUR_HUMAIN if joueur == JOUEUR_HUMAIN else COULEUR_IA
        self.canvas.create_oval(x1, y1, x2, y2, fill=couleur, outline=COULEUR_FOND)

    def est_gagnant(self, joueur):
        """Vérif si le joueur a gagné."""
        # Vérification horizontale
        for ligne in range(LIGNES):
            for colonne in range(COLONNES - 3):
                if all(self.grille[ligne][colonne + i] == joueur for i in range(4)):
                    return True

        # Vérification verticale
        for colonne in range(COLONNES):
            for ligne in range(LIGNES - 3):
                if all(self.grille[ligne + i][colonne] == joueur for i in range(4)):
                    return True

        # Vérification diagonale (haut-gauche à bas-droite)
        for ligne in range(LIGNES - 3):
            for colonne in range(COLONNES - 3):
                if all(self.grille[ligne + i][colonne + i] == joueur for i in range(4)):
                    return True

        # Vérification diagonale (bas-gauche à haut-droite)
        for ligne in range(3, LIGNES):
            for colonne in range(COLONNES - 3):
                if all(self.grille[ligne - i][colonne + i] == joueur for i in range(4)):
                    return True

        return False

    def est_plein(self):
        return all(cellule != VIDE for ligne in self.grille for cellule in ligne)

    def afficher_victoire(self, joueur):
        gagnant = "Vous" if joueur == JOUEUR_HUMAIN else "L'IA"
        messagebox.showinfo("Fin du jeu", f"{gagnant} a gagné !")
        self.racine.quit()

    def afficher_match_nul(self):
        messagebox.showinfo("Fin du jeu", "Match nul !")
        self.racine.quit()

    def minimax(self, grille, profondeur, alpha, beta, maximisant):
        """Algorithme Minimax avec élagage Alpha-Bêta."""
        # Cas de base : fin du jeu ou profondeur maximale atteinte
        if self.est_gagnant(JOUEUR_IA):
            return (None, 100)
        if self.est_gagnant(JOUEUR_HUMAIN):
            return (None, -100)
        if self.est_plein() or profondeur == 0:
            return (None, 0)

        if maximisant:
            valeur = -float('inf')
            meilleure_colonne = None
            for colonne in range(COLONNES):
                if grille[0][colonne] == VIDE:
                    ligne = self.trouver_ligne_vide(grille, colonne)
                    grille[ligne][colonne] = JOUEUR_IA
                    _, nouvelle_valeur = self.minimax(grille, profondeur - 1, alpha, beta, False)
                    grille[ligne][colonne] = VIDE
                    if nouvelle_valeur > valeur:
                        valeur = nouvelle_valeur
                        meilleure_colonne = colonne
                    alpha = max(alpha, valeur)
                    if alpha >= beta:
                        break
            return (meilleure_colonne, valeur)
        else:
            valeur = float('inf')
            meilleure_colonne = None
            for colonne in range(COLONNES):
                if grille[0][colonne] == VIDE:
                    ligne = self.trouver_ligne_vide(grille, colonne)
                    grille[ligne][colonne] = JOUEUR_HUMAIN
                    _, nouvelle_valeur = self.minimax(grille, profondeur - 1, alpha, beta, True)
                    grille[ligne][colonne] = VIDE
                    if nouvelle_valeur < valeur:
                        valeur = nouvelle_valeur
                        meilleure_colonne = colonne
                    beta = min(beta, valeur)
                    if alpha >= beta:
                        break
            return (meilleure_colonne, valeur)

    def trouver_ligne_vide(self, grille, colonne):
        """Trouve la première ligne vide dans une colonne."""
        for ligne in reversed(range(LIGNES)):
            if grille[ligne][colonne] == VIDE:
                return ligne
        return None

# Lancement du jeu
if __name__ == "__main__":
    racine = tk.Tk()
    jeu = Puissance4(racine)
    racine.mainloop()