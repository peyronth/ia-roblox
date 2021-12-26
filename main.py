############################################################################################
####                                PROJET IA 41 ROBOT
###                             Samuel Bernard - Thomas Peyron
############################################################################################


from tkinter import *
from tkinter import messagebox
import random
import time

SIZE = 500/19

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

selected = []

#Declaration de la cible
#Liste comprenant deux coordonées de position et un chiffre déterminant la couleur du pion devant atteindre la cible
cible = []

#Declaration de la fenetre contenant les boutons permettant de jouer et la représentation graphique du plateau
#De type Fenetre
fenetre = None

#Declaration des 4 boutons permettant de choisir la direction du mouvement du pion
#De type Button 
up_button = None
down_button = None
right_button = None
left_button = None

#Declaration des 4 boutons permettant de choisir le pion à déplacer
#De type Button 
bleu_button = None
vert_button = None
jaune_button = None
rouge_button = None

#Declaration du canvas de type Canvas, des 4 ronds représentant les pions et le carré représentant la cible créés dans le canvas
canvas = None
bleu_oval = None
vert_oval = None
jaune_oval = None
rouge_oval = None
cible_carre = None

#Declaration de la variable incrémentée à chaque déplacement d'un pion et du label mis à jour en conséquences
nombre_coups = 0
coups_label = None

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


def isWin(plateau):
    global cible
    if(cible[2]==plateau[cible[0]][cible[1]][1]):
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

#détermine si une etape est équivalent à un autre
def is_equiv(elem1,elem2,idx_cible):
    if(elem1[0]==elem2[0] and elem1[1]==elem2[1] and elem1[2]==elem2[2] and elem1[3]==elem2[3]):
        return True
    else:
        verif=1
        i=0
        while(verif!=0 and i<4):
            if(not elem1.count(elem1[i])==elem2.count(elem1[i])):
                return False
            else:
                i+=1
        return True
        



#Retroune si l'état n'est pas dans une liste
def notIn(element,list):

    ##Pour chaque element
    for list_elem in list:
        if(is_equiv(list_elem,element,cible[2])):
            return 0
    return 1
        


#processus de résolution de l'ia
def iaSolution(plateau,bleu,jaune,vert,rouge):

    closed=[]
    open=[]
    open.append(construct_state(bleu,jaune,vert,rouge,None))
    compteur=0
    while (open.count!=0 and compteur<1000):
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
                if(notIn(child,open)==1 and notIn(child,closed)==1):                         ##penser à ajouter qu'il n'existe pas avec un coût inférieur
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
    while (open.count!=0 and compteur<6000):
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
#Developpement de l'interface graphique du jeu

#Renvoie une chaine de caractère correspondant à la couleur de la cible (3e élément de sa liste)
def cibleColorToString():
    if(cible[2]==1):
        s = "Bleu"
    elif(cible[2]==2):
        s = "Jaune"
    elif(cible[2]==3):
        s = "Vert"
    elif(cible[2]==4):
        s = "Rouge"
    return s

#Désactivation des quatres boutons du choix de la couleur du pion à bouger
def disabledColorButtons():
    bleu_button['state'] = DISABLED
    vert_button['state'] = DISABLED
    jaune_button['state'] = DISABLED
    rouge_button['state'] = DISABLED

#Activation des quatres boutons du choix de la couleur du pion à bouger
def enabledColorButtons():
    bleu_button['state'] = NORMAL
    vert_button['state'] = NORMAL
    jaune_button['state'] = NORMAL
    rouge_button['state'] = NORMAL

#Désactivation des quatres boutons du choix de la direction du pion sélectionné
def disabledDirectionButtons():
    up_button['state'] = DISABLED
    left_button['state'] = DISABLED
    right_button['state'] = DISABLED
    down_button['state'] = DISABLED

#Activation des quatres boutons du choix de la direction du pion si celui ci peut se déplacer dans la direction 
#C'est à dire que la position du pion après s'être déplacée est différente que s'il ne s'était pas déplacé
#pion - paramètre correspondant à la copie du pion qu'on souhaite déplacé
#plateau - paramètre correpondant à la variable global plateau représentant l'état du jeu
def enabledDirectionButtons(pion,plateau):
    if(moveLeft(pion,plateau)!=pion):
        left_button['state'] = NORMAL
    if(moveRight(pion,plateau)!=pion):
        right_button['state'] = NORMAL
    if(moveDown(pion,plateau)!=pion):
        down_button['state'] = NORMAL
    if(moveUp(pion,plateau)!=pion):
        up_button['state'] = NORMAL

#Actions réalisées lors de la pression sur un bouton de choix de couleur
#pion - paramètre correspondant à la copie du pion qu'on souhaite déplacé
def selectPion(pion):
    #La variable global selected prend comme valeur celle du pion sélectionné
    #Cette variable permet de transmettre la valeur du pion qui va se déplacer aux fonctions de mouvemet définies ensuite 
    global selected
    selected = pion
    disabledColorButtons()
    enabledDirectionButtons(selected,plateau)

#Actions réalisées lors de la pression du bouton up_button :
#Déplacer le pion séléctionné vers le haut et mettre à jour le plateau et l'affichage
#pion - paramètre correspondant 
def moveToUp():
    #Définition des variables globales dont les valeurs vont être modifiées
    global plateau, selected, fenetre, bleu, jaune, vert, rouge, canvas, nombre_coups

    #Disjonction de cas suivant la couleur du pion
    #c'est à dire que le pion selected correspond à l'un des quatre pion
    #Dans chaque cas, déplacement du pion correspondant vers le haut 
    if(selected==bleu):
        bleu = moveUp(bleu,plateau)
    elif(selected==jaune):
        jaune = moveUp(jaune,plateau)
    elif(selected==vert):
        vert = moveUp(vert,plateau)
    elif(selected==rouge):
        rouge = moveUp(rouge,plateau)

    #Suppression des représentations graphiques des 4 pions du canvas 
    canvas.delete(fenetre,bleu_oval)
    canvas.delete(fenetre,vert_oval)
    canvas.delete(fenetre,jaune_oval)
    canvas.delete(fenetre,rouge_oval)

    #Un mouvement donc un coup en plus de réalisé
    nombre_coups = nombre_coups + 1

    #Mise à jour de la variable plateau avec les nouvelles position
    #Puis mise à jour de l'interface graphique
    update_plateau(bleu,jaune,vert,rouge,plateau)
    displayGame()

    #Désactivation des boutons de déplacement et activation de ceux de couleur
    disabledDirectionButtons()
    enabledColorButtons()

    #Si le pion correspondant a atteint la cible,
    #alors ouverture d'une fenêtre d'information et désactivation de tous les boutons car partie terminée
    if(isWin(plateau)==1):
        messagebox.showinfo("Succès", "Vous avez atteint la cible en " + str(nombre_coups) + " coups !")
        disabledColorButtons()
        disabledDirectionButtons()

#Actions réalisées lors de la pression du bouton left_button :
#Déplacer le pion séléctionné vers la gauche et mettre à jour le plateau et l'affichage
def moveToLeft():
    
    global selected, plateau, fenetre, bleu, jaune, vert, rouge, canvas, nombre_coups

    if(selected==bleu):
        bleu = moveLeft(bleu,plateau)
    elif(selected==jaune):
        jaune = moveLeft(jaune,plateau)
    elif(selected==vert):
        vert = moveLeft(vert,plateau)
    elif(selected==rouge):
        rouge = moveLeft(rouge,plateau)

    canvas.delete(fenetre,bleu_oval)
    canvas.delete(fenetre,vert_oval)
    canvas.delete(fenetre,jaune_oval)
    canvas.delete(fenetre,rouge_oval)

    nombre_coups = nombre_coups + 1

    update_plateau(bleu,jaune,vert,rouge,plateau)
    displayGame()

    disabledDirectionButtons()
    enabledColorButtons()

    if(isWin(plateau)==1):
        messagebox.showinfo("Succès", "Vous avez atteint la cible en " + str(nombre_coups) + " coups !")
        disabledColorButtons()
        disabledDirectionButtons()


#Actions réalisées lors de la pression du bouton right_button :
#Déplacer le pion séléctionné vers la droite et mettre à jour le plateau et l'affichage
def moveToRight():
    
    global selected, plateau, fenetre, bleu, jaune, vert, rouge, nombre_coups

    if(selected==bleu):
        bleu = moveRight(bleu,plateau)
    elif(selected==jaune):
        jaune = moveRight(jaune,plateau)
    elif(selected==vert):
        vert = moveRight(vert,plateau)
    elif(selected==rouge):
        rouge = moveRight(rouge,plateau)

    canvas.delete(fenetre,bleu_oval)
    canvas.delete(fenetre,vert_oval)
    canvas.delete(fenetre,jaune_oval)
    canvas.delete(fenetre,rouge_oval)

    nombre_coups = nombre_coups + 1

    update_plateau(bleu,jaune,vert,rouge,plateau)
    displayGame()

    disabledDirectionButtons()
    enabledColorButtons()

    if(isWin(plateau)==1):
        messagebox.showinfo("Succès", "Vous avez atteint la cible en " + str(nombre_coups) + " coups !")
        disabledColorButtons()
        disabledDirectionButtons()

#Actions réalisées lors de la pression du bouton down_button :
#Déplacer le pion séléctionné vers le bas et mettre à jour le plateau et l'affichage
def moveToDown():
    
    global selected, plateau, fenetre, bleu, jaune, vert, rouge, canvas, nombre_coups

    if(selected==bleu):
        bleu = moveDown(bleu,plateau)
    elif(selected==jaune):
        jaune = moveDown(jaune,plateau)
    elif(selected==vert):
        vert = moveDown(vert,plateau)
    elif(selected==rouge):
        rouge = moveDown(rouge,plateau)

    canvas.delete(fenetre,bleu_oval)
    canvas.delete(fenetre,vert_oval)
    canvas.delete(fenetre,jaune_oval)
    canvas.delete(fenetre,rouge_oval)

    nombre_coups = nombre_coups + 1

    update_plateau(bleu,jaune,vert,rouge,plateau)
    displayGame()

    disabledDirectionButtons()
    enabledColorButtons()

    if(isWin(plateau)==1):
        messagebox.showinfo("Succès", "Vous avez atteint la cible en " + str(nombre_coups) + " coups !")
        disabledColorButtons()
        disabledDirectionButtons()

#Définition de la position sur le canvas en fonction de la coordonnée sur le plateau d'un élement
#coord - paramètre 
def interfacePos(coord):
    return coord*500/16+2

#Définition de l'affichage graphique du plateau de jeu dont nottament le canvas
def displayGame():
    #Définition des variables globales dont les valeurs vont être modifiées
    global plateau, bleu_oval, vert_oval, jaune_oval, rouge_oval, cible_carre, coups_label

    #Suppression de tous les éléments présents dans le canvas 
    canvas.delete(all)

    #Création d'un rectangle orange correspondant à la cible
    cible_carre = canvas.create_rectangle(interfacePos(cible[1]),interfacePos(cible[0]),interfacePos(cible[1])+SIZE,interfacePos(cible[0])+SIZE, fill = 'orange',  outline = 'orange')
    
    #Pour chaque case du plateau
    for y in range(16):
        for x in range(16):
            #Type de case
            if(plateau[y][x][1]==5):
                #Création de rectangles noir correspondant au centre non accessible
                canvas.create_rectangle(interfacePos(x),interfacePos(y),interfacePos(x)+SIZE,interfacePos(y)+SIZE, fill = 'black',  outline = 'black')

            elif(plateau[y][x][1]==1):
                #Création d'un cercle bleu correspondant au pion bleu
                bleu_oval = canvas.create_oval(interfacePos(x),interfacePos(y),interfacePos(x)+SIZE,interfacePos(y)+SIZE, fill = 'blue',  outline = 'blue')
            
            elif(plateau[y][x][1]==2):
                #Création d'un cercle jaune correspondant au pion jaune
                jaune_oval = canvas.create_oval(interfacePos(x),interfacePos(y),interfacePos(x)+SIZE,interfacePos(y)+SIZE, fill = 'yellow',  outline = 'yellow')

            elif(plateau[y][x][1]==3):
                #Création d'un cercle vert correspondant au pion vert
                vert_oval = canvas.create_oval(interfacePos(x),interfacePos(y),interfacePos(x)+SIZE,interfacePos(y)+SIZE, fill = 'green',  outline = 'green')

            elif(plateau[y][x][1]==4):
                #Création d'un cercle rouge correspondant au pion rouge
                rouge_oval = canvas.create_oval(interfacePos(x),interfacePos(y),interfacePos(x)+SIZE,interfacePos(y)+SIZE, fill = 'red',  outline = 'red')

            #Présence de murs latéraux
            #Si mur à droite ou mur sur la prochaine case à gauche
            if(plateau[y][x][2]==1 or (x+1<=15 and plateau[y][x+1][4]==1)):                                                                                               
                canvas.create_line(interfacePos(x+1)-1,interfacePos(y)-1,interfacePos(x+1)-1,interfacePos(y)-1+SIZE,width = 3.5, fill = 'black')
            
            #Présence de murs horizontaux
            #Si mur à droite en bas sur la prochaine case en haut
            if(plateau[y][x][3]==1 or (y+1<=15 and plateau[y+1][x][5]==1)):
                canvas.create_line(interfacePos(x)-1,interfacePos(y+1)-1,interfacePos(x)-1+SIZE,interfacePos(y+1)-1,width = 3.5, fill = 'black')

    #Placement du canvas dans la fenêtre
    canvas.place(x=5,y=5)

    #Mise à jour du label indiquant le nombre de coups réalisés
    coups_label['text'] = "Nombre de coups = " + str(nombre_coups)

#Inittialisation d'une partie 
def init_game():
    #Définition des variables globales dont les valeurs vont être modifiées
    global fenetre, canvas
    global up_button, down_button, left_button, right_button
    global bleu_button, vert_button, jaune_button, rouge_button
    global plateau, selected, nombre_coups, coups_label

    #Création d'une fenètre de taille 750 par 510 
    fenetre = Tk()
    fenetre.geometry("750x510")

    #Création d'un canvas correspondant au plateau de jeu
    canvas = Canvas(fenetre, width=500, height=500, background='light yellow')

    #Création des limites du plateau correspondant à un rectagle dont l'épaisseur du trait est épais.
    canvas.create_rectangle(4,4,500,500, width = 3.5, outline = 'black')

    #Création des lignes verticales et horizontales formant les cases du plateau
    for i in range(15):
        canvas.create_line(500/16*(i+1),0,500/16*(i+1),500)
        canvas.create_line(0,500/16*(i+1),500,500/16*(i+1))

    #Création et positionnement du cadre comprenant les différentes informations 
    info_frame = Frame(fenetre,width = 220, height = 20, borderwidth = 2, relief = GROOVE)
    info_frame.place(x=520,y=20)

    #Création et positionnement du cadre comprenant les boutons de choix du pion
    color_frame = LabelFrame(fenetre, text="Choix du pion", width = 220, height = 180)
    color_frame.place(x=520,y=80)

    #Création et positionnement du cadre comprenant les boutons de choix de la direction
    direction_frame = LabelFrame(fenetre, text="Choix de la direction", width = 220, height = 230)
    direction_frame.place(x=520,y=270)

    #Création des deux labels du cadre info_frame
    #Le premier indiquant la couleur du pion devant accéder à la cible
    #Le second indiquant le nombre de coups réalisés
    Label(info_frame,text = "Le pion " + cibleColorToString() + " doit aller à la cible.").pack(padx=2.5, pady=2.5)
    coups_label  = Label(info_frame, text = "Nombre de coups = " + str(nombre_coups))
    coups_label.pack(padx=2.5, pady=2.5)

    #Création des 4 boutons de choix du pion
    #Chaque bouton appelle la fonction selectPion avec en paramètre le pion de la couleur correspondante 
    bleu_button = Button(color_frame, text ='Bleu', width = 10, height = 3, command = lambda :selectPion(bleu))
    vert_button = Button(color_frame, text ='Vert', width = 10, height = 3, command = lambda :selectPion(vert))
    jaune_button = Button(color_frame, text ='Jaune', width = 10, height = 3, command = lambda :selectPion(jaune))
    rouge_button = Button(color_frame, text ='Rouge', width = 10, height = 3, command = lambda :selectPion(rouge))

    #Création des 4 boutons du choix de la direction
    #Chaque fonction appelle la fonction de déplacement correspondant
    up_button = Button(direction_frame, text ='Haut', width = 10, height = 3, state = DISABLED, command = lambda :moveToUp())
    left_button = Button(direction_frame, text ='Gauche', width = 10, height = 3, state = DISABLED, command = lambda :moveToLeft())
    right_button = Button(direction_frame, text ='Droit', width = 10, height = 3, state = DISABLED, command = lambda :moveToRight())
    down_button = Button(direction_frame, text ='Bas', width = 10, height = 3, state = DISABLED, command = lambda :moveToDown())

    #Positionnement des boutons dans leur cadre respectif
    bleu_button.place(x=15, y=20)
    vert_button.place(x=115, y=20)
    jaune_button.place(x=15, y=90)
    rouge_button.place(x=115, y=90)

    up_button.place(x=60, y=15)
    left_button.place(x=20, y=75)
    right_button.place(x=100, y=75)
    down_button.place(x=60, y=135)

    #Affichage du canvas
    displayGame()
    
#******************************************************************************************************
#Initialisation des coordonnées des 4 pions
#les 4 pions et la cible possèdent des coordonnées initiales différentes 
condition = True
while condition == True:
    bleu = init_pion()
    jaune = init_pion()
    vert = init_pion()
    rouge = init_pion()
    if(bleu != jaune != vert != rouge != cible):
        condition = False

#Initialisation du plateau
plateau = init_plateau()

#Ajout d'un troisième élément à la liste correspondant à la cible
#identifie la couleur du pion devant atteindre la cible
cible.append(random.randint(1,4))

#Affichage du plateau en console
#display_plateau(plateau)

#Affichage de la couleur du pion devant atteindre la cible
if(cible[2]==1):
    print("Bleu doit aller sur la cibe")
elif(cible[2]==2):
    print("Jaune doit aller sur la cibe")
elif(cible[2]==3):
    print("Vert doit aller sur la cibe")
elif(cible[2]==4):
    print("Rouge doit aller sur la cibe")

init_game()
fenetre.mainloop()


#Creation de la solution de l'ia 
result=iaSolution(plateau,bleu,jaune,vert,rouge)
if(result!=0):
    result=solutionList(result)
    for line in result:
            print (line)
else:
    print("aucun resultat trouvé")
