#! /usr/bin/env python
#-*- coding: utf-8 -*-

from random import *
import sys
sys.setrecursionlimit(200000) # augmente le nombre de récursions possibles
import time


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

"""
####################################################
### FONCTIONS ###
####################################################


##################################
### I - CREATION DU LABYRINTHE ###
##################################


### Generation de la matrice ### -------------------


"""
Demande une valeur à l'utilisateur et verifie qu'il s'agit bien d'un entier.
Entrée : une question pour l'utilisateur
Retourne : le nombre entré
"""
def verifSaisie(question):
    entree = -1

    # Demande à l'utilisateur une entree jusqu'a ce que ce soit un entier.
    while entree < 0:
        try: # Verifie si la valeur entrée est de type entier.
            entree = int(input(question))
        except ValueError: # Dans le cas contraire, on affiche une erreur.
            print("Entrée invalide.")
    return entree


"""
Genere une matrice de -1 séparants des valeurs de 0 à (x * y - 1).
Entrée : largeur et hauteur de la matrice
Retourne : la matrice
"""
def matrice(x, y):
    # on créé une matrice par rapport aux dimensions en argument et on initialise l'accumulateur
    matrice, accumulateur = [[-1 for m in range(2*x+1)] for n in range(2*y+1)], 0

    # Parcours de 2 en 2 l'axe y de la matrice
    for i in range(1, len(matrice) - 1, 2):
        # Parcours de 2 en 2 l'axe x
        for j in range(1, len(matrice[0]) - 1, 2):
            # La case voulu prend la valeur de l'accumulateur
            matrice[i][j] = accumulateur
            # Puis on incrémente l'accumulateur de 1
            accumulateur += 1

    return(matrice)


### Formatage de la matrice ### --------------------


"""
Etabli la liste de tous les murs destructibles.
Entrée : la matrice
Retourne : la liste des coordonnées de tous les murs destructibles
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

"""
Cherche la valeur_plus et la valeur_moins autour du mur selectionné.
Entrée : la matrice
         les coordonnées du mur à détruire
Retourne : 1 ou 0 qui indique au compteur du programme si un mur a été détruit ou non.
"""
def cloisons(matrice, x, y):
    # en fonction de la colonne on sait si les valeurs à récupérer sont à gauche/droite ou en haut/bas
    if x%2 == 0: # gauche/droite
        valeur_plus, valeur_moins = max(matrice[y][x-1], matrice[y][x+1]), min(matrice[y][x-1], matrice[y][x+1])

    else: # haut/bas
        valeur_plus, valeur_moins = max(matrice[y-1][x], matrice[y+1][x]), min(matrice[y-1][x], matrice[y+1][x])

    # Changement des valeurs si les deux valeurs trouvées sont differentes, pour obtenir un labyrinthe parfait.
    if valeur_moins != valeur_plus:
        matrice[y][x] = valeur_moins # on casse le mur

        # On propage la valeur_moins par récursivité
        propagation(matrice, x, y, valeur_moins)
        return(1)

    return(0)

"""
Prend un point ou la valeur moins a déja été appliquée et recherche autours les valeurs à changer.
Entrée : la matrice
         les coordonnées d'un point deja modifié
         la valeur à propager
Retourne : rien (puisque la matrice se modifie)
"""
def propagation(matrice, x, y, valeur_moins):

    if matrice[y][x+1] > valeur_moins: # à droite
        # Applique la nouvelle valeur
        matrice[y][x+1] = valeur_moins
        # Propage depuis ce point
        propagation(matrice, x + 1, y, valeur_moins)

    if matrice[y][x-1] > valeur_moins: # à gauche
        # Applique la nouvelle valeur
        matrice[y][x-1] = valeur_moins
        # Propage depuis ce point
        propagation(matrice, x - 1, y, valeur_moins)


    if matrice[y+1][x] > valeur_moins: # en bas
        # Applique la nouvelle valeur
        matrice[y+1][x] = valeur_moins
        # Propage depuis ce point
        propagation(matrice, x, y + 1, valeur_moins)

    if matrice[y-1][x] > valeur_moins: # en haut
        # Applique la nouvelle valeur
        matrice[y-1][x] = valeur_moins
        # Propage depuis ce point
        propagation(matrice, x, y - 1, valeur_moins)

### Affichage ### ----------------------------------


"""
Affiche ligne par ligne le labyrinthe en fonction des valeurs de la matrice
Entrée : la matrice
Retourne : Rien (procédure)
"""
def dessin(matrice):
    for y in range(len(matrice)):
        ligne = "" # Reinitialise la ligne
        for x in range(len(matrice[0])):
            # chaque caractere correspond a une valeur de la matrice
            # Les murs
            if matrice[y][x] == -1 :
                ligne += ('\x1b[0;37;47m' + '  ' + '\x1b[0m')
            # Les espaces libres
            elif matrice[y][x] == 0 :
                ligne += "  "
            # L'entrée
            elif matrice[y][x] == -2 :
                ligne += "A "
            # La sortie
            elif matrice[y][x] == -3 :
                ligne += "B "
            # Chemin le plus court
            elif matrice[y][x] > 0 or matrice[y][x] == -4 : # Chemin le plus court
                ligne += ('\x1b[0;33;43m' + '  ' + '\x1b[0m')
        print(ligne)


###########################################
### II - RECHERCHE DU PLUS COURT CHEMIN ###
###########################################

### Entrée / Sortie ### ----------------------------

"""
Verifie que les coordonnées entrées sont sur le bords du labyrinthe
Entrée : la matrice
         les coordonnées x et y à tester
         les coordonnées de l'entrée (qui doivent etre differentes de la sortie)
Retourne : les coordonnées
"""
def verifInputs(matrice, x, y, entree_x, entree_y):

    # Tant que le point n'est pas correctement placé ou est superposé à l'entrée
    while not exterieur(x, y, matrice) or (entree_x == x and entree_y == y):
        x = verifSaisie("X : ")
        y = verifSaisie("Y : ")

    return(x, y)

"""
Verifie si les coordonnées sont possibles pour pouvoir rentrer et sortir du labyrinthe.
Entrée : les coordonnées à tester
         la matrice
Retourne True si le point est sur le mur externe, pas dans un coin et avec un acces vers l'interieur.
"""
def exterieur(x, y, matrice):
    if (0 <= x <= len(matrice[0])-1) and (0 <= y <= len(matrice)-1): # On ne dépasse pas du labyrinthe

        # Verifie si il y a un bloc devant le point, en fonction de sa position.
        # Et limite la selection au mur exterieur.
        # Mur de gauche
        if x == 0 and matrice[y][x+1] == 0:
            return(True)
        # Mur de droite
        elif x == len(matrice[0])-1 and matrice[y][x-1] == 0:
            return(True)
        # Mur haut
        elif y == 0 and matrice[y+1][x] == 0:
            return(True)
        # Mur bas
        elif y == len(matrice)-1 and matrice[y-1][x] == 0:
            return(True)

        # Sert à ne pas afficher le message d'erreur au premier passage dans la boucle.
        elif x != 0.1 and y != 0.1:
            print("Les coordonnées ne sont pas disponibles")
    return(False)

### Recherche de la sortie ### ---------------------

"""
place la premiere case adjacente à l'entrée/sortie
Entrée : la matrice
         les coordonnées d'un point du mur externe
Retourne : les coordonnées du point à coté (a l'interieur du labyrinthe)
"""
def premierPoint(matrice, x, y):

    if x == 0 : x = 1
    elif x == len(matrice[0])-1: x -= 1

    if y == 0 : y = 1
    elif y == len(matrice)-1: y -= 1

    return(x, y)

"""
Parcours les chemins possibles du labyrinthe tant que
la sortie n'a pas été atteinte.
Entrée : la matrice
         les coordonnées du premier point
         les coordonnées du dernier point
sortie : la matrice avec les chemins explorés
"""
def recherche(matrice, entree_x, entree_y, sortie_x, sortie_y):
    # initialise l'accumulateur
    accumulateur = 0
    # liste contenant les points de front explorés pour optimiser de maniere importante la propagation.
    liste_exploration = [(entree_x, entree_y)]

    # Tant qu'on a pas trouvé la sortie
    while matrice[sortie_y][sortie_x] == 0:
        # On met à jour l'accumulateur et on reinitialise la liste
        accumulateur += 1
        nouvelle_liste = []

        # Parcours tous les points à verifier
        for point in liste_exploration:

            x, y = point[0], point[1] # Recupere les coordonnées pour plus de clareté
            matrice[y][x] = accumulateur # Modifie la valeur de la case exporée

            # Puis on regarde si les points adjacents sont explorables.
            # à droite du point
            if matrice[y][x+1] == 0:
                nouvelle_liste.append((x+1, y))
            # à gauche du point
            if matrice[y][x-1] == 0:
                nouvelle_liste.append((x-1, y))
            # en bas du point
            if matrice[y+1][x] == 0:
                nouvelle_liste.append((x, y+1))
            # en haut du point
            if matrice[y-1][x] == 0:
                nouvelle_liste.append((x, y-1))

        # Enfin, on met à jour la liste du front d'exploration
        liste_exploration = []
        liste_exploration += nouvelle_liste

    return(matrice)


### Chemin le plus court ### -----------------------

"""
Prend le point d'arrivée et recherche la valeur adjacente la plus petite
de maniere a retrouver la sortie par le plus court chemin.
Entrée : la matrice de base (celle du labyrinthe innexploré)
         la matrice contenant l'exploration des chemins
         les coordonnées du point d'arrivée
sortie : la matrice avec le chemin le plus court
"""
def cheminInverse(matrice, matrice_exploration, x, y):

    # Récupère la valeur adjacente à la sortie (c'est a dire la longueur du chemin)
    valeur = matrice_exploration[y][x]

    # On rebrousse le chemin autant de fois que sa longueur totale.
    while valeur != 0:

        # On donne la valeur -4 aux cases par lesquelles on passe
        matrice[y][x] = -4

        # Puis on modifie les coordonnées pour aller au point suivant
        # qui a une valeur directement inferieure (-1).
        if matrice_exploration[y][x+1] == valeur - 1:
            x += 1
        elif matrice_exploration[y][x-1] == valeur - 1:
            x -= 1
        elif matrice_exploration[y+1][x] == valeur - 1:
            y += 1
        elif matrice_exploration[y-1][x] == valeur - 1:
            y -= 1

        # Enfin, on soustrait 1 au nombre de cases restantes à explorées.
        valeur -= 1

    return(matrice)



####################################################
### /// FONCTIONS ###
####################################################


# On demande les dimensions du labyrinthe
print("Entrez la taille de votre Labyrinthe :")
largeur = hauteur = -1
while largeur < 0:
    largeur = verifSaisie("Largeur : ")
while hauteur < 0:
    hauteur = verifSaisie("Hauteur : ")

### Création de la matrice ###

matrice = matrice(largeur, hauteur)

### Génération du labyrinthe ###

# Obtention de la liste des murs destructibles
liste_cloisons = listeCloisons(matrice)

start_time = time.time()

# Destructions aleatoire de murs. sachant qu'on va en detruire x*y-1
compteur = 0
while compteur < (largeur * hauteur -1): # On détruit x*y-1 murs
    cible = randint(0, len(liste_cloisons)-1) # On choisit un mur
    # Détruit le mur
    compteur += cloisons(matrice, liste_cloisons[cible][0], liste_cloisons[cible][1])
    liste_cloisons.pop(cible) # On retire le mur deja tester de la liste

print("--- %s seconds ---" % (time.time() - start_time))

# Affichage du labyrinthe
print("voici le labyrinthe aléatoire généré :")
dessin(matrice)

### Entrée / Sortie ###


# Inputs des coordonnées de l'entrée
print("Entrez les coordonnées du point de départ")
entree = verifInputs(matrice, 0.1, 0.1, 0.1, 0.1) # les 0.1 sont des valeurs impossibles
# Elle me servent à obliger le programme à passer dans la boucle while
entree_x = entree[0]
entree_y = entree[1]
matrice[entree_y][entree_x] = -2 # Valeur de l'entrée

# Inputs des coordonnées de sortie
print("Entrez les coordonnées du point de d'arrivée")
sortie = verifInputs(matrice, 0.1, 0.1, entree_x, entree_y)
sortie_x = sortie[0]
sortie_y = sortie[1]
matrice[sortie_y][sortie_x] = -3# Valeur de la sortie


### Recherche de la sortie ###


# Obtention du premier point à l'entrée
premier = premierPoint(matrice, entree_x, entree_y)
entree_x, entree_y = premier[0], premier[1]

# Obtention du premier point à la sortie (soit le dernier point du chemin)
premier = premierPoint(matrice, sortie_x, sortie_y)
sortie_x, sortie_y = premier[0], premier[1]

# Recherche du chemin
start_time = time.time()
matrice_exploration = []
matrice_exploration = [row[:] for row in matrice]
matrice_exploration = recherche(matrice_exploration, entree_x, entree_y, sortie_x, sortie_y)
print("--- %s seconds ---" % (time.time() - start_time))

# A partir de l'exploration des chemins, on rerouve le le chemin le plus court
# en partant de l'arrivée.
matrice = cheminInverse(matrice, matrice_exploration, sortie_x, sortie_y)

# On affiche la matrice avec le chemin le plus court
dessin(matrice)
