verdict = etat.get(segment, False)
    print(verdict)
    if verdict == False:
        
        if mouse == "ClicGauche":
            etat[segment] = 1
            segmentsRef[segment] =  rectangle(rect['x']['min'] + 4, rect['y']['min'], rect['x']['max'] - 4, rect['y']['max'], remplissage="black")
        elif mouse == "ClicDroit":
            etat[segment] = -1
            centerX = (rect['x']['min'] + rect['x']['max']) / 2
            centerY = (rect['y']['min'] + rect['y']['max']) / 2
            segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")

    elif verdict == 1:
        if mouse == "ClicGauche":
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            etat[segment] = -1
            centerX = (rect['x']['min'] + rect['x']['max']) / 2
            centerY = (rect['y']['min'] + rect['y']['max']) / 2
            segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")

            pass
        elif mouse == "ClicDroit":
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            etat[segment] = -1
            centerX = rect['x']['min'] + rect['x']['max']
            centerY = rect['y']['min'] + rect['y']['max']
            segmentsRef[segment] = rectangle(centerX - 5 , centerY - 5, centerX + 5, centerY + 5, remplissage="red")
            pass
        
        print("exist must delete")

    elif verdict == -1:
        if mouse == "ClicGauche":
            efface(segmentsRef[segment])
            etat[segment] = 1
            segmentsRef[segment] =  rectangle(rect['x']['min'] + 4, rect['y']['min'], rect['x']['max'] - 4, rect['y']['max'], remplissage="black")
            
            pass
        elif mouse == "ClicDroit":
            efface(segmentsRef[segment])
            segmentsRef.pop(segment, None)
            etat.pop(segment, None)
            pass