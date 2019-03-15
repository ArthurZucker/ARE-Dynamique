import math
import random
import numpy as np
from parameteres import *
#!/usr/bin/env python
# -*- coding: utf-8 -*-


def liste_tuples(liste):
    return [(k.place_MATRICE) for k in liste]

#Definition de la classe Humain
class Humain:
    """
    Classe définissant un humain, qui peux se déplacer, fuir les zombies
    """
     #A l'initialisation, le premier humain crée est l'humain 0
    num_humain=0
    def __init__(self):
        self.nom = Humain.num_humain
        #On incrémente pour nommer les autres zombies
        Humain.num_humain += 1
        self.compteur_temps=0
        self.pdv=random.randint(40,100)
        #parametre global
        self.faim=faim_humain
        self.compteur_faim=0
        self.sac={"Munitions":munition_début,"Médicaments":médicaments_début,"Nourriture":nourriture_début}  # Mun max : 30
        #initialisation à l'aide des paramètre globaux

    def __str__(self):
        return "Humain " + str(self.nom)

    def __repr__(self):
        return self.__str__()


    def sentir_zombie(self,carte,Liste_zombie):
        i_humain,j_humain=self.place_MATRICE
        self.place_matrice=self.place_MATRICE
        liste_zombie = liste_tuples(Liste_zombie)
        dmin = 10000000                                  # Distance supposée du zombie le plus proche
        i_zombie = None
        j_zombie = None
        self.Zombie_le_plus_proche = (i_zombie, j_zombie)
        self.liste_zombie_proche = []
        for e in range(len(liste_zombie)):
            i_zombieTempo, j_zombieTempo = liste_zombie[e]
            if i_zombieTempo in range((i_humain-Odorat_H),(i_humain+Odorat_H+1))\
            and j_zombieTempo in range((j_humain-Odorat_H),(j_humain+Odorat_H+1)):         # L'humain est dans un voisinage +/- 10 du zombie
                 self.liste_zombie_proche +=[(i_zombieTempo,j_zombieTempo)]
                 dz=math.sqrt((i_zombieTempo - i_humain)**2+(j_zombieTempo - j_humain)**2)
                 if (dz<dmin):                        # Compare la distance H-Z la plus petite trouvée
                    i_zombie = i_zombieTempo                                          # Garde en mémoire les coordonnées du zombie le plus proche
                    j_zombie = j_zombieTempo
                    dmin=dz
                    self.Zombie_le_plus_proche = (i_zombieTempo,j_zombieTempo)
                    self.Zombie_le_plus_proche2= Liste_zombie[e]

    def Pdv(self,carte,Liste_humain,Liste_classe):
        """Etat de la vie de l'humain """
        i_humain, j_humain = self.place_MATRICE
        if self.faim == 0:
            if self.compteur_temps < temps_perdre_pdv:
                self.compteur_temps += 1
            else:
                self.pdv -= 1
                self.compteur_temps = 0
                self.faim=0
        if self.pdv<=80 and self.sac["Médicaments"]>1:
            self.sac["Médicaments"]-=1
            self.pdv+=pdv_rendus
        if self.pdv==0:
            carte[i_humain,j_humain]=Zombie()
            carte[i_humain,j_humain].place_MATRICE=i_humain,j_humain
            Liste_humain.remove(self)
            Liste_classe.remove(self)
            #Append ??
            Liste_zombie+=carte[i_humain,j_humain]
            Liste_classe+=carte[i_humain,j_humain]

    def Faim(self):
        if self.sac["Nourriture"]>=1 and self.faim<=0:

                self.sac["Nourriture"]-=1
                self.faim+=faim_rendu

        if self.compteur_faim < 2:
            self.compteur_faim += 1
        elif self.faim>0:
            self.faim -=1
            self.compteur_faim=0

    def shoot(self,carte,Liste_zombie,Liste_classe):
        if len(self.liste_zombie_proche)<=2 and len(self.liste_zombie_proche)>0 :
            if self.sac["Munitions"]>=1:
                x=random.randint(taux_réussite_tir1,taux_réussite_tir2)
                print(x)
                if x==1 and self.Zombie_le_plus_proche2 != None:
                    Liste_classe.remove(self.Zombie_le_plus_proche2)
                    Liste_zombie.remove(self.Zombie_le_plus_proche2)
                    carte[self.Zombie_le_plus_proche]=Vide()
                    self.sac["Munitions"]=self.sac["Munitions"]-1
                    print(self.sac)
                    print(carte[self.Zombie_le_plus_proche])
                    print("Un zombie s'est fait tué")
                else:
                    self.sac["Munitions"]=self.sac["Munitions"]-1
                    print("RATE")
                    print(self.sac)

    def prendre_nourr(self,carte):
        i_humain, j_humain = self.place_MATRICE
        for x in range(-1,2):
            for y in range (-1,2):#Vérifie qu'il y a une porte autour de l'humain

                if (i_humain + x in range(i)) and (j_humain + y in range(j)):
                    if not isinstance(carte[i_humain+x,j_humain+y], Zombie) and not isinstance(carte[i_humain+x,j_humain+y], Vide) and not isinstance(carte[i_humain+x,j_humain+y], Humain) and carte[i_humain+x, j_humain+y].type == "Porte":
                        posx_porte = i_humain+x
                        posy_porte = j_humain+y

                        if not carte[posx_porte,posy_porte].stock_medicaments == 0 :    # Si le stock n'est pas vide
                            print(self.sac)
                            if not self.sac["Médicaments"]== Médicaments_max :          # Si le sac n'est pas plein
                                if carte[posx_porte,posy_porte].stock_medicaments >= (Médicaments_max - self.sac["Médicaments"]) : # Si stock >= Place dans le sac
                                    carte[posx_porte,posy_porte].stock_medicaments -= (Médicaments_max - self.sac["Médicaments"])  # Vide le stock de la quantité à remplir dans le sac
                                    self.sac["Médicaments"] = Médicaments_max                                                      # Rempli au max le sac
                                if carte[posx_porte,posy_porte].stock_medicaments < (Médicaments_max - self.sac["Médicaments"]) :  # Si stock < Place dans le sac
                                    self.sac["Médicaments"] += carte[posx_porte,posy_porte].stock_medicaments                      # Rempli le sac avec la taille du stock
                                    carte[posx_porte,posy_porte].stock_medicaments -= 0 #Médicaments_max-self.sac["Médicaments"]  # Vide entièrement le stock

                        if not carte[posx_porte,posy_porte].stock_munitions == 0 :  # Même chose mais avec une autre ressource

                            if not self.sac["Munitions"]== Munitions_max :
                                if carte[posx_porte,posy_porte].stock_munitions >= (Munitions_max - self.sac["Munitions"]) :
                                    carte[posx_porte,posy_porte].stock_munitions -= (Munitions_max - self.sac["Munitions"])
                                    self.sac["Munitions"] = Munitions_max
                                if carte[posx_porte,posy_porte].stock_munitions < (Munitions_max - self.sac["Munitions"]) :
                                    self.sac["Munitions"] += carte[posx_porte,posy_porte].stock_munitions
                                    carte[posx_porte,posy_porte].stock_munitions = 0     #Probleme: tu remet à 0 le nombres de munitions....

                        if not carte[posx_porte,posy_porte].stock_nourriture == 0 :  # Même chose mais avec une autre ressource

                            if not self.sac["Nourriture"]== Nourriture_max :
                                if carte[posx_porte,posy_porte].stock_nourriture >= (Nourriture_max - self.sac["Nourriture"]) :
                                    carte[posx_porte,posy_porte].stock_nourriture -= (Nourriture_max - self.sac["Nourriture"])
                                    self.sac["Nourriture"] = Nourriture_max
                                if carte[posx_porte,posy_porte].stock_nourriture < (Nourriture_max - self.sac["Nourriture"]) :
                                    self.sac["Nourriture"] += carte[posx_porte,posy_porte].stock_nourriture
                                    carte[posx_porte,posy_porte].stock_nourriture = 0




    def move(self,carte,i_destination, j_destination):

        i_humain, j_humain = self.place_matrice
        i_prox, j_prox = i_humain, j_humain
        i_boussole = 0                                  # Coordonnées de la direction
        j_boussole = 0
        if i_humain < i_destination :                   # Analyse du chemin idéal
            i_prox += 1
            i_boussole = 1

        elif i_humain > i_destination :
            i_prox -= 1
            i_boussole = -1

        if j_humain < j_destination :
            j_prox += 1
            j_boussole = 1

        elif j_humain > j_destination :
            j_prox -= 1
            j_boussole = -1
        if isinstance((carte[i_prox,j_prox]),Vide):                   # Déplacement prévu
            carte[i_prox,j_prox] = self
            self.place_matrice=i_prox,j_prox
            self.place_MATRICE=self.place_matrice
            carte[i_humain,j_humain] = Vide()
        elif isinstance(carte[i_prox - i_boussole ,j_prox],Vide):   # Alternative si chemin obstrué
            carte[i_prox - i_boussole ,j_prox] = self
            self.place_matrice=i_prox - i_boussole ,j_prox
            self.place_MATRICE=self.place_matrice
            carte[i_humain,j_humain] = Vide()
        elif isinstance(carte[i_prox,j_prox - j_boussole],Vide):
            carte[i_prox ,j_prox - j_boussole] = self
            self.place_matrice=i_prox ,j_prox - j_boussole
            self.place_MATRICE=self.place_matrice
            carte[i_humain,j_humain] = Vide()

        elif not isinstance(carte[i_prox,j_prox], Zombie) and not isinstance(carte[i_prox,j_prox], Vide) and not isinstance(carte[i_prox,j_prox], Humain) and (carte[i_prox,j_prox].type=='Porte'):
            self.prendre_nourr(carte)

        else:
                compteur_boucle = 0                                 # Compteur de sortie de boucle
                while compteur_boucle == 0 :

                    x = random.randint(-1,1)                        # Tirage du déplacement vertical
                    y = random.randint(-1,1)                        # Tirage du déplacement horizontal
                    #i_humain, j_humain = self.place_matrice
                    i1 = i_humain + x
                    j1 = j_humain + y
                    if (i1 in range(i)) and (j1 in range(j)):       # Vérifie que le déplacement voulu ne sort pas de la map
                        if isinstance(carte[i1,j1], Vide):
                            carte[i1,j1] = self
                            carte[i_humain,j_humain] = Vide()
                            self.place_matrice=i1,j1
                            self.place_MATRICE=self.place_matrice
                            compteur_boucle += 1





    def run(self,carte,Liste_porte):
        """
     Lance la capacité de l'humain à se déplacer
     """
        i_humain, j_humain = self.place_matrice
        L_P=liste_tuples(Liste_porte)
        for x in range(len(self.liste_zombie_proche)):
                if len(self.liste_zombie_proche) <=x and self.sac["Munitions"] < x:
                    i_porte, j_porte = trouve_batiment("Maison",i_humain,j_humain,carte,Liste_porte)
                    self.move(carte,i_porte, j_porte)


        if len(self.liste_zombie_proche) == 0:                         # Si il n'y a pas de zombie à l'horizon
            if self.sac["Munitions"] < 1:                        # Déplacement vers une porte quelconque
                i_porte, j_porte = trouve_batiment("Armurerie",i_humain,j_humain,carte,Liste_porte)

                self.move(carte, i_porte, j_porte)


            elif self.faim < 20 and self.sac["Nourriture"] == 0 : # Déplacement vers n'importe quelle porte

                dmin=1000000
                for e in range(0,len(L_P)):
                    i_portetempo, j_portetempo = (L_P)[e] # L'humain est dans un voisinage +/- 10 du zombie
                    dz=math.sqrt((i_portetempo - i_humain)**2+(j_portetempo - j_humain)**2)
                    if (dz<dmin) and Liste_porte[e].stock_nourriture>0:                        # Compare la distance H-Z la plus petite trouvée
                        i_porte = i_portetempo                                          # Garde en mémoire les coordonnées du zombie le plus proche
                        j_porte = j_portetempo
                        dmin=dz
                        self.Porte_la_plus_proche = (i_porte,j_porte)  # Fonction qui rend toute les portes
                self.move(carte, i_porte, j_porte)

            elif self.pdv < 30 and self.sac["Médicaments"]==0:
                i_porte, j_porte = trouve_batiment("Hôpital",i_humain,j_humain,carte,Liste_porte)
                self.move(carte,i_porte, j_porte)
            else:
                compteur_boucle = 0                                 # Compteur de sortie de boucle
                while compteur_boucle == 0 :

                    x = random.randint(-1,1)                        # Tirage du déplacement vertical
                    y = random.randint(-1,1)                        # Tirage du déplacement horizontal
                    #i_humain, j_humain = self.place_matrice
                    i1 = i_humain + x
                    j1 = j_humain + y
                    if (i1 in range(i)) and (j1 in range(j)):       # Vérifie que le déplacement voulu ne sort pas de la map
                       if isinstance(carte[i1,j1], Vide):

                           carte[i1,j1] = self
                           carte[i_humain,j_humain] = Vide()
                           self.place_matrice=i1,j1
                           self.place_MATRICE=self.place_matrice
                           compteur_boucle += 1


        else:
            compteur_boucle = 0                                 # Compteur de sortie de boucle
            while compteur_boucle == 0 :

                x = random.randint(-1,1)                        # Tirage du déplacement vertical
                y = random.randint(-1,1)                        # Tirage du déplacement horizontal
                #i_humain, j_humain = self.place_matrice
                i1 = i_humain + x
                j1 = j_humain + y
                if (i1 in range(i)) and (j1 in range(j)):       # Vérifie que le déplacement voulu ne sort pas de la map
                   if isinstance(carte[i1,j1], Vide):
                        carte[i1,j1] = self
                        carte[i_humain,j_humain] = Vide()
                        self.place_matrice=i1,j1
                        self.place_MATRICE=self.place_matrice
                        compteur_boucle += 1




########################################################################################################
#FONCTIONS AUXILLIARES



def liste_porte_Bat(carte,type_batiment,Liste_porte):
    """
 Rend la liste des coordonnées de l'ensemble des portes des batiments convoités
 """
    liste_portes_desirees = []
    E=set()
    L=(Liste_porte)
    for k in L:
        i_porte,j_porte=k.place_MATRICE
        if k.type_bat==type_batiment:
            liste_portes_desirees.append((i_porte,j_porte))
    return liste_portes_desirees

def trouve_batiment(type_batiment,i_humain,j_humain,carte,Liste_porte):
    """
 Rend les coordonnées de la porte du batiment convoité le plus proche
 """
    L = liste_porte_Bat(carte, type_batiment,Liste_porte)
    distance = 1000
    i_Bat_proche,j_Bat_proche=None,None
    for k in range(len(L)):
        i_porte,j_porte = L[k]
        dz=math.sqrt((i_porte-i_humain)**2+(j_porte-j_humain)**2)
        if min (dz,distance)==dz:
                #if Liste_porte[k].stock_medicaments != 0 or Liste_porte[k].stock_nourriture !=0 or Liste_porte[k].stock_munitions != 0:
                distance = dz
                i_Bat_proche,j_Bat_proche= i_porte,j_porte
    return i_Bat_proche,j_Bat_proche



#####################################################################################################
#ZOMBIE

class Zombie:

    """
 Classe définissant un zombie, qui peux se déplacer et cherche à tuer les humains
 """

    num_zombie=0

    def __init__(self):
        self.nom = Zombie.num_zombie                        # Attribue le nom à chaque zombie
        Zombie.num_zombie += 1
        self.comp=0                           # Compteur pour différencier chaque zombie
    def __str__(self):
        return "Zombie " + str(self.nom)
    def __repr__(self):
        return self.__str__()
    def sentir(self, carte,Liste_humain):

        i_zombie,j_zombie=self.place_MATRICE
        liste_humain = liste_tuples(Liste_humain)          # Arrange cette liste en liste de tuples
        self.place_matrice = i_zombie ,j_zombie
        self.place_MATRICE=self.place_matrice
        dmin = 1000                                     # Distance supposée du plus proche humain
        i_humain_cible = None                               # Coordonnée i de l'humain le plus proche
        j_humain_cible = None                               # Coordonnée j de l'humain le plus proche
        for X in range(len(liste_humain)):
            i_humain, j_humain = liste_humain[X]
            if i_humain in range((i_zombie-Odorat_Z),(i_zombie+Odorat_Z+1)) and j_humain in range((j_zombie-Odorat_Z),(j_zombie+Odorat_Z+1)):
                dz=math.sqrt(((i_humain - i_zombie)**2)+((j_humain - j_zombie)**2))
                if dz<dmin:                        # Compare la distance H-Z avec la plus petite trouvée
                    i_humain_cible = i_humain
                    j_humain_cible = j_humain
                    dmin=dz
        self.coord_humain=(i_humain_cible ,j_humain_cible)


    def move(self, carte,Liste_humain,Liste_zombie,Liste_classe):
        if self.coord_humain==(None,None):
            compteur_boucle = 0
            while compteur_boucle == 0 :
                x = random.randint(-1,1)                        # Tirage du déplacement vertical
                y = random.randint(-1,1)                        # Tirage du déplacement horizontal
                i_zombie, j_zombie = self.place_matrice
                i1 = i_zombie + x
                j1 = j_zombie + y
                if (i1 in range(i)) and (j1 in range(j)):       # Vérifie que le déplacement voulu ne sort pas de la map
                    if isinstance(carte[i1,j1], Vide):
                        carte[i1,j1] = self
                        carte[i_zombie,j_zombie] = Vide()
                        self.place_matrice=i1,j1
                        self.place_MATRICE=self.place_matrice
                        compteur_boucle += 1
        else:
            A1,B1=0,0
            A3,B3=self.coord_humain
            A,B=self.place_matrice
            A1,B1,A2,B2=nouveau_coordonnées(A3,B3,A,B)
            print(carte[A2,B2])
            if isinstance(carte[A2,B2], Vide):
                carte[A2,B2]=self
                carte[A,B]=Vide()
                self.place_matrice=A2,B2
                self.place_MATRICE=self.place_matrice

            if isinstance(carte[A2,B2],Humain):
                x=random.randint(taux_de_réussite_zombies1,taux_de_réussite_zombies2)
                if x==1:

                    Liste_humain.remove(carte[A2,B2])
                    Liste_classe.remove(carte[A2,B2])
                    carte[A2,B2]=self
                    carte[A,B]=Vide()
                    print(Liste_humain)
                    self.place_matrice=A2,B2
                    self.place_MATRICE=self.place_matrice

                else:

                    print(Liste_zombie)
                    Liste_humain.remove(carte[A2,B2])
                    Liste_classe.remove(carte[A2,B2])
                    carte[A2,B2]=self
                    carte[A,B]=Zombie()
                    carte[A,B].place_MATRICE=A,B
                    carte[A,B].place_matrice=carte[A,B].place_MATRICE
                    self.place_matrice=A2,B2
                    self.place_MATRICE=self.place_matrice
                    Liste_zombie+=[carte[A,B]]
                    Liste_classe.append(carte[A,B])
                    print(Liste_zombie)

def nouveau_coordonnées(H1,H2,Z1,Z2):
    if H1<=Z1:
        Z1-=1
    if H1>=Z1:
        Z1+=1
    if H2<=Z2:
        Z2-=1
    if H2>=Z2:
        Z2+=1
    return (H1,H2,Z1,Z2)


########################################################################################################
#VIDE

class Vide:
    def __repr__(self):
        return "Vide"
