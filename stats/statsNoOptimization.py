import time
import numpy as np
import matplotlib.pyplot as plt

from graphGeneration import randomDataGenerator
from graphChecker import calcPathEfficiency

from tabu import tabu
from genetic import geneticPathFinder

# Maximum graph size
maxGraph = randomDataGenerator(1, 500, False)
# Setup iterations
minSize = 5
maxSize = 100
padding = 15
# Setup lists of worst cases for every algorithm
worstsTabu = []
worstsGen = []

for i in range(minSize, maxSize, padding):  
    # Cut the max size graph
    g = []
    for j in range(i):
        g.append(maxGraph[j][0:i])
    initGraph = g

    # Tabu
    result = tabu(g, 3, 1)
    worst, worstIndex, totLen = calcPathEfficiency(initGraph, result[0], False)
    worstsTabu.append(worst)
    
    # Genetic
    # A ne pas changer : config opti
    mutationRate = 1
    populationSize = 40
    maxGen = 10000
    maxIteration = 1
    # Parametre 
    position = 0
    nbCamion = 3
    # Start algorithm
    result = geneticPathFinder(mutationRate, populationSize, nbCamion, maxGen, maxIteration, g, position)
    worst, worstIndex, totLen = calcPathEfficiency(initGraph, result, False)
    worstsGen.append(worst)

xTabu = [i for i in range(minSize, maxSize, padding)]
yTabu = worstsTabu
# Regression
coefTabu = np.polyfit(xTabu, yTabu, 1)
poly1d_fnTabu = np.poly1d(coefTabu)

xGen = [i for i in range(minSize, maxSize, padding)]
yGen = worstsGen
# Regression
coefGen = np.polyfit(xGen, yGen, 1)
poly1d_fnGen = np.poly1d(coefGen)

#print(len(xTabu), len(yTabu), len(xGen), len(yGen))

plt.figure(figsize=(20,10))
plt.xlabel("Taille du graphe")
plt.ylabel("Pire cas trouvé")
#plt.plot(x, y, "gray")
plt.plot(xTabu, yTabu, "bo", xTabu, poly1d_fnTabu(xTabu), label="Tabu")
plt.plot(xGen, yGen, "yo", xGen, poly1d_fnGen(xGen), label="Genetic")
plt.xlim(0, maxSize)
plt.legend()
#plt.plot([1,2,3], label='durée au pire')
plt.show()