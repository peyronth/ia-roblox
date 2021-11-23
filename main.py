############################################################################################
####                                PROJET IA 41 ROBOT
###                             Samuel Bernard - Thomas Peyron
############################################################################################

import random

#Plateau contient les cases du plateau.
#Les cases sont un tableau de type [id case, couleur case, mur droit, mur bas, mur gauche, mur haut]
#Avec couleur case 0=>Aucune 1=>Bleu 2=>JAune 3=>Vert 4=>Rouge 5=>Blocked
plateau = []



def display_plateau(plateau):
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

def init_plateau():
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

    return plateau





plateau=init_plateau()
display_plateau(plateau)


