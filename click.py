from fltk import *
import glob
import re
import math
view = ""
elements = []
clickables = {}
segmentsRef = {}
gameTexts = {}
def createButton(x = 0, y = 0, width=150, height=50, content="", fontSize = 12):
    global elements
    a = rectangle(x, y, x + width, y + height)
    
    textX = int((x + x + width ) / 2)
    textY =int((y + y + height ) / 2)

    a =  texte(textX, textY,content, ancrage='center', taille=fontSize)
    elements.append(a)
    return {"x": {"min": x, "max": x + width}, "y": {"min": y, "max": y + height} }


def clearScreen():
    global element
    global clickables
    global view
    for element in elements:
        efface(element)
    element = []
    clickables = {}
    ferme_fenetre()
    view = ""




def mainScreen():
    global view
    view = "main"
    cree_fenetre(400, 300)
    clickables['grille'] = createButton(400 / 2 - 150 / 2, 300 / 2 - 50 / 2, content="choose grille")
    mise_a_jour()

def handleClick(coords):
    global clickables
    x, y = coords
    event = None
    for name, xy in clickables.items():
        if (xy['x']['min']) < x and (x < xy['x']['max']) and (xy['y']['min'] < y) and (y < xy['y']['max']):
            print("clicked " + name)
            event = name

    if (view == "main" and event == "grille"):
        clearScreen()
        grilleScreen()
    elif (view == "grilleSelection"):
        clearScreen()
        StartGame(event)
        pass
height = 0
width = 0
indices = []
etat = {}
def lireJeu(filename = ""):
    global indices, height, width
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
    print(lines)
    
    if len(list(set([len(line) for line in lines]))) != 1:
        raise BaseException("lines length are not consistent")

    
    if False in [True if re.match(r'^([0123_])+$', line) else False  for line in lines]:
        raise BaseException("Invalid Characters detected")

    indices = [[int(letter) if letter.isdigit() else None for letter in list(line)] for line in lines]
    height = len(lines)
    width = len(lines[0])
    
    pass

def createBox():
    pass
def verifyTuplesOrder(segment):
    tup1 = segment[0]
    tup2 = segment[1]

    if tup1[0] > tup2[0]:
        return (tup2, tup1)

    if tup1[0] == tup2[0] and tup1[1] > tup2[1]:
        return (tup2, tup1)

    return segment

def handleGameClick(mouse, coords):
    global etat
    global indices
    squareSide = 20
    distanceBetweenSquares = 60
    padding = 40
    x, y = coords
    print("for :" + str(coords))

    i = math.ceil((y - padding) / (squareSide + distanceBetweenSquares)) - 1
    j = math.ceil((x - padding) / (squareSide + distanceBetweenSquares)) - 1

    row = len(indices)
    column = len(indices[0])
    print(row)
    print(column)
    if i > row  or i < 0:
        return
    if j > column  or j < 0:
        return
    sommetY = i * (squareSide + distanceBetweenSquares) + padding
    sommetX = j * (squareSide + distanceBetweenSquares) + padding
    print("sommet: " + str((i, j)))
    print("sommet coords: " + str((sommetX, sommetY)))

    horizontalRectangle = {
        'x': {
            'min': sommetX + squareSide,
            'max': sommetX + squareSide + distanceBetweenSquares
        },
        'y': {
            'min': sommetY,
            'max': sommetY + squareSide
        }
    }

    verticalRectangle = {
        'x': {
            'min': sommetX,
            'max': sommetX + squareSide
        },
        'y': {
            'min': sommetY + squareSide,
            'max': sommetY + squareSide + distanceBetweenSquares
        }
    }

    xInHorizontalRectangle = horizontalRectangle['x']['min'] <= x and x <= horizontalRectangle['x']['max']
    yInHorizontalRectangle = horizontalRectangle['y']['min'] <= y and y <= horizontalRectangle['y']['max']


    xInVerticalRectangle = verticalRectangle['x']['min'] <= x and x <= verticalRectangle['x']['max']
    yInVerticalRectangle = verticalRectangle['y']['min'] <= y and y <= verticalRectangle['y']['max']
    

    isHorizontal = xInHorizontalRectangle and yInHorizontalRectangle
    isVertical = xInVerticalRectangle and yInVerticalRectangle
    if xInHorizontalRectangle and yInHorizontalRectangle:
        segment = ((i, j), (i, j+1))
        rectangle(horizontalRectangle['x']['min'], horizontalRectangle['y']['min'] + 4, horizontalRectangle['x']['max'], horizontalRectangle['y']['max'] - 4, remplissage="black")
        print(segment)
    if xInVerticalRectangle and yInVerticalRectangle:
        segment = ((i, j), (i + 1, j))
        verdict = etat.get(segment, False)
        print(verdict)
        if verdict == False:
            
            if mouse == "ClicGauche":
                etat[segment] = 1
                segmentsRef[segment] =  rectangle(verticalRectangle['x']['min'] + 4, verticalRectangle['y']['min'], verticalRectangle['x']['max'] - 4, verticalRectangle['y']['max'], remplissage="black")
            elif mouse == "ClicDroit":
                etat[segment] = -1
                centerX = (verticalRectangle['x']['min'] + verticalRectangle['x']['max']) / 2
                centerY = (verticalRectangle['y']['min'] + verticalRectangle['y']['max']) / 2
                segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")

        elif verdict == 1:
            if mouse == "ClicGauche":
                efface(segmentsRef[segment])
                segmentsRef.pop(segment, None)
                etat.pop(segment, None)
                etat[segment] = -1
                centerX = (verticalRectangle['x']['min'] + verticalRectangle['x']['max']) / 2
                centerY = (verticalRectangle['y']['min'] + verticalRectangle['y']['max']) / 2
                segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")

                pass
            elif mouse == "ClicDroit":
                efface(segmentsRef[segment])
                segmentsRef.pop(segment, None)
                etat.pop(segment, None)
                etat[segment] = -1
                centerX = verticalRectangle['x']['min'] + verticalRectangle['x']['max']
                centerY = verticalRectangle['y']['min'] + verticalRectangle['y']['max']
                segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")
                pass
            
            print("exist must delete")

        elif verdict == -1:
            if mouse == "ClicGauche":
                efface(segmentsRef[segment])
                etat[segment] = 1
                segmentsRef[segment] =  rectangle(verticalRectangle['x']['min'] + 4, verticalRectangle['y']['min'], verticalRectangle['x']['max'] - 4, verticalRectangle['y']['max'], remplissage="black")
                
                pass
            elif mouse == "ClicDroit":
                efface(segmentsRef[segment])
                segmentsRef.pop(segment, None)
                etat.pop(segment, None)
                pass
        print("in vertical")
        print(segment)
    
def drawGrid():
    global indices
    global gameTexts

    row = len(indices)
    column = len(indices[0])
    squareSide = 20
    distanceBetweenSquares = 60
    padding = 40
    width = row * (squareSide + distanceBetweenSquares) + padding  * 3
    height = column * (squareSide + distanceBetweenSquares) + padding  * 3
    cree_fenetre(width , height)
    for j in range(0, column + 1):
        starty = padding + j * (squareSide + distanceBetweenSquares)
        endy = padding + j * (squareSide + distanceBetweenSquares) + squareSide

        for i in range(0, row + 1):
            
            color = "black" if i % 2 == 0 else  "green"
            startx = padding + i * (squareSide + distanceBetweenSquares)
            endx = padding + i * (squareSide + distanceBetweenSquares)+ squareSide

            print({"x": {"min": startx, "max": endx}, "y": {"min": starty, "max": endy}})
            rectangle(startx, starty, endx, endy, remplissage=color)
            
            if i < row and j < column and indices[j][i] != None:
                lstartx = padding + i * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
                lstarty = padding + j * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
                gameTexts[(j, i)] = texte(lstartx, lstarty,str(indices[j][i]), ancrage='center', taille=14)
    print(gameTexts)

    #rectangle(200,100,300,150)
    #rectangle(300,400 ,300 ,400)
    mise_a_jour()
def StartGame(grille):
    global view
    view = "game"
    #cree_fenetre(800, 800)
    lireJeu('./grilles/' + grille + ".txt")
    drawGrid()
    
def grilleScreen():
    global view
    view = "grilleSelection"
    grilles = glob.glob("./grilles/*.txt")
    grilles = [grille.replace("\\", "/").replace(".txt", "").split("/")[-1] for grille in grilles]
    #grilles = [grille.replace(".txt", "") for grille in grilles]
    #grilles = [grille.split("/")[-1] for grille in grilles]
    height = 50 + len(grilles) * 75 + 25
    cree_fenetre(400, height)
    startx = 50
    starty = 50
    for grille in grilles:
        clickables[grille] = createButton(400 / 2 - 150 / 2 ,starty, content=grille)
        starty = starty + 50 + 25

HEIGHT = 300
WIDTH = 400


mainScreen()

while True:
    if getCanevas() == None:
        continue
    ev = donne_ev()
    tev = type_ev(ev)
    

    # Action dépendant du type d'événement reçu :

    if tev == 'Touche':
        print('Appui sur la touche', touche(ev))

    elif tev == "ClicDroit":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))
        if view == "game":
            handleGameClick(tev, (abscisse(ev), ordonnee(ev)))
    elif tev == "ClicGauche":
        if view in ['main', "grilleSelection"]:
            handleClick((abscisse(ev), ordonnee(ev)))
        elif view == "game":
            handleGameClick(tev, (abscisse(ev), ordonnee(ev)))
        print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))

    elif tev == 'Quitte':  # on sort de la boucle
        break

    else:  # dans les autres cas, on ne fait rien
        pass
    try:
        mise_a_jour()
    except:
        pass
    


