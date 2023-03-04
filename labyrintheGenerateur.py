from asyncio.mixins import _global_lock
from operator import index
from tkinter import *
import random

random.seed(13)

cote=50
larg=12
haut=12
flag = 0
labyrintheCreer=False


class Cell:
    def __init__(self):
        self.cheminAccessible=[]
        self.caseDebut=False
        self.caseFin=False
        self.recompense=0
        self.value=[0,0,0,0]

class Joueur:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.epsilon=0.999999999999


matriceValeur=[[Cell() for ligne in range (haut)] for colonne in range (larg)]
matriceValeurTemp=[[Cell() for ligne in range (haut)] for colonne in range (larg)]
fondAfficher=[[0 for ligne in range (haut)] for colonne in range (larg)]
ligneAfficher=[[0 for ligne in range (haut)] for colonne in range (larg)]
#0 gauche 1 haut 2 droite 3 bas
valeurAfficher=[[[0 for coté in range (4)] for ligne in range (haut)] for colonne in range (larg)]
prochaineCase=set()
caseDejaCreer=set()
joueurPresent=[]
xDebut,yDebut= None,None
xFin,yFin= None,None


def tableau():

    global flag

    jouerJoueur()
    if flag==1:
        fenetre.after(100, tableau)
    else:
        flag=0


def initLaby():
    global joueurPresent
    global matriceValeur
    global matriceValeurTemp
    global prochaineCase
    global caseDejaCreer
    global labyrintheCreer
    global fondAfficher
    global valeurAfficher
    global xDebut,xFin,yDebut,yFin

    matriceValeur=[[Cell() for ligne in range (haut)] for colonne in range (larg)]
    matriceValeurTemp=[[Cell() for ligne in range (haut)] for colonne in range (larg)]
    fondAfficher=[[0 for ligne in range (haut)] for colonne in range (larg)]
    valeurAfficher=[[[0 for coté in range (4)] for ligne in range (haut)] for colonne in range (larg)]
    joueurPresent=[]
    prochaineCase=set()
    caseDejaCreer=set()
    
    xDebut=random.randrange(larg)
    yDebut=random.randrange(haut)
    xFin=random.randrange(larg)
    yFin=random.randrange(haut)
    

    caseDejaCreer.add((xDebut,yDebut))
    for x in range(larg):

        for y in range(haut):

            canvas.itemconfig(fondAfficher[xFin][yFin], fill="red")
            matriceValeur[xFin][yFin].caseFin = True
            matriceValeur[xFin][yFin].recompense = 1


            if xDebut==x and yDebut==y:
                fondAfficher[x][y] = canvas.create_rectangle((x*cote, y*cote, (x+1)*cote, (y+1)*cote), outline="", fill="green")
                matriceValeur[x][y].caseDebut=True
                joueurPresent.append(Joueur(x,y))
                prochaineCase.add((x,y))

                valeurAfficher[x][y][0]=canvas.create_text(x*cote+cote*1/4, y*cote+cote*2/4,fill="black",text=matriceValeur[x][y].value[0])
                valeurAfficher[x][y][1]=canvas.create_text(x*cote+cote*2/4, y*cote+cote*1/4,fill="black",text=matriceValeur[x][y].value[1])
                valeurAfficher[x][y][2]=canvas.create_text(x*cote+cote*3/4, y*cote+cote*2/4,fill="black",text=matriceValeur[x][y].value[2])
                valeurAfficher[x][y][3]=canvas.create_text(x*cote+cote*2/4, y*cote+cote*3/4,fill="black",text=matriceValeur[x][y].value[3])
            elif xFin==x and yFin==y:
                fondAfficher[x][y] = canvas.create_rectangle((x*cote, y*cote, (x+1)*cote, (y+1)*cote), outline="", fill="grey")
            else:
                fondAfficher[x][y] = canvas.create_rectangle((x*cote, y*cote, (x+1)*cote, (y+1)*cote), outline="", fill="grey")
                valeurAfficher[x][y][0]=canvas.create_text(x*cote+cote*1/4, y*cote+cote*2/4,fill="black",text=matriceValeur[x][y].value[0])
                valeurAfficher[x][y][1]=canvas.create_text(x*cote+cote*2/4, y*cote+cote*1/4,fill="black",text=matriceValeur[x][y].value[1])
                valeurAfficher[x][y][2]=canvas.create_text(x*cote+cote*3/4, y*cote+cote*2/4,fill="black",text=matriceValeur[x][y].value[2])
                valeurAfficher[x][y][3]=canvas.create_text(x*cote+cote*2/4, y*cote+cote*3/4,fill="black",text=matriceValeur[x][y].value[3])



            
            """
            ligneAfficher[x][y] = canvas.create_line((x*cote, y*cote, x*cote, (y+1)*cote))
            ligneAfficher[x][y] = canvas.create_line((x*cote, y*cote, (x+1)*cote, y*cote))
            """
            

def creerLabyrinthe():

    global prochaineCase
    global caseDejaCreer
    global matriceValeur


    caseActuel= prochaineCase.pop()
    x,y=caseActuel

    caseDejaCreer.add((x,y))

    

    AdjacentCell=[]
    #Different conclusion on the type of cell
    
    if 0<x<larg-1 and 0<y<haut-1:
        AdjacentCell.extend(((x,y-1),(x-1,y),(x+1,y),(x,y+1)))

        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord) 
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)


    #Border cell
    elif x==0 and 0<y<haut-1:
        
        AdjacentCell.extend(((x,y-1),(x+1,y),(x,y+1)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)


    elif x==larg-1 and 0<y<haut-1:
        AdjacentCell.extend(((x,y-1),(x-1,y),(x,y+1)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)

    elif 0<x<larg-1 and y==haut-1:
        AdjacentCell.extend(((x,y-1),(x-1,y),(x+1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)

    elif 0<x<larg-1 and y==0:
        AdjacentCell.extend(((x,y+1),(x-1,y),(x+1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)

    #Corner cell
    elif x==0 and y==0:
        AdjacentCell.extend(((x,y+1),(x+1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)
                
    elif x==larg-1 and y==0:
        AdjacentCell.extend(((x,y+1),(x-1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)

    elif x==0 and y==haut-1:
        AdjacentCell.extend(((x,y-1),(x+1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:

            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)

    elif x==larg-1 and y==haut-1:
        AdjacentCell.extend(((x,y-1),(x-1,y)))
        #Find new cell to explore
        for coord in AdjacentCell:
            
            if coord not in caseDejaCreer:
                prochaineCase.add(coord)
            else:
                matriceValeur[x][y].cheminAccessible.append(coord)
                matriceValeur[coord[0]][coord[1]].cheminAccessible.append(caseActuel)





    if len(matriceValeur[x][y].cheminAccessible) >=2:
        
        random.shuffle(matriceValeur[x][y].cheminAccessible)

        xSuppr,ySuppr=matriceValeur[x][y].cheminAccessible.pop()


        if x < xSuppr:
            ligneAfficher[x][y] = canvas.create_line(((x+1)*cote, y*cote, (x+1)*cote, (y+1)*cote))
            matriceValeur[xSuppr][ySuppr].cheminAccessible.remove(caseActuel)

        elif x> xSuppr:
            ligneAfficher[x][y] = canvas.create_line((x*cote, y*cote, x*cote, (y+1)*cote))
            matriceValeur[xSuppr][ySuppr].cheminAccessible.remove(caseActuel)

        elif y> ySuppr:
            ligneAfficher[x][y] = canvas.create_line((x*cote, y*cote, (x+1)*cote, y*cote))
            matriceValeur[xSuppr][ySuppr].cheminAccessible.remove(caseActuel)

        elif y< ySuppr:
            ligneAfficher[x][y] = canvas.create_line((x*cote, (y+1)*cote, (x+1)*cote, (y+1)*cote))
            matriceValeur[xSuppr][ySuppr].cheminAccessible.remove(caseActuel)



def jouerJoueur():
    global joueurPresent
    global matriceValeur
    global fondAfficher
    global valeurAfficher
    global xDebut,xFin,yDebut,yFin
    #Pour chaque joueur présent jouer
    for joueur in joueurPresent:
        x=joueur.x
        y=joueur.y
        destination=None
        if random.uniform(0, 1) < joueur.epsilon:
            newX,newY=random.choice(matriceValeur[x][y].cheminAccessible)
            joueur.epsilon*=0.99999

        else:
            indexMax=[-100,None,None]
            for coord in matriceValeur[x][y].cheminAccessible:
                newXtemp,newYtemp=coord
                if x> newXtemp:
                    direction=0
                elif y< newYtemp:
                    direction=3
                elif x < newXtemp:
                    direction=2
                elif y> newYtemp:
                    direction=1
                if matriceValeur[x][y].value[direction] > indexMax[0]:
                    indexMax[0]=matriceValeur[x][y].value[direction]
                    indexMax[1]=newXtemp
                    indexMax[2]=newYtemp
            newX=indexMax[1]
            newY=indexMax[2]

        if x> newX:
            direction=0
        elif y< newY:
            direction=3
        elif x < newX:
            direction=2
        elif y> newY:
            direction=1

        matriceValeur[x][y].value[direction]=valueFunction(x,y,newX,newY,direction)
        canvas.itemconfig(valeurAfficher[x][y][direction], text=round(matriceValeur[x][y].value[direction],2))
            
        joueur.x=newX
        joueur.y=newY

        if matriceValeur[x][y].caseDebut == True:
            canvas.itemconfig(fondAfficher[x][y], fill="green")

        elif matriceValeur[newX][newY].caseFin == True:
            canvas.itemconfig(fondAfficher[x][y], fill="grey")
            joueur.x=xDebut
            joueur.y=yDebut
        else:
            canvas.itemconfig(fondAfficher[x][y], fill="grey")
        
        canvas.itemconfig(fondAfficher[joueur.x][joueur.y], fill="black")

        

        


        


def valueFunction(x,y,newX,newY,direction):
    global matriceValeur
    lr=0.1
    gamma=0.7
    maxValueNextCell=max(matriceValeur[newX][newY].value)
    return(matriceValeur[x][y].value[direction]+lr*(matriceValeur[newX][newY].recompense+gamma*maxValueNextCell-matriceValeur[x][y].value[direction])-0.001)



# arret de l'animation"
def stop():
    global flag
    flag=0

#démarrage de l'animation"
def start():
    global flag
    if flag==0:
        flag=1
    
    tableau()


#animation pas à pas
def pasapas():
    global flag
    flag=2
    tableau()

def creerLaby():
    global flag
    global labyrintheCreer
    global haut
    global larg
    if labyrintheCreer:
        initLaby()
        labyrintheCreer=False
        creerLaby()

    else:
        labyrintheCreer=True
        for i in range(larg*haut-1):

            fenetre.after(1, creerLabyrinthe)




def avancerIteration():
    global flag
    flag =2
    for i in range (200000):
        jouerJoueur()
    global joueurPresent
    print(joueurPresent[0].epsilon)
    tableau()

fenetre = Tk()
fenetre.title("Simulation ecosysteme")
canvas = Canvas(fenetre, width=cote*larg, height=cote*haut, highlightthickness=0)
canvas.pack()
bou1 = Button(fenetre,text='Creer Labyrinthe', width=8, command=creerLaby)
bou1.pack(side=RIGHT)
bou1 = Button(fenetre,text='Quitter', width=8, command=fenetre.destroy)
bou1.pack(side=RIGHT)
bou2 = Button(fenetre, text='Démarrer', width=8, command=start)
bou2.pack(side=LEFT)
bou3 = Button(fenetre, text='Arrêter', width=8, command=stop)
bou3.pack(side=LEFT)
bou3 = Button(fenetre, text='10000 itération', width=8, command=avancerIteration)
bou3.pack(side=LEFT)
bou4 = Button(fenetre, text='Pas à  pas', width=8, command=pasapas)
bou4.pack(side=LEFT)

initLaby()



fenetre.mainloop()
