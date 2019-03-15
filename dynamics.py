import matplotlib.animation as animation
from parameteres import *
from classes import *
from env import *

###############################################################################


evolution_H = []    # Liste du nombre d'humains à chaque tour
evolution_Z = []    # Liste du nombre de zombies à chaque tour

###############################################################################
Liste_humain
Liste_zombie
Liste_classe
Liste_porte
Liste_batiment
Liste_hopital
taillex=i
tailley=j
print(liste_tuples(Liste_humain),liste_tuples(Liste_zombie))
def compte_agent(carte,agent):
    """
 carte->int
 Rend le nombre d'agent spécifié sur la carte à l'instant t
 """
    compteur_agent = 0
    for ligne in range(i):
        for colonne in range(j):
            if isinstance(carte[ligne,colonne],agent):
                compteur_agent +=1
    return compteur_agent


def dynamique(carte):
    """
    Lance la simulation avec un nombre d'itérations choisi
    """
    E=set()
    for classe in (Liste_classe):
            if isinstance(classe,Zombie) and classe not in E:     # Lance les fonctions propres aux zombies
                E.add(classe)
                classe.sentir(carte,Liste_humain)
                classe.move(carte,Liste_humain,Liste_zombie,Liste_classe)
            if isinstance(classe,Humain) and classe not in E:   # Lance les fonctions propres aux humains
                E.add(classe)
                classe.sentir_zombie(carte,Liste_zombie)
                classe.Faim()
                classe.Pdv(carte,Liste_humain,Liste_classe)
                classe.run(carte,Liste_porte)
                classe.shoot(carte,Liste_zombie,Liste_classe)


    evolution_H.append(len(Liste_humain))
    evolution_Z.append(len(Liste_zombie))

AA=array(CreationMatriceZero(i, j))
def affichage(carte,Liste_batiment,Liste_classe):
    #carte_affiche = np.zeros(carte.shape)
    carte_affiche = np.zeros(AA.shape)
    for k in Liste_classe:
        if isinstance(k, Zombie):
            A,B=k.place_MATRICE
            carte_affiche[A,B] = 1
        if isinstance(k, Humain):
            A,B=k.place_MATRICE
            carte_affiche[A,B]=2
    for k1 in Liste_batiment:
        if k1.type == "Porte":
            A,B=k1.place_MATRICE
            carte_affiche[A][B] = 3.1
        elif k1.type == "Maison":
            A,B=k1.place_MATRICE
            carte_affiche[A][B] = 3.2
        elif k1.type == "Magasin":
            A,B=k1.place_MATRICE
            carte_affiche[A][B] = 3.3
        elif k1.type == "Armurerie":
            A,B=k1.place_MATRICE
            carte_affiche[A][B] = 3.4
        elif k1.type == "Hôpital":
            A,B=k1.place_MATRICE
            carte_affiche[A][B] = 3.5

    return carte_affiche




def init_affichage(carte):
    """
 carte[object] -> map
 Sort une carte graphique
 """
    carte_affiche = affichage(carte,Liste_batiment,Liste_classe)
    size = np.array(carte.shape)
    dpi = 72.0
    #figsize = size[1]/float(dpi), size[0]/float(dpi)
    figsize = size[1]/10, size[0]/10
    fig = plt.figure(figsize = figsize, dpi = dpi , facecolor = "White")
    cmap = mpl.colors.ListedColormap(["White","Red","Green","saddlebrown","grey","royalblue","olive","salmon"])
    bounds=(0, 1, 2, 3.1, 3.2, 3.3, 3.4, 3.5, 4)   # Le 4 n'existe pas mais permet au code de fonctionner ! :)
    norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
    img = plt.imshow(carte_affiche,interpolation="nearest",cmap=cmap,norm=norm)
    plt.colorbar(img,cmap=cmap,norm=norm,boundaries=bounds,ticks=bounds)
    return fig,img

fig,img = init_affichage(carte0)


def update(t, *args):
   """
 Rafraichit la carte
 """
   print ("formal arg:", t)
   for arg in args:
       print ("another arg:", arg)
   dynamique(carte0)
   c = affichage(carte0,Liste_batiment,Liste_classe)
   img.set_array(c)
   return img,

ani = animation.FuncAnimation(fig, update, frames = range(nb_simulations), interval = vitesse_simulations  , repeat = False )
plt.show()


def courbes_suivi(carte):
    """
   Affiche les courbes de suivi
   """

    x1 = list(range(nb_simulations + 1))
    print(evolution_H)
    plt.plot(x1,evolution_H,"green")
    plt.plot(x1,evolution_Z,"red")
    plt.axis([0, len(evolution_H)-1, 0, max(max(evolution_H)+2, max(evolution_Z))+2])
    plt.title('Evolution Humains (green) et Evolution Zombies (red)')
    plt.show()
