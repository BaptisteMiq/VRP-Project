from starts import StartAlgorithm
import time
import numpy as np
import matplotlib.pyplot as plt

import math

from graphGeneration import randomDataGenerator
from graphChecker import calcPathEfficiency

from tabu import tabu
from threads import GeneticThread
# from multiprocess import Multiprocess

from functools import partial

import multiprocessing as mp

# Maximum graph size
maxGraph = randomDataGenerator(1, 500, False)

# Setup iterations
minSize = 10
maxSize = 400
padding = 20
graphIterations = len([i for i in range(minSize, maxSize, padding)])

# Setup lists of worst cases for every algorithm
worstsTabu = []
worstsGen = [-1] * graphIterations

genThreads = [None for _ in range(graphIterations)]

it = 0 # Index of genThread to insert the result of the thread
for i in range(minSize, maxSize, padding):  
    # Cut the max size graph
    g = []
    for j in range(i):
        g.append(maxGraph[j][0:i])
    initGraph = g

    # Tabu
    result = tabu(g, 1, 1)
    worst, worstIndex, totLen = calcPathEfficiency(initGraph, result[0], False)
    worstsTabu.append(worst)


    genThreads[it] = {
        "g": g,
        "nbVehicules": 1
    }
    
    it += 1

# Define shared variables between processes
manager = mp.Manager()
worstsGenShared = manager.list(range(len(worstsGen)))

# Wrap all algorithm functions to be started with only one argument
def startGeneticWrapper(it):
    StartAlgorithm.Genetic(it, worstsGenShared, genThreads[it])

cores = mp.cpu_count() # Computer cores
coreProcesses = cores * 32 # Number of processes available for multiprocess pool

# Define multi process logic
def Multiprocess(maxCores = cores):
    # Define a maximum number of cores to use at the same time
    # Will crash if the maximum is over the number of available cores
    for i in range(math.ceil(len(genThreads) / maxCores)):
        print("Starting process subdivision", i)
        # Start the algorithm on every specified core
        p = mp.Pool(maxCores * 32)
        print(i*maxCores, min(i*maxCores+maxCores, len(genThreads)))
        p.map(startGeneticWrapper, range(i*maxCores, min(i*maxCores+maxCores, len(genThreads))))
        p.close()
        time.sleep(2)
    return worstsGenShared

worstsGen = Multiprocess(cores - 2)

x = [i for i in range(minSize, maxSize, padding)]

# Parse data of tabou and add regression
yTabu = worstsTabu
coefTabu = np.polyfit(x, yTabu, 1)
poly1d_fnTabu = np.poly1d(coefTabu)

# Parse data of genetic and add regression
yGen = worstsGen
coefGen = np.polyfit(x, yGen, 1)
poly1d_fnGen = np.poly1d(coefGen)

#print(len(x), len(yTabu), len(yGen))

# Draw graph on plt
plt.figure(figsize=(20,10))
plt.xlabel("Taille du graphe")
plt.ylabel("Pire cas trouvé")

plt.plot(x, yTabu, "bo", x, poly1d_fnTabu(x), label="Tabu")
plt.plot(x, yGen, "yo", x, poly1d_fnGen(x), label="Genetic")

plt.xlim(0, maxSize)
plt.legend()
plt.show()