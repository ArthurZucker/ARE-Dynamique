
import random
import numpy as np
from scipy import *
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
from parameteres import *
from classes import *



#CREATION D'UNE MATRICE AVEC CONTROLE DES PARAMETRES
########################################################################################################
#BATIMENTS

class Batiment:
   """
Création de la classe Bâtiment qui comprend les différents types de batiments
"""

   def __init__(self, taille_batiment): # Définit le type des bâtiments selon leur taille
       if taille_batiment == 1:
           self.type = "Porte"
           Liste_porte.append(self)
           Liste_batiment.append(self)
       elif taille_batiment in (taille_des_maisons):
           self.type = "Maison"
           Liste_maison.append(self)
           Liste_batiment.append(self)
       elif taille_batiment == taille_des_armureries :
           self.type = "Armurerie"
           Liste_armurerie.append(self)
           Liste_batiment.append(self)
       elif taille_batiment in (taille_des_magasins):
           self.type = "Magasin"
           Liste_magasin.append(self)
           Liste_batiment.append(self)
       elif taille_batiment == taille_des_hopitaux:
           self.type = "Hôpital"
           Liste_hopital.append(self)
           Liste_batiment.append(self)
       if self.type == "Porte":        #Stocks des portes
           self.stock_medicaments = 0
           self.stock_nourriture = 0
           self.stock_munitions = 0


   def __str__(self):                  # Fait en sorte que leur nom soit leur type
       return self.type

   def __repr__(self):
       return self.__str__()
def CreationMatriceZero(x, y):
   """
   int*int -> list[list[int]]
   Crée une map de 0 de hauteur x et de largeur y
   """

   return [[0 for j in range(y)] for i in range(x)]
Liste_batiment=[]
Liste_porte=[]
Liste_maison=[]
Liste_armurerie=[]
Liste_magasin=[]
Liste_hopital=[]
def  implante_batiments(carte, nbb):
   """
   liste[liste[int]]*int -> liste[liste[int * Object]]
   Prend une carte vide et la renvoie avec batiments, portes et ressources
   """

   taille_min = 4            # Fixe la taille minimale de bâtiment L*L
   taille_max = 18           # Fixe la taille maximale de bâtiment L*L
   compteur_batiment = 0     # Compteur du nombre de bâtiments placés
   taille_batiment = 0       # Tirage aléatoire de la taille du prochain bâtiment à placer
   x = 0                     # Coordonnées du coin haut-gauche du bâtiment à placer
   y = 0

   while compteur_batiment < nbb:                                   # Place nbb bâtiments aléatoirement selon leur point haut-gauche
       taille_batiment = random.randint(taille_min, taille_max )    # Tirage de la taille du bâtiment
       x = random.randint(1,len(carte[0])-taille_batiment-1)        # Tirage aléatoire de x pour que le batîment ne dépasse pas des bords
       y = random.randint(1,len(carte)-taille_batiment-1)           # Tirage aléatoire de y ...
       compteur_verif = 0                                           # Compteur vérifiant que le bâtiment n'en écrase pas un autre

       for x1 in range(x,x+taille_batiment):                        # Vérifie que le bâtiment ne vas pas en écraser un autre
           for y1 in range(y,y+taille_batiment):                    # Parcours toutes les cases qui doivent être remplacées par le bâtiment
               if carte[x1][y1]==0:                                 # Vérifie qu'elles sont vides
                   compteur_verif += 1                              # Si oui, incrémentation du compteur


       if compteur_verif == taille_batiment**2 and not taille_batiment in range(12,18): # Place libre & taille du batiment définie
           compteur_batiment += 1                                                       # Ajoute 1 au compteur de bâtiments placés
           for x1 in range(x,x+taille_batiment):                                        # Place un bâtiment dans chaque case
               for y1 in range(y,y+taille_batiment):
                   carte[x1][y1] = Batiment(taille_batiment)
                   carte[x1][y1].place_MATRICE=x1,y1

                                                                    # Placement des portes
           x_porte = random.randint(x, x+taille_batiment-1)         # Tire la ligne de la porte
           if x_porte == x or x_porte == x + taille_batiment-1:     # Tire la colonne de la porte
               y_porte = random.randint(y+1, y+ taille_batiment-2)

           else:
               tirage_y = random.randint(0,2)
               if tirage_y == 0:
                   y_porte = y
               else:
                   y_porte = y+(taille_batiment-1)
           carte[x_porte][y_porte] = Batiment(1)                                     # Implante la porte
           carte[x_porte][y_porte].place_MATRICE=x_porte,y_porte

           if taille_batiment in range(4,7):                                         # Ressources des Maisons
               carte[x_porte][y_porte].stock_medicaments = random.randint(0,3)
               carte[x_porte][y_porte].stock_nourriture = random.randint(0,5)
               carte[x_porte][y_porte].stock_munitions = random.randint(0,5)
               carte[x_porte][y_porte].type_bat="Maison"
           elif taille_batiment == 7:                                                # Ressources des Armureries
               carte[x_porte][y_porte].stock_munitions = random.randint(150,200)
               carte[x_porte][y_porte].type_bat="Armurerie"
           elif taille_batiment in range(8,12):                                      # Ressources des Magasins
               carte[x_porte][y_porte].stock_medicaments = random.randint(0,10)
               carte[x_porte][y_porte].stock_nourriture = random.randint(0,300)
               carte[x_porte][y_porte].type_bat="Magasin"
           elif taille_batiment == 18 :                                              # Ressources des Hôpitaux
               carte[x_porte][y_porte].stock_medicaments = random.randint(0,100)
               carte[x_porte][y_porte].type_bat="Hopital"

   return carte



Liste_zombie=[]
Liste_humain=[]
Liste_classe=[]
def implante_agents(carte,nbh,nbz):
   """
   liste[liste[int]]*int**2 -> liste[liste[int]]
   Prend une carte avec batiments et la renvoie avec humains et zombies
   """


   compteur_h = 0                                   # Nombre d'humains placés
   compteur_z = 0                                   # Nombre de zombies placés
   x = 0                                            # Coordonnés en x et y tirées aléatoirement où seront placés les H ou Z
   y = 0

   while compteur_h < nbh:                         # Tant que tous les humains n'ont pas été placés
       x = random.randint(1,len(carte[0])-1)       # Tirage des coordonnées
       y = random.randint(1,len(carte)-1)
       if not isinstance(carte[x][y], Batiment):
           carte[x][y] = Humain()
           carte[x][y].place_MATRICE=x,y
           Liste_humain.append(carte[x][y])
           Liste_classe.append(carte[x][y])
           compteur_h += 1                              # Incrémentation du compteur d'humains placés

   while compteur_z < nbz:                              # Tant que tous les zombies n'ont pas été placés
       x = random.randint(1,len(carte[0])-1)            # Tirage des coordonnées
       y = random.randint(1,len(carte)-1)
       if not isinstance(carte[x][y], Batiment)\
       and not isinstance(carte[x][y], Humain):
           carte[x][y] = Zombie()                       #Place un zombie
           carte[x][y].place_MATRICE=x,y
           Liste_zombie.append(carte[x][y])
           Liste_classe.append(carte[x][y])



           compteur_z += 1                              # Incrémentation du compteur de zombies placés
   return carte


def set_map(carte):
   """
   list[list[int*Object]] -> liste[list[Object]]
   Remplace les zéros de la matrice initiale par la classe Vide
   """
   for ligne in range (i):
       for colonne in range(j):
           if carte[ligne][colonne] == 0:
               carte[ligne][colonne] = Vide()
   return carte



def init_carte():
   """
   -> array[object]
   Rassemble les fonctions précédentes et rend la carte initialisée
   """

   carte0 = CreationMatriceZero(i,j)                        # Map initialisée avec des zéros
   carte0 = implante_batiments(carte0, nb_batiment)         # Implantation des batiments
   carte0 = implante_agents(carte0, nb_humain, nb_zombie)   # Implantation des differents agents
   carte0 = set_map(carte0)                                 # Correspondance Zéro - Vide
   carte0 = array(carte0)                                   # Liste[Liste[object]] -> array[object]
   return carte0

carte0 = init_carte()

#FONCTIONS AUXILIAIRES

def trouve_agent(carte, agent):
   """
   carte*object -> list[tuple[int,int]]
   """
   LR = []
   for ligne in range (i):
       for colonne in range(j):
           if isinstance(carte[ligne,colonne],agent):
               LR.append((ligne,colonne))
   return LR

def trouve_porte(carte):
   LR = []
   for ligne in range (i):
       for colonne in range(j):
           if isinstance(carte[ligne,colonne],Batiment) and carte[ligne,colonne].type == "Porte":
               LR.append((ligne,colonne))
   return LR
