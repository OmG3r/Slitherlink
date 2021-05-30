#importations
from fltk import * 
from time import sleep
from os import * 
from random import randint


# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

#image arrier plan  
PG = "ground.png"   #chemine des photo utiliser si il ne marche pas merci d'utiliser le chemin absolu (de votre ordinateur)
PG1 = "groundv7.png"   #chemine des photo utiliser si il ne marche pas merci d'utiliser le chemin absolu (de votre ordinateur)
PG_2 ="first1.png"  #chemine des photo utiliser si il ne marche pas merci d'utiliser le chemin absolu (de votre ordinateur)

#les option de jeu
VITE = False  
PACMAN = False
OBSTACLE = False
MULTI = False
MENU = True



def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):  # cree le cercle qui va forme la pomme 
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)   
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red',tag='mise')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen',tag='mise')


def affiche_serpent(serpent): # cree le serpent 1
    for boule in range(len(serpent)):
        x, y = case_vers_pixel(serpent[boule])  # à modifier !!!

        cercle(x, y, taille_case/2 + 1,
               couleur='black', remplissage='dodgerblue',tag="mise")

        rectangle(x-2, y-taille_case*.2, x+1, y-taille_case*.3,
                  couleur='darkgreen', remplissage='darkgreen',tag="mise")
        
        rectangle(x-2, y-taille_case*.2, x+1, y-taille_case*-.3,
                  couleur='darkgreen', remplissage='darkgreen',tag="mise")

def affiche_serpent1(serpent1): # cree le serpent 1
    for boule in range(len(serpent1)):
        x, y = case_vers_pixel(serpent1[boule])  # à modifier !!!

        cercle(x, y, taille_case/2 + 1,
               couleur='white', remplissage='black', tag = "mise")

        rectangle(x-2, y-taille_case*.2, x+1, y-taille_case*-.3,
                  couleur='darkgreen', remplissage='darkgreen',tag="mise")

        rectangle(x-2, y-taille_case*.2, x+1, y-taille_case*-.3,
                  couleur='darkgreen', remplissage='darkgreen',tag="mise")
        

def affiche_obstacles(obstacles):  #cree les obstacles
    for mine in obstacles:
        x, y = case_vers_pixel(mine)  # à modifier !!!

        cercle(x, y, taille_case/2 + 1,
               couleur='black', remplissage='gold',tag="mise")
        
def change_direction(direction, touche): # la fonction qui nous permet de recvoir une touche et l'a transformer a un movment 
    if touche == 'Up' and direction != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction

def change_direction1(direction1, touche): # la fonction qui nous permet de recvoir une touche et l'a transformer a un movment 
    if touche == 'z' and direction1 != (0, 1):
        # flèche haut pressée
        return (0, -1)
    elif touche == 's' and direction1 != (0, -1):
        return (0, 1)
    elif touche == 'q' and direction1 != (1, 0):
        return (-1, 0)
    elif touche == 'd' and direction1 != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction1

def maj_serpent(serpent, direction):  # la fonction qui nous permet de laisser le serpent dans la fenêtre de jeu (mode pacman desactiver)
    """fonction principale des tests lors des déplacements + event"""
    x_tete,y_tete = serpent[-1]
    simuX = x_tete+direction[0]
    simuY = y_tete+direction[1]
    if PACMAN: #mode pacman
        if 0 > simuY:
            simuY = 30
        elif simuY > 29:
            simuY = 0
        if 0 > simuX:
            simuX = 40
        elif simuX > 39:
            simuX = 0
    else: #mode pacman désactiver 
        if 0 > simuY or simuY > 29 or simuX < 0 or simuX > 39 : #quitter la fenêtre
            return False    #le fin de mode pacman

    if ((simuX,simuY) in serpent and len(serpent) > 1) or (simuX,simuY) in serpent1: # se manger ?
        return False
    elif (simuX,simuY) in obstacles: #se bouffe une mine ?
        return False
    elif (simuX,simuY) in pommes: #mange une pomme ?
        ajoute_pomme()
        pommes.remove((simuX,simuY))
    else:
        serpent.pop(0) #effacer son dernier element de la liste serpent (queue)
    serpent.append((simuX, simuY)) #ajout de la tete

    return True

def maj_serpent1(serpent1, direction1):
    """fonction principale des tests lors des déplacements + event"""
    x_tete,y_tete = serpent1[-1]
    simuX = x_tete+direction1[0]
    simuY = y_tete+direction1[1]
    if MULTI == True :
        if PACMAN:       #mode pacman
            if 0 > simuY:
                simuY = 30
            elif simuY > 29:
                simuY = 0
            if 0 > simuX:
                simuX = 40
            elif simuX > 39:
                simuX = 0
        else: #si pas pacman
            if 0 > simuY or simuY > 29 or simuX < 0 or simuX > 39 : #quitter le fenêtre de jeu
                return False

    if ((simuX,simuY) in serpent1 and len(serpent1) > 1) or (simuX,simuY) in serpent: #se manger 
        return False
    elif (simuX,simuY) in obstacles: # manger un obstacles
        return False
    elif (simuX,simuY) in pommes: #mange une pomme 
        ajoute_pomme()
        pommes.remove((simuX,simuY))
    else:
        serpent1.pop(0) #effacer son dernier element de la liste serpent (queue)
    serpent1.append((simuX, simuY)) #ajout de la tete

    return True



def ajoute_pomme(): # spawner les pommes
    """fonction ajoutant une pomme au terrain, ssi la nouvelle pomme
    spawn dans une case vide"""
    while True:
        simu = (randint(0,39),randint(0,29)) 
        if simu not in serpent and simu not in pommes and simu not in obstacles:
            pommes.append(simu)
            return None
        
def ajoute_obstacle(): #spawner ler obstacle aléatoirement
    """fonction ajoutant une pomme au terrain, ssi la nouvelle pomme
    spawn dans une case vide"""
    while True:
        simu = (randint(0,39),randint(0,29)) 
        if simu not in serpent and simu not in pommes and simu not in obstacles:
            obstacles.append(simu)
            return None
    
# programme principal
if __name__ == "__main__":
    while MENU:
        Bouton_JOUER = [(50, 340),(550, 430)]#coordonnées boutons JOUER
        Bouton_OBSTACLE = [(50, 50),(200, 110)]#coordonnées boutons obstacle
        Bouton_Pacman = [(220, 50),(370, 110)] #coordonnées boutons Pacman
        Bouton_vitesse = [(390, 50),(550, 110)] #coordonnées boutons vitesse
        Bouton_Multi = [(50, 160),(160, 325)] #coordonnées boutons Multi
        Bouton_Quitter = ([(440,160),(550,330)]) #coordonnées boutons quitter
        #DEBUT MENU
        
        cree_fenetre(taille_case * largeur_plateau,taille_case * hauteur_plateau)
        image(300,300, PG_2, ancrage='center')
        #boutons jouer

        rectangle(Bouton_JOUER[0][0], Bouton_JOUER[0][1], Bouton_JOUER[1][0], Bouton_JOUER[1][1],\
                  couleur='black', remplissage='green', epaisseur=3, tag='menu')
        texte(240,385,"☞Jouer",tag='menu')
        
        #boutons onstacle

        rectangle(Bouton_OBSTACLE[0][0], Bouton_OBSTACLE[0][1], Bouton_OBSTACLE[1][0], Bouton_OBSTACLE[1][1],\
                  couleur='black', remplissage='yellow', epaisseur=3, tag='menu')
        texte(50,70,"☞Obstacles",tag='menu',couleur='black',taille=19)
        
        #boutons PACMAN

        rectangle(Bouton_Pacman[0][0], Bouton_Pacman[0][1], Bouton_Pacman[1][0], Bouton_Pacman[1][1],\
                  couleur='black', remplissage='yellow', epaisseur=3, tag='menu')
        texte(220,70,"☞Pac-man",tag='menu',taille=19)

        #boutons Vitesse
 
        rectangle(Bouton_vitesse[0][0], Bouton_vitesse[0][1], Bouton_vitesse[1][0], Bouton_vitesse[1][1],\
                  couleur='black', remplissage='yellow', epaisseur=3, tag='menu')
        texte(390,70,"☞vitesse",tag='menu',taille=22)

        #boutons Multi joueur 
        
        rectangle(Bouton_Multi[0][0], Bouton_Multi[0][1], Bouton_Multi[1][0], Bouton_Multi[1][1],\
                  couleur='black', remplissage='cyan', epaisseur=3, tag='menu')
        texte(55,190,"☞Multi\njoueur",tag='menu',)

        
        #bouton Quitter
        rectangle(Bouton_Quitter[0][0], Bouton_Quitter[0][1], Bouton_Quitter[1][0], Bouton_Quitter[1][1],\
                  couleur='black', remplissage='red', epaisseur=3, tag='menu')
        texte(440,220,"☞\nQuitter",tag='menu',taille=21) 


        ###########################################"# a complete par les autre bouton est a changer les couleur et le police
        while True: #TANT QUE UN BOUTON A PAS ETE PRESSE
            clique = attend_clic_gauche()
            if Bouton_JOUER[0][0] <= clique[0] and clique[0] <= Bouton_JOUER[1][0] and \
               Bouton_JOUER[0][1] <= clique[1] and clique[1] <= Bouton_JOUER[1][1]:
                efface_tout()
                ferme_fenetre()
                break #si on a appuyé sur le bouton JOUER alors on procède à la suite, donc on sort du while
            elif Bouton_OBSTACLE[0][0] <= clique[0] and clique[0] <= Bouton_OBSTACLE[1][0] and \
               Bouton_OBSTACLE[0][1] <= clique[1] and clique[1] <= Bouton_OBSTACLE[1][1]:
                OBSTACLE = not OBSTACLE
            elif Bouton_Quitter[0][0] <= clique[0] and clique[0] <= Bouton_Quitter[1][0] and \
               Bouton_Quitter[0][1] <= clique[1] and clique[1] <= Bouton_Quitter[1][1]:
                    ferme_fenetre()
            elif Bouton_Pacman[0][0] <= clique[0] and clique[0] <= Bouton_Pacman[1][0] and \
               Bouton_Pacman[0][1] <= clique[1] and clique[1] <= Bouton_Pacman[1][1]:
                PACMAN = not PACMAN
            elif Bouton_Multi[0][0] <= clique[0] and clique[0] <= Bouton_Multi[1][0] and \
               Bouton_Multi[0][1] <= clique[1] and clique[1] <= Bouton_Multi[1][1]:
                MULTI = not MULTI        

        #FIN MENU

        
        # initialisation du jeu
        framerate = 10   # taux de rafraîchissement du jeu en images/s
        direction = (0, 0)  # direction initiale du serpent
        direction1 = (0, 0)
        pommes = [(20,15)] # liste des coordonnées des cases contenant des pommes
        obstacles = [] # liste des coordonnées des cases contenant des obstacles
        serpent = [(0,0)] # liste des coordonnées de cases adjacentes décrivant le serpent
        if MULTI == True :
            serpent1 = [(39,29)] # liste des coordonnées de cases adjacentes décrivant le serpent 2
        elif MULTI == False :
            serpent1 = [(50,50)]
            
        for _ in range(OBSTACLE*randint(5,15)): #spowner les obstacle avec randint
            ajoute_obstacle()

        
        cree_fenetre(taille_case * largeur_plateau,taille_case * hauteur_plateau)
        if PACMAN == True : # image 1 sans bordure rouge (mode pacman True)
            image(299,299, PG, ancrage='center')
        elif PACMAN == False : # image deux avec la bordure rouge (mode pacman False)
            image(299, 225, PG1, ancrage='center')
        texte(250, 200, "PLAY", taille = 35, couleur = 'white', tag = "mise")
        mise_a_jour()
        attend_ev()
        # boucle principale
        jouer = True
        while jouer:
            # affichage des objets
            efface("mise")  
            affiche_pommes(pommes) #appele le fonction affiche_pommes
            affiche_serpent(serpent) #appele le fonction affiche_serpent
            affiche_serpent1(serpent1*MULTI) # appele le fonction affiche_serpent1
            affiche_obstacles(obstacles)

            texte(10, 390, f"Pomme P1: {len(serpent)-1}",couleur = 'Black',taille = 15, tag = "mise")# afficher score de joueur 1
            if MULTI == True : 
                texte(10, 420, f"Pomme P2: {len(serpent1)-1}",couleur = 'aqua',taille = 15, tag = "mise") # afficher le score de joueur 2
            mise_a_jour()

            # gestion des événements
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte': #quitter le jeu
                jouer = False
            elif ty == 'Touche': # detecter un touche
                direction = change_direction(direction, touche(ev))
                direction1 = change_direction1(direction1, touche(ev))
            if not maj_serpent(serpent, direction):
                if MULTI == True : #afficher le texte si le 2eme joueur a gagner
                    texte(50,320, f"le 2éme joueur a gagner ( ͡° ͜ʖ ͡°)  : {len(serpent1)- 1}",couleur='orange',taille=20,police='arial')
                break #sortie du jeu
            if not maj_serpent1(serpent1, direction1):
                if MULTI == True : # afficher le texte si le 1ere joueur a gagner
                    texte(50,320, f"le 1ére joueur a gagner ᕦ( ͡° ͜ʖ ͡°)ᕤ : {len(serpent1)- 1}",police='arial',couleur='orange',taille=20)
                break #sortie du jeu
            framerate += 0.02*((len(serpent)+1)%16 == 0)*VITE
            sleep(2/framerate)
        if MULTI == False :
            texte(160, 110, f"vous avez perdu Noob\nVotre Score :  {len(serpent)-1}\nune autre partie ??", taille = 20, couleur = 'black',police='arial')
        mise_a_jour()
        attend_ev()
        # fermeture et sortie
        ferme_fenetre()
