#PARAMETRES GENERAUX

i = 150           # Nombre de lignes de la Carte
j = 150           # Nombre de colonnes de la Carte

nb_simulations = 500
vitesse_simulations=100  #Augmenter pour que le programme ralentisse

nb_humain = 50  # Nombre d'humains
nb_zombie = 150  # Nombre de zombies
nb_batiment = 30  # #Nombre de batiments

#Paramétrage de la taille des batiments
taille_des_maisons=range(4,7)
taille_des_armureries= 7
taille_des_magasins=range(8,12)
taille_des_hopitaux=18



#Paramétrages des initialisations et des valeurs maximales

Munitions_max = 20      # Quantité maximale que peut avoir un humain dans son sac
Médicaments_max = 10    # Quantité maximale que peut avoir un humain dans son sac
Nourriture_max = 20     # Quantité maximale que peut avoir un humain dans son sac

Odorat_Z = 10           # Zone d'odorat des zombies
Odorat_H = 10           # Zone d'alerte des humains

faim_humain= 40
munition_début=3
médicaments_début=0
nourriture_début=0

pdv_rendus=2            #PDV rendu par médicaments
temps_perdre_pdv=20     #Temps/iterrations avant qu'un humain perde de la vie lorsque sa Faim est à 0
faim_rendu=20           #Faim rendu par les médicaments


taux_réussite_tir1,taux_réussite_tir2=0,1
taux_de_réussite_zombies1,taux_de_réussite_zombies2=0,1    #Taux de réussite de la transformation d'un humain en zombie après avoir été mordu
########################################################################################################
