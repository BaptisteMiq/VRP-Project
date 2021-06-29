import numpy as np
import random
import pprint

def randomDataGenerator(proba, nbSommet, doPrint, max = 1):
    b = np.random.choice((1, 0), size=(nbSommet,nbSommet), p=[proba, 1-proba])
    mat_sym = np.logical_or(b, b.T)
    #seconde instance de tableau
    newTab = [0] * nbSommet
    #generation du tableau à partir du nombre de sommet
    for i in range(nbSommet):
            newTab[i] = [0] * nbSommet
            for j in range(nbSommet):
                newTab[i][j] = 0
    #Generation des nombre de prevision sur les aretes
    for indexX,x in enumerate(mat_sym.astype(int)):
        for indexY,y in enumerate(x):
            if y == 1 and indexY != indexX:
                rand = round(random.randint(1, max) if max != 1 else random.random(), 2 if max == 1 else 0)
                if rand == 0: rand = 0.01
                #génère le random de prevision dans les deux points du tableaux
                newTab[indexX][indexY] = rand
                newTab[indexY][indexX] = rand
    
    if doPrint:
        pprint.pprint(newTab)
        
    #initGraph = newTab
    return newTab

# graph = randomDataGenerator(1, 20, False)
# print(graph)