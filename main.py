############################################################################################
####                                PROJET IA 41 ROBOT
###                             Samuel Bernard - Thomas Peyron
############################################################################################

import random

#Plateau contient les cases du plateau.
#Les cases sont un tableau de type [id case, couleur case, mur droit, mur bas, mur gauche, mur haut]
#Avec couleur case 0=>Aucune 1=>Bleu 2=>Jaune 3=>Vert 4=>Rouge 5=>Blocked 6=>Objectif
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


#Afficher le plateau sur la console
def display_plateau(plateau):
    
    global cible
    
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
            elif(plateau[y][x][1]==6):type=" O "

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

#Initialiser le plateau au départ du jeu
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

    #On détermine la position de la cible dans un de ces angles
    idx_cible=random.randint(0, 15)
    idx=0

    #4 Angle par quart de tableau chaque angle ne doit pas toucher une autre parois
    for h_middle in range(2):
        for v_middle in range(2):
            for i in range(2):
                x=random.randint(1, 6)+6*(h_middle)
                y=random.randint(1, 6)+6*(v_middle)
                plateau[y][x][3]=1
                plateau[y][x][2]=1
                idx+=1
                if(idx==idx_cible):
                    cible=[y,x]
            for i in range(2,4):
                x=random.randint(1, 6)+6*(h_middle)
                y=random.randint(1, 6)+6*(v_middle)
                plateau[y][x][4]=1
                plateau[y][x][5]=1
                idx+=1
                if(idx==idx_cible):
                    cible=[y,x]

    plateau[cible[0]][cible[1]][1]=6

    #Type des cases dont les coordonnées sont celles des pions correspond :
    #1 : bleu
    #2 : jaune etc.
    plateau[bleu[0]][bleu[1]][1] = 1
    plateau[jaune[0]][jaune[1]][1] = 2
    plateau[vert[0]][vert[1]][1] = 3
    plateau[rouge[0]][rouge[1]][1] = 4
    
    return plateau

#Mise à jour du plateau lorsqu'un ou plusieurs pions ont été déplacés
def update_plateau(bleu, jaune, vert, rouge, plateau):
    
    #on place la cible
    plateau[cible[0]][cible[1]][1] = 6
    
    #On change la couleur de la case si le robot à bougé
    if(not plateau[bleu[0]][bleu[1]][1] == 1):
        #on enleve l'ancienne case de cette couleur
        for ligne in plateau:
            for case in ligne:
                if(case[1]==1):
                    case[1]=0
        #on met la bonne case dans la couleur
        plateau[bleu[0]][bleu[1]][1] = 1
    if(not plateau[jaune[0]][jaune[1]][1] == 2):
        #on enleve l'ancienne case de cette couleur
        for ligne in plateau:
            for case in ligne:
                if(case[1]==2):
                    case[1]=0
        #on met la bonne case dans la couleur
        plateau[jaune[0]][jaune[1]][1] = 2
    if(not plateau[vert[0]][vert[1]][1] == 3):
        #on enleve l'ancienne case de cette couleur
        for ligne in plateau:
            for case in ligne:
                if(case[1]==3):
                    case[1]=0
        #on met la bonne case dans la couleur
        plateau[vert[0]][vert[1]][1] = 3 
    if(not plateau[rouge[0]][rouge[1]][1] == 4):
        #on enleve l'ancienne case de cette couleur
        for ligne in plateau:
            for case in ligne:
                if(case[1]==4):
                    case[1]=0
        #on met la bonne case dans la couleur
        plateau[rouge[0]][rouge[1]][1] = 4              

    return plateau
    
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
def isEmpty(p_case,plateau):
    return(plateau[p_case[0]][p_case[1]][1] == 0 or plateau[p_case[0]][p_case[1]][1] == 6)


def moveLeft(p_pion,plateau):
    
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][4] != 1 and plateau[nextPion[0]][nextPion[1]-1][2] != 1 and isEmpty([nextPion[0],nextPion[1]-1],plateau):
        nextPion[1]-=1
    
    return nextPion
  

def moveRight(p_pion,plateau):
    
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][2] != 1 and plateau[nextPion[0]][nextPion[1]+1][4] != 1 and isEmpty([nextPion[0],nextPion[1]+1],plateau):
        nextPion[1]+=1
    
    return nextPion


def moveUp(p_pion,plateau):
    
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][5] != 1 and plateau[nextPion[0]-1][nextPion[1]][3] != 1 and isEmpty([nextPion[0]-1,nextPion[1]],plateau):
        nextPion[0]-=1
    
    return nextPion


def moveDown(p_pion,plateau):
    
    nextPion = [p_pion[0],p_pion[1]]
    
    while plateau[nextPion[0]][nextPion[1]][3] != 1 and plateau[nextPion[0]+1][nextPion[1]][5] != 1 and isEmpty([nextPion[0]+1,nextPion[1]],plateau):
        nextPion[0]+=1
    return nextPion


#Définit et retourne la liste des 4 positions possibles du pion s'il se dirige à gauche, à droite, en haut ou en bas
def nextPositions(p_pion,plateau):
    a_p_next=[]
    if(moveLeft(p_pion,plateau)!=p_pion):
        a_p_next.append(moveLeft(p_pion,plateau))
    if(moveRight(p_pion,plateau)!=p_pion):
        a_p_next.append(moveRight(p_pion,plateau))
    if(moveDown(p_pion,plateau)!=p_pion):
        a_p_next.append(moveDown(p_pion,plateau))
    if(moveUp(p_pion,plateau)!=p_pion):
        a_p_next.append(moveUp(p_pion,plateau))
    return a_p_next



def move(p_pion):

    plateau[p_pion[0]][p_pion[1]][1] = 0
    p_pion = moveLeft(p_pion)
    plateau[p_pion[0]][p_pion[1]][1] = 1
    return p_pion


def isWin(plateau):
    global cible
    if(cible[2]==plateau[cible[0]][cible[1]][1]):
        #display_plateau(plateau)
        #print(plateau[cible[0]][cible[1]][1])
        #print(cible)
        return 1
    else:
        return 0


#******************************************************************************************************
#Construit un état fictif du jeu
def construct_state(bleu,jaune,vert,rouge,idx_parent=0,heur=0):

    return [bleu,jaune,vert,rouge,idx_parent,heur]

#Insérer un élément dans la liste selon son heuristique
def insertList(list, child):
    n=0
    inserted=0
    while (n<len(list) and inserted==0):
        if(list[n][5]<child[5]):
            list.insert(n,child)
            inserted=1
        n+=1
    if(inserted==0):
        list.append(child)
    return list
        


#processus de résolution de l'ia
def iaSolution(plateau,bleu,jaune,vert,rouge):
    
    closed=[]
    open=[]
    open.append(construct_state(bleu,jaune,vert,rouge,None))
    compteur=0
    while (open.count!=0 and compteur<3000):
        u=open[0]
        #print("je recommence avec ",u)
        del open[0]
        if (isWin(plateau)):
            print("Jeu terminé avec succès")
            return closed
        else:
            #On génère les états qui peuvent être générés par u
            children=[]

            bleu=u[0]
            jaune=u[1]
            vert=u[2]
            rouge=u[3] 
            #poids=u[4]+1
            plateau=update_plateau(bleu, jaune, vert, rouge, plateau)
            #display_plateau(plateau)

            for states in nextPositions(bleu,plateau):
                children.append(construct_state(states,jaune,vert,rouge,len(closed)))
            for states in nextPositions(jaune,plateau):
                children.append(construct_state(bleu,states,vert,rouge,len(closed)))
            for states in nextPositions(vert,plateau):
                children.append(construct_state(bleu,jaune,states,rouge,len(closed)))
            for states in nextPositions(rouge,plateau):
                children.append(construct_state(bleu,jaune,vert,states,len(closed)))
            #Pour chaque child possible on vérifie s'il est dans les listes
            for child in children:
                if(closed.count(child)==0 and (open.count(child)==0)):                         ##penser à ajouter qu'il n'existe pas avec un coût inférieur
                    open=insertList(open, child)
                    #print("j'ajoute ",child)
            closed.append(u)
            compteur+=1
    return 0


def iaSolution_largeurFirst(plateau,bleu,jaune,vert,rouge):
    
    closed=[]
    open=[]
    open.append(construct_state(bleu,jaune,vert,rouge,None))
    compteur=0
    while (open.count!=0 and compteur<3000):
        u=open[0]
        #print("je recommence avec ",u)
        del open[0]
        if (isWin(plateau)):
            print("Jeu terminé avec succès")
            return closed
        else:
            #On génère les états qui peuvent être générés par u
            children=[]

            bleu=u[0]
            jaune=u[1]
            vert=u[2]
            rouge=u[3] 
            #poids=u[4]+1
            plateau=update_plateau(bleu, jaune, vert, rouge, plateau)
            #display_plateau(plateau)

            for states in nextPositions(bleu,plateau):
                children.append(construct_state(states,jaune,vert,rouge,len(closed)))
            for states in nextPositions(jaune,plateau):
                children.append(construct_state(bleu,states,vert,rouge,len(closed)))
            for states in nextPositions(vert,plateau):
                children.append(construct_state(bleu,jaune,states,rouge,len(closed)))
            for states in nextPositions(rouge,plateau):
                children.append(construct_state(bleu,jaune,vert,states,len(closed)))
            #Pour chaque child possible on vérifie s'il est dans les listes
            for child in children:
                if(closed.count(child)==0 and (open.count(child)==0)):                         ##penser à ajouter qu'il n'existe pas avec un coût inférieur
                    open.append(child)
                    #print("j'ajoute ",child)
            closed.append(u)
            compteur+=1
    return 0

def solutionList(t_closed):
    a_result=[t_closed[len(t_closed)-1]]
    while(a_result[len(a_result)-1][4]!=None):
        idx_nest_elem=a_result[len(a_result)-1][4]
        a_result.append(t_closed[idx_nest_elem])
    return a_result




#******************************************************************************************************

#Initialisation des coordonnées des 4 pions et de la cible
#les 4 pions et la cible possèdent des coordonnées initiales différentes 
condition = True
while condition == True:
    bleu = init_pion()
    jaune = init_pion()
    vert = init_pion()
    rouge = init_pion()
    #cible = init_pion()
    if(bleu != jaune != vert != rouge != cible):
        condition = False

#Ajout d'un troisième élément à la liste correspondant à la cible
#identifie la couleur du pion devant atteindre la cible

#Initialisation du plateau
plateau = init_plateau()
#choix de la couleur qui doit aller sur la cible
cible.append(random.randint(1,4)) 
#Affichage du plateau
display_plateau(plateau)

if(cible[2]==1):
    print("Bleu doit aller sur la cibe")
elif(cible[2]==2):
    print("Jaune doit aller sur la cibe")
elif(cible[2]==3):
    print("Vert doit aller sur la cibe")
elif(cible[2]==4):
    print("Rouge doit aller sur la cibe")

#Creation de la solution de l'ia 
result=iaSolution(plateau,bleu,jaune,vert,rouge)
if(result!=0):
    result=solutionList(result)
    for line in result:
            print (line)
else:
    print("aucun resultat trouvé")

#choix quelle direction
#compte nombre de coups / déplacement = nombre appel fonction
#algo recherche
#interface graphique


