#! /usr/bin/env python
#-*- coding: utf-8 -*-

from random import *

""" TO DO LIST

"""


""" PROBLEMS

"""

""" NOTES

  0 1 2 3 4 5 6
0 - - - - - - -
1 -   -       -
2 -   - - -   -
3 -           -
4 - - - - - - -

y = [row[:] for row in x]

"""

####################################################
### FONCTIONS ###
####################################################

### GENERATION MATRICE ### -------------------------
""" Genere la matrice de -1 séparants des valeurs de 0 à (x * y - 1)
"""
def matrice(x, y):
    # on créé une matrice par rapport aux dimensions en argument et on initialise l'accumulateur
    matrice, accumulateur = [[-1 for m in range(2*x+1)] for n in range(2*y+1)], 0

    # Parcours de 2 en 2 l'axe y de la matrice
    for i in range(1, len(matrice)-1, 2):
        # Parcours de 2 en 2 l'axe x
        for j in range(1, len(matrice[0])-1, 2):
            matrice[i][j] = accumulateur
            accumulateur += 1

    return(matrice)

### FORMATAGE MATRICE ### --------------------------

""" Etabli la liste de tous les murs non porteurs.
"""
def listeCloisons(matrice):
    liste = []
    for x in range(1, len(matrice[0])-1):
        if x%2 == 1: # Pour les colonnes paires, on prend les lignes impaires
            for y in range(2, len(matrice)-1, 2):
                liste.append((x,y))
        else: # Pour les colonnes impaires, on prend les lignes paires
            for y in range(1, len(matrice)-1, 2):
                liste.append((x,y))
    return(liste)

""" Abat des cloisons, les bonnes, et proprement.
Cherche la valeur_plus et la valeur_moins
Propagation des valeurs
Mise a jour de la matrice
"""
def cloisons(matrice, x, y):
    # en fonction de la colonne on sait si les valeurs à récupérer sont à gauche/droite ou en haut/bas
    if x%2 == 0: # gauche/droite
        valeur_plus = max(matrice[y][x-1], matrice[y][x+1])
        valeur_moins = min(matrice[y][x-1], matrice[y][x+1])
    else: # haut/bas
        valeur_plus = max(matrice[y-1][x], matrice[y+1][x])
        valeur_moins = min(matrice[y-1][x], matrice[y+1][x])

    # Application du changement de valeur si les 2 valeurs trouvées sont differentes
    if valeur_moins != valeur_plus:
        matrice[y][x] = valeur_moins # on casse le mur

        # met à jour la matrice avec la nouvelle valeur
        for j in range(1, len(matrice)-1):
            for i in range(1, len(matrice[0])-1):
                if matrice[j][i] == valeur_plus:
                    matrice[j][i] = valeur_moins

    return(matrice)

""" Verifie si la matrice est prete.
Vérifie chaque valeurs
retourne False s'il y a une valeur plus grande que 0
True sinon
"""
def check(matrice):
    for j in range(1, len(matrice)-1):
        for i in range(1, len(matrice[0])-1):
            if matrice[j][i] > 0:
                return(False)
    return(True)

### AFFICHAGE ### ----------------------------------

""" Chaque -1 est affiché comme "* " et les 0 comme "  "
"""
def dessin(matrice):
    for y in range(len(matrice)):
        ligne = ""
        for x in range(len(matrice[0])):
            if matrice[y][x] == -1:
                ligne += "* "
            elif matrice[y][x] == 0:
                ligne += "  "
            elif matrice[y][x] == -2:
                ligne += "A "
            elif matrice[y][x] == -3:
                ligne += "B "
            elif matrice[y][x] > 0 or matrice[y][x] == -4:
                ligne += ". "
        print(ligne)

### ENTREE - SORTIE ### ----------------------------

""" Demande a l'utilisateur d'entrer les coordonnées d'entrée et sortie
du labyrinthe tant que celles-ci sont fausses.
Retourne la nouvelle matrice avec les valeurs d'entrée et sortie
et retourne les coordonnées de l'entrée
"""
def inputs(mat):

    # Inputs des coordonnées de l'entrée
    print("Entrez les coordonnées du point de départ")
    spawn_x = int(input("X : "))
    spawn_y = int(input("Y : "))

    while not exterieur(spawn_x, spawn_y, mat):
        print("Les coordonnées ne sont pas disponibles")
        spawn_x = int(input("X : "))
        spawn_y = int(input("Y : "))

    mat[spawn_y][spawn_x] = -2

    # Inputs des coordonnées de sortie
    print("Entrez les coordonnées du point de d'arrivée")
    exit_x = int(input("X : "))
    exit_y = int(input("Y : "))

    while not (exterieur(exit_x, exit_y, mat)) or (spawn_x == exit_x and spawn_y == exit_y):
        print("Les coordonnées ne sont pas disponibles")
        exit_x = int(input("X : "))
        exit_y = int(input("Y : "))

    mat[exit_y][exit_x] = -3

    return(mat, spawn_x, spawn_y, exit_x, exit_y)

""" Retourne True si elle est sur le mur externe, pas dans un coin et avec un acces vers l'interieur.
"""
def exterieur(x, y, matrice):
    if (0 <= x <= len(matrice[0])-1) and (0 <= y <= len(matrice)-1): # Exterieur

        # Verifie si il y a un bloc devant
        if x == 0 and matrice[y][x+1] == 0:
            return(True)
        elif x == len(matrice[0])-1 and matrice[y][x-1] == 0:
            return(True)
        elif y == 0 and matrice[y+1][x] == 0:
            return(True)
        elif y == len(matrice)-1 and matrice[y-1][x] == 0:
            return(True)

    return(False)


### RECHERCHE DU CHEMIN ### ------------------------

"""
"""
def gps(matrice, x, y):

    # Reassigne les valeurs pour avoir la premiere position dans les labyrinthe
    if x == 0 : x = 1
    elif x == len(matrice[0])-1: x -= 1
    if y == 0 : y = 1
    elif y == len(matrice)-1: y -= 1

    matrice[y][x] = 1
    return(recursion(nouvelle_matrice, x, y, 2))


""" peut etre amélioré avec un for ?
"""
def recursion(matrice, x, y, valeur):
    if matrice[y][x+1] == -3 or matrice[y][x-1] == -3 or matrice[y-1][x] == -3 or matrice[y+1][x] == -3:
        return(matrice)

    if matrice[y][x+1] == 0:
        matrice[y][x+1] = valeur
        if recursion(matrice, x + 1, y, valeur + 1) == matrice:
            return(matrice)

    if matrice[y][x-1] == 0:
        matrice[y][x-1] = valeur
        if recursion(matrice, x - 1, y, valeur + 1) == matrice:
            return(matrice)


    if matrice[y+1][x] == 0:
        matrice[y+1][x] = valeur
        if recursion(matrice, x, y + 1, valeur + 1) == matrice:
            return(matrice)

    if matrice[y-1][x] == 0:
        matrice[y-1][x] = valeur
        if recursion(matrice, x, y - 1, valeur + 1) == matrice:
            return(matrice)

### CHEMIN LE PLUS COURT ### -----------------------

def cheminInverse(matrice, nouvelle_matrice, x, y):
    if x == 0 : x = 1
    elif x == len(matrice[0])-1: x -= 1
    if y == 0 : y = 1
    elif y == len(matrice)-1: y -= 1

    valeur = nouvelle_matrice[y][x]

    while valeur != 0:

        matrice[y][x] = -4

        if nouvelle_matrice[y][x+1] == valeur - 1:
            x += 1
        elif nouvelle_matrice[y][x-1] == valeur - 1:
            x -= 1
        elif nouvelle_matrice[y+1][x] == valeur - 1:
            y += 1
        elif nouvelle_matrice[y-1][x] == valeur - 1:
            y -= 1

        valeur -= 1

    return(matrice)

####################################################
### /// FONCTIONS ###
####################################################

# Inputs de dimension
largeur = int(input("largeur de la matrice? "))
hauteur = int(input("hauteur de la matrice? "))

# Obtention de la matrice
mat = matrice(largeur, hauteur)

# Génération du labyrinthe
liste_cloisons = listeCloisons(mat)

while not check(mat):
    cible = randint(0, len(liste_cloisons)-1)
    cloisons(mat, liste_cloisons[cible][0], liste_cloisons[cible][1])
    liste_cloisons.pop(cible)

# Affichage du labyrinthe
print("voici le labyrinthe aleatoire généré :")
dessin(mat)

# Positionnement de l'entree et de la sortie et Résolution
inputs = inputs(mat)
mat = inputs[0]
start_x = inputs[1]
start_y = inputs[2]
exit_x = inputs[3]
exit_y = inputs[4]


nouvelle_matrice = []
nouvelle_matrice = [row[:] for row in mat]


nouvelle_matrice = gps(nouvelle_matrice, start_x, start_y)

mat = cheminInverse(mat, nouvelle_matrice, exit_x, exit_y)

dessin(mat)

quit()
