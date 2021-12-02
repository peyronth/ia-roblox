############################################################################################
####                                PROJET IA 41 ROBOT
###                             Samuel Bernard - Thomas Peyron
############################################################################################

import random

#Plateau contient les cases du plateau.
#Les cases sont un tableau de type [id case, couleur case, mur droit, mur bas, mur gauche, mur haut]
#Avec couleur case 0=>Aucune 1=>Bleu 2=>Jaune 3=>Vert 4=>Rouge 5=>Blocked
plateau = []


#Declaration des 4 pions, chacun comprenant une abcisse et une ordonnée
#Chaque pion est une liste comprenant une valeur d'abcisse et d'ordonnée
bleu = []
jaune = []
vert = []
rouge = []

#Declaration de la cible
#Liste comprenant deux coordonées de position et un chiffre déterminant la couleur du pion devant atteindre la cible
cible = []



def display_plateau():
    
    global plateau, cible
    
    #affichage du mur haut
    print("  _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _")
    for y in range(16):
        line=""
        line_down=""
        for x in range(16):
            #POUR CHAQUE CASE ON DETERMINE LES ELEMENTS
            #Type de case
            if(plateau[y][x][1]==0):type=" □ "
            elif(plateau[y][x][1]==5):type=" ■ "
            elif(plateau[y][x][1]==1):type=" B "
            elif(plateau[y][x][1]==2):type=" J "
            elif(plateau[y][x][1]==3):type=" V "
            elif(plateau[y][x][1]==4):type=" R "
            elif(y== cible[0] and x==cible[1]):type=" O "

            #Présence de murs latéraux
            if(x==0):                                                                                               #colonne bord gauche
                line+="|"
            if (plateau[y][x][2]==1 or (x+1<=15 and plateau[y][x+1][4]==1)):                                         #Si mur à droite ou mur sur la prochaine case à gauche
                line+=type+"|"
            else:
                line+=type+" "
            
            #Présence de murs horizontaux
            if(plateau[y][x][3]==1 or (y+1<=15 and plateau[y+1][x][5]==1)):
                line_down+="  _ "
            else:
                line_down+="    "

        print(line)
        print(line_down)

def init_plateau():
    
    global bleu, jaune, vert, rouge, cible
    
    plateau=[]
    for y in range(16):
        line_array=[]
        for x in range(16):
            
            mur_droit=mur_gauche=mur_haut=mur_bas=type=0

            #On met en place les murs du bord du terrain
            if(x==15):
                mur_droit=1
            elif(x==0):
                mur_gauche=1

            #Murs verticaux de bord de terrain
            if(y==0):
                mur_haut=1
            elif(y==15):
                mur_bas=1
        
            #mise en place des cases bloquées au milieu du terrai
            if((x==7 or x==8) and (y==7 or y==8)):
                type=5
                if(x==7):mur_gauche=1
                else:mur_droit=1
                if(y==7):mur_haut=1
                else:mur_bas=1

            line_array.append([x+y*16,type,mur_droit,mur_bas,mur_gauche,mur_haut,x,y])

        plateau.append(line_array)
    #mise en place des autre murs ALEATOIRE

    #2 Murs attenant à chaque paroi exterieur
    #Parois Verticales
    plateau[random.randint(0, 6)][0][3]=1
    plateau[random.randint(7, 14)][0][3]=1
    plateau[random.randint(0, 6)][15][3]=1
    plateau[random.randint(7, 14)][15][3]=1
    #Parois horizontales
    plateau[0][random.randint(0, 6)][2]=1
    plateau[0][random.randint(7, 14)][2]=1
    plateau[15][random.randint(0, 6)][2]=1
    plateau[15][random.randint(7, 14)][2]=1

    #4 Angle par quart de tableau chaque angle ne doit pas toucher une autre parois
    for h_middle in range(2):
        for v_middle in range(2):
            for i in range(2):
                x=random.randint(1, 6)+6*(h_middle)
                y=random.randint(1, 6)+6*(v_middle)
                plateau[x][y][3]=1
                plateau[x][y][2]=1
            for i in range(2):
                x=random.randint(1, 6)+6*(h_middle)
                y=random.randint(1, 6)+6*(v_middle)
                plateau[x][y][4]=1
                plateau[x][y][5]=1

    #Type des cases dont les coordonnées sont celles des pions correspond :
    #1 : bleu
    #2 : jaune etc.
    plateau[bleu[0]][bleu[1]][1] = 1
    plateau[jaune[0]][jaune[1]][1] = 2
    plateau[vert[0]][vert[1]][1] = 3
    plateau[rouge[0]][rouge[1]][1] = 4
    
    return plateau


#Mise à jour du plateau lorsqu'un ou plusieurs pions ont été déplacés
def update_plateau():
    
    global plateau
    global bleu, jaune, vert, rouge
    
    #Le type de la case du plateau dépend de la présence d'un pion et de sa couleur
    plateau[bleu[0]][bleu[1]][1] = 1
    plateau[jaune[0]][jaune[1]][1] = 2
    plateau[vert[0]][vert[1]][1] = 3
    plateau[rouge[0]][rouge[1]][1] = 4
    

#Initialisation des deux coordonnées d'un pion
def init_pion():
    pion = []
    
    #Génération de deux entiers aléatoires différents de 7 et 8
    #Une case avec l'une de ses coordonnées à 7 ou 8 est une des cases bloquées
    #au centre du plateau
    condition = True
    while condition == True:
        y = random.randint(0,15)
        x = random.randint(0,15)
        if(x!=7 and x!=8 and y!=7 and y!=8):
            condition = False
            
    #Ordonnée : coordonnée y comprise dans les cases du plateau
    #Abcisse : coordonnée x comprise dans les cases du plateau
    pion = [y,x]
    return pion


#Supprimer et vérifie si le type de la case est carré vide uniquement
def isEmpty(p_case):
    global plateau
    return(plateau[p_case[0]][p_case[1]][1] >= 1 and plateau[p_case[0]][p_case[1]][1] <= 4)


def moveLeft(p_pion):
    
    global plateau
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][4] != 1 and plateau[nextPion[0]][nextPion[1]-1][2] != 1 and isEmpty([nextPion[0],nextPion[1]-1]):
        nextPion[1]-=1
    
    print(nextPion)
    return nextPion
  

def moveRight(p_pion):
    
    global plateau
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][2] != 1 and plateau[nextPion[0]][nextPion[1]+1][4] != 1 and isEmpty([nextPion[0],nextPion[1]+1]):
        nextPion[1]+=1
    
    print(nextPion)
    return nextPion


def moveUp(p_pion):
    
    global plateau
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][5] != 1 and plateau[nextPion[0]-1][nextPion[1]][3] != 1 and isEmpty([nextPion[0]-1,nextPion[1]]):
        nextPion[0]-=1
    
    print(nextPion)
    return nextPion


def moveDown(p_pion):
    
    global plateau
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][3] != 1 and plateau[nextPion[0]+1][nextPion[1]][5] != 1 and isEmpty([nextPion[0]+1,nextPion[1]]):
        nextPion[0]+=1
    
    print(nextPion)
    return nextPion


#Définit et retourne la liste des 4 positions possibles du pion s'il se dirige à gauche, à droite, en haut ou en bas
def nextPositions(p_pion):
    
    return [moveLeft(p_pion),moveRight(p_pion),moveUp(p_pion),moveDown(p_pion)]


def move(p_pion):
    
    plateau[p_pion[0]][p_pion[1]][1] = 0
    p_pion = moveLeft(p_pion)
    plateau[p_pion[0]][p_pion[1]][1] = 1
    return p_pion


def isWin(p_pion):
    
    global cible, plateau
    return (cible[0]==p_pion[0] and cible[1]==p_pion[1] and cible[2]==plateau[p_pion[0]][p_pion[1]][1])


#******************************************************************************************************


#Initialisation des coordonnées des 4 pions et de la cible
#les 4 pions et la cible possèdent des coordonnées initiales différentes 
condition = True
while condition == True:
    bleu = init_pion()
    jaune = init_pion()
    vert = init_pion()
    rouge = init_pion()
    cible = init_pion()
    if(not(bleu == jaune == vert == rouge == cible)):
        condition = False

#Ajout d'un troisième élément à la liste correspondant à la cible
#identifie la couleur du pion devant atteindre la cible
cible.append(random.randint(1,4))
        
plateau = init_plateau()
        
print(bleu)
print(vert)
print(jaune)
print(rouge)
print(cible)
    
display_plateau()
update_plateau()
print("\n")
display_plateau()


#choix quelle direction
#compte nombre de coups / déplacement = nombre appel fonction
#algo recherche
#interface graphique


