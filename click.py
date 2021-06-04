from fltk import *
import glob
import re
import math
view = ""
elements = []
clickables = {}
segmentsRef = {}
gameTexts = {}
gGrille = None
squareSide = 20
distanceBetweenSquares = 60
padding = 40
height = 0
width = 0
indices = []
etat = {}

won = False
def createButton(x = 0, y = 0, width=150, height=50, content="", fontSize = 12):
    global elements
    rectxc = rectangle(x, y, x + width, y + height)
    
    textX = int((x + x + width ) / 2)
    textY =int((y + y + height ) / 2)

    a =  texte(textX, textY,content, ancrage='center', taille=fontSize)
    elements.append(a)
    return {"x": {"min": x, "max": x + width}, "y": {"min": y, "max": y + height}, 'rect': rectxc, 'txt': a }


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
        if event != None:
            global gGrille
            gGrille = event
            clearScreen()
            StartGame(event)
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



def statut_case(indices, etat, case):
    maxRow = len(indices)
    maxColumn = len(indices[0])


    i, j = case

    if i > maxRow - 1:
        return
    if j > maxColumn - 1:
        return
    indice = indices[i][j]
    if indice == None:
        return None
    pts = [
        (i,j),
        (i, j + 1),
        (i + 1, j + 1),
        (i + 1 , j)
    ]
    segments = [
        (pts[0], pts[1]),
        (pts[1], pts[2]),
        (pts[2], pts[3]),
        (pts[3], pts[0])
    ]
    segments = [verifyTuplesOrder(segment) for segment in segments]
    
    nber_trace = 0
    nber_veirge = 0
    nber_interdit = 0
    for segment in segments:
        nber_trace = nber_trace + int(est_trace(etat, segment))
        nber_veirge = nber_veirge + int(est_vierge(etat, segment))
        nber_interdit = nber_interdit + int(est_interdit(etat, segment))
    pass

    if nber_trace== indice:
        return 0

    if (nber_trace < indice) and (nber_trace + nber_interdit < 4) and (nber_veirge > 0):
        return 1

    if (nber_trace > indice) or (nber_veirge < indice - nber_trace):
        return -1


def est_trace(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == 1:
        return True
    return False

def est_interdit(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == -1:
        return True
    return False


def est_vierge(etat, segment):
    segment = verifyTuplesOrder(segment)
    if etat.get(segment, None) == None:
        return True
    return False

def doSolveFunction():
    print("pressed solve button")

def getSommetSegments(sommet):
        i, j = sommet
        global indices

        maxRow = len(indices)
        maxColumn = len(indices[0])

        candidates = [
            ((i, j), (i, j + 1)),
            ((i, j), (i + 1, j)),
            ((i,j), (i, j - 1)),
            ((i,j), (i - 1, j))
        ]
        if i == 0:
            candidates.remove(((i,j), (i - 1, j)))
        if i == maxRow:
            candidates.remove(((i, j), (i + 1, j)))
        
        if j == 0:
            candidates.remove(((i,j), (i, j - 1)))

        if j == maxColumn:
            candidates.remove(((i, j), (i, j + 1)))
        candidates = [verifyTuplesOrder(candidate) for candidate in candidates]
        return candidates
            
def VerifyLockedPremises():
    global etat
    global indices


    allSegments = [segment for segment,status in etat.items() if status == 1]
    if len(allSegments) == 0:
        print("no lines")
        return False
    firstSegment = allSegments[0]
    firstSommet = firstSegment[0]
    res = thatFunc(previousSommet=firstSommet, segment=firstSegment, verifiedsegments=[], allSegments=allSegments)
    print("res for verifylocked :" + str(res))
    return res


def verifyAllCasesGreen():
    global indices
    global etat
    for i, val in enumerate(indices):
        for j, case in enumerate(val):
            if case == None:
                continue
            if statut_case(indices, etat, (i, j)) != 0:
                print("case :" + str((i, j)) + " is not green")
                return False
    print("all cases green")
    return True
def thatFunc(previousSommet=(), segment=((), ()), verifiedsegments=[], allSegments=[]):
    if segment in verifiedsegments:
        print("lngth verfiedsegments = " + str(len(verifiedsegments)) + " all segments length = " + str(len(allSegments)))
        if len(verifiedsegments) != len(allSegments):
            print("lose end not included in premises")
            return False
        
        return True

    segment = verifyTuplesOrder(segment)
    segmentList = list(segment)
    segmentList.remove(previousSommet)
    nextSommet = segmentList[0]
    possibleSegments = getSommetSegments(nextSommet)

    possibleSegments.remove(segment)
    candidateSegments = possibleSegments
    matchs = []
    for candidate in candidateSegments:
        res = etat.get(candidate, False)
        if res == 1:
            matchs.append(candidate)

    if len(matchs) == 0:
        print("premises not locked at " + str(nextSommet))
        return False
    elif len(matchs) > 1:
        print("premises have loss ends")
        return False
    elif len(matchs) == 1:
        print("perfect going for next segment")
        verifiedsegments.append(segment)
        return thatFunc(previousSommet=nextSommet, segment=matchs[0], verifiedsegments=verifiedsegments, allSegments=allSegments)
def handleGameClick(mouse, coords):
    global etat
    global indices
    global squareSide
    global distanceBetweenSquares
    global padding
    global clickables
    x, y = coords
    bsolve = clickables.get('solve', False)
    if bsolve and bsolve['x']['min'] <= x and x <= bsolve['x']['max'] and bsolve['y']['min'] <= y and bsolve['y']['max']:
        doSolveFunction()
        return

    def resetGame():
        global gGrille
        clearScreen()
        StartGame(gGrille)

    def exitGame():
        exit()

    def newGame():
        clearScreen()
        grilleScreen()
        pass

    actions = {
        'reset': resetGame,
        'exit': exitGame,
        'new': newGame
    }

    if 'reset' in clickables:
        for btn, data in clickables.items():
            if data and data['x']['min'] <= x and x <= data['x']['max'] and data['y']['min'] <= y and data['y']['max']:
                print("clicked " + btn)
                actions[btn]()
                return
    print("for :" + str(coords))

    i = math.ceil((y - padding) / (squareSide + distanceBetweenSquares)) - 1
    j = math.ceil((x - padding) / (squareSide + distanceBetweenSquares)) - 1

    row = len(indices)
    column = len(indices[0])
    print("max row : " + str(row))
    print("max column :" + str(column))
    if i > row  or i < 0:
        return
    if j > column  or j < 0:
        return
    sommet = (i, j)
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

    rect = {}
    segment = ()
    direction = ""
    if xInHorizontalRectangle and yInHorizontalRectangle:
        segment = ((i, j), (i, j+1))
        rect = horizontalRectangle
        direction = "horizontal"
        #rectangle(horizontalRectangle['x']['min'], horizontalRectangle['y']['min'] + 4, horizontalRectangle['x']['max'], horizontalRectangle['y']['max'] - 4, remplissage="black")
        print(segment)
    elif xInVerticalRectangle and yInVerticalRectangle:
        segment = ((i, j), (i + 1, j))
        rect = verticalRectangle
        direction = "vertical"
    else:
        return

    def createRect(rect, direction, padding = 4):
        if direction == "vertical":
            return rectangle(rect['x']['min'] + padding, rect['y']['min'], rect['x']['max'] - padding, rect['y']['max'], remplissage="black")
        elif direction == "horizontal":
            return rectangle(rect['x']['min'], rect['y']['min'] + padding, rect['x']['max'], rect['y']['max'] - padding, remplissage="black")
        pass

    verdict = etat.get(segment, False)
    print(verdict)
    if verdict == False:
        
        if mouse == "ClicGauche":
            etat[segment] = 1
            segmentsRef[segment] =  createRect(rect, direction)
        elif mouse == "ClicDroit":
            etat[segment] = -1
            centerX = (rect['x']['min'] + rect['x']['max']) / 2
            centerY = (rect['y']['min'] + rect['y']['max']) / 2
            segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")

    elif verdict == 1:
        if mouse == "ClicGauche":
            print("verdict = 1, click = gauche")
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            
            

            pass
        elif mouse == "ClicDroit":
            print("verdict = 1, click = droie")
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            etat[segment] = -1
            centerX = (rect['x']['min'] + rect['x']['max']) / 2
            centerY = (rect['y']['min'] + rect['y']['max']) / 2
            print((centerX, centerY))
            segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")
            pass
        
        print("exist must delete")

    elif verdict == -1:
        if mouse == "ClicGauche":
            efface(segmentsRef[segment])
            etat[segment] = 1
            segmentsRef[segment] =  createRect(rect, direction)
            
            pass
        elif mouse == "ClicDroit":
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            pass
        print("in vertical")
        print(segment)

    verifyCases = []
    maxRow = len(indices)
    maxColumn = len(indices[0])
    if direction == "vertical":
        if j == 0:
            verifyCases = [(i, j)]
            pass
        elif j == maxColumn:
            verifyCases = [(i, j - 1)]
            pass
        else:
            verifyCases = [(i, j), (i, j - 1)]
            pass 

    elif direction == "horizontal":
        if i == 0:
            verifyCases = [(i,j)]
        elif i == maxRow:
            verifyCases = [(i - 1, j)]
            pass
        else:
            verifyCases = [(i, j), (i - 1, j)]
            pass
    
    print("verifyCases : " + str(verifyCases))

    def updateTexte(case, color):
        i , j = case
        global gameTexts
        global indices
        global squareSide
        global distanceBetweenSquares
        global padding
        indice = indices[i][j]
        efface(gameTexts[case])
        lstartx = padding + j * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
        lstarty = padding + i * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
        gameTexts[case] = texte(lstartx, lstarty,str(indice), ancrage='center', taille=14, couleur=color)
        pass

    for case in verifyCases:
        res = statut_case(indices, etat, case)
        print("for case : " + str(case) + " result : " + str(res))
        if res == None:
            pass
        if res == 0:
            updateTexte(case, 'green')
        elif res == 1:
            updateTexte(case, 'black')
        elif res == -1:
            updateTexte(case, 'red')

    VerifyLockedPremises()
    verifyAllCasesGreen()

    if VerifyLockedPremises() and verifyAllCasesGreen():
        
        print(clickables['solve'])
        efface(clickables['solve']['rect'])
        efface(clickables['solve']['txt'])
        del clickables['solve']
        row = len(indices)
        column = len(indices[0])


        
        width = row * (squareSide + distanceBetweenSquares) + padding  * 3
        height = column * (squareSide + distanceBetweenSquares) + padding  * 3 + 80

        centerX = width / 2
        bwidth = 100
        bcenterX = bwidth / 2
        bheight = 50
        bcenterH = bheight / 2
        
        clickables['reset'] = createButton(10, height - 20 - bheight, bwidth, bheight, "Reset" )
        clickables['exit'] = createButton(centerX - bcenterX, height - 20 - bheight, bwidth, bheight, "Exit")
        clickables['new'] = createButton(width - 10 - bwidth, height - 20 - bheight, bwidth, bheight, "New" )
        
        texte(centerX , height - 20 - bheight - 30, "you won", "green", "center")
        global won
        won = True
        print("you have won")
    else:
        print("no win yet")

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

def drawGrid():
    global indices
    global gameTexts
    global squareSide
    global distanceBetweenSquares
    global padding
    global clickables
    row = len(indices)
    column = len(indices[0])


    
    width = row * (squareSide + distanceBetweenSquares) + padding  * 3
    height = column * (squareSide + distanceBetweenSquares) + padding  * 3 + 80

    centerX = width / 2
    bwidth = 150
    bcenterX = bwidth / 2
    bheight = 50
    bcenterH = bheight / 2
    cree_fenetre(width , height)
    clickables['solve'] = createButton(centerX - bcenterX, height - 20 - bheight, bwidth, bheight, "Solve" )
    
    for i in range(0, row + 1):
        starty = padding + i * (squareSide + distanceBetweenSquares)
        endy = padding + i * (squareSide + distanceBetweenSquares) + squareSide

        for j in range(0, column + 1 ):
            
            color = "black" if j % 2 == 0 else  "green"
            startx = padding + j * (squareSide + distanceBetweenSquares)
            endx = padding + j * (squareSide + distanceBetweenSquares)+ squareSide

            print({"x": {"min": startx, "max": endx}, "y": {"min": starty, "max": endy}})
            rectangle(startx, starty, endx, endy, remplissage=color)
            
            if i != row and j != column and indices[i][j] != None:
                lstartx = padding + j * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
                lstarty = padding + i * (squareSide + distanceBetweenSquares) + squareSide + distanceBetweenSquares / 2
                color = "green" if indices[i][j] == 0 else "black"
                gameTexts[(i, j)] = texte(lstartx, lstarty,str(indices[i][j]), ancrage='center', taille=14, couleur=color)
    print(gameTexts)

    #rectangle(200,100,300,150)
    #rectangle(300,400 ,300 ,400)
    mise_a_jour()
def StartGame(grille):
    global view
    global etat
    etat = {}
    view = "game"
    #cree_fenetre(800, 800)
    lireJeu('./grilles/' + grille + ".txt")
    drawGrid()
    global won
    won = False
    
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
        

    elif tev == 'Quitte':  # on sort de la boucle
        break

    else:  # dans les autres cas, on ne fait rien
        pass
    try:
        mise_a_jour()
    except:
        pass
    


