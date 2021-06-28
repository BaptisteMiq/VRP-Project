import tracemalloc
from stats.starts import StartAlgorithm
import time
import numpy as np
import matplotlib.pyplot as plt

import math

from graphGeneration import randomDataGenerator
from graphChecker import calcPathEfficiency

from algorithms.tabu import tabu
from . import threads

from functools import partial

import multiprocessing as mp

genThreads = []
worstsGenShared = []
ramGenShared = []
timeGenShared = []

tabouOGMThreads = []
worstsTabouOGMShared = []
ramTabouOGMShared = []
timeTabouOGMShared = []


# Wrap all algorithm functions to be started with only one argument
def startGeneticWrapper(it):
    print("genThreads", genThreads)
    StartAlgorithm.Genetic(it, worstsGenShared, ramGenShared, timeGenShared, genThreads[it])
def startTabouOGMWrapper(it):
    StartAlgorithm.TabouOGM(it, worstsTabouOGMShared, ramTabouOGMShared, timeTabouOGMShared, tabouOGMThreads[it])

def GetStats(minIterations, maxIterations, padding, algos):

    # Maximum graph size
    maxGraph = randomDataGenerator(1, maxIterations, False)

    # Setup iterations
    minSize = minIterations
    maxSize = maxIterations
    graphIterations = len([i for i in range(minSize, maxSize, padding)])

    # Setup lists of worst cases for every algorithm
    worstsTabu = []
    worstsGen = [-1] * graphIterations
    worstsTabouOGM = [-1] * graphIterations

    ramTabu = []
    ramGen = [-1] * graphIterations
    ramTabouOGM = [-1] * graphIterations

    timeTabu = []
    timeGen = [-1] * graphIterations
    timeTabouOGM = [-1] * graphIterations

    global genThreads
    global tabouOGMThreads
    genThreads = [None for _ in range(graphIterations)]
    tabouOGMThreads = [None for _ in range(graphIterations)]    

    it = 0 # Index of genThread to insert the result of the thread
    for i in range(minSize, maxSize, padding):  
        # Cut the max size graph
        g = []
        for j in range(i):
            g.append(maxGraph[j][0:i])
        initGraph = g

        # Tabu
        tracemalloc.start()

        startTime = time.time()

        result = tabu(g, 1, 1)
        worst, worstIndex, totLen = calcPathEfficiency(initGraph, result[0], False)
        worstsTabu.append(worst)

        timeTabu.append(time.time() - startTime)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramTabu.append(peak / 10**6)

        genThreads[it] = {
            "g": g,
            "nbVehicules": 1
        }

        tabouOGMThreads[it] = {
            "g": g,
            "nbVehicules": 1
        }
        
        it += 1

    # Define shared variables between processes
    manager = mp.Manager()
    global worstsGenShared
    global worstsTabouOGMShared
    worstsGenShared = manager.list(range(len(worstsGen)))
    worstsTabouOGMShared = manager.list(range(len(worstsTabouOGM)))

    global ramGenShared
    global ramTabouOGMShared
    ramGenShared = manager.list(range(len(ramGen)))
    ramTabouOGMShared = manager.list(range(len(ramTabouOGM)))

    global timeGenShared
    global timeTabouOGMShared
    timeGenShared = manager.list(range(len(timeGen)))
    timeTabouOGMShared = manager.list(range(len(timeTabouOGM)))

    cores = mp.cpu_count() # Computer cores
    # coreProcesses = cores * 32 # Number of processes available for multiprocess pool

    # Define multi process logic
    def Multiprocess(maxCores = cores):
        # Define a maximum number of cores to use at the same time
        # Will crash if the maximum is over the number of available cores
        for i in range(math.ceil(len(genThreads) / maxCores)):
            print("Starting process subdivision", i)
            # Start the algorithm on every specified core
            
            try:
                mp.set_start_method('spawn')
            except RuntimeError:
                pass

            p = mp.Pool(maxCores * 32)
            print(i*maxCores, min(i*maxCores+maxCores, len(genThreads)))
            p.map(startGeneticWrapper, range(i*maxCores, min(i*maxCores+maxCores, len(genThreads))))
            p.close()
        return (worstsGenShared, ramGenShared, timeGenShared)

    if("genetic" in algos):
        worstsGen, ramGen, timeGen = Multiprocess(cores // 2)

        # Define multi process logic
    def MultiprocessOGM(maxCores = cores):
        # Define a maximum number of cores to use at the same time
        # Will crash if the maximum is over the number of available cores
        for i in range(math.ceil(len(tabouOGMThreads) / maxCores)):
            print("Starting process subdivision", i)
            # Start the algorithm on every specified core
            
            try:
                mp.set_start_method('spawn')
            except RuntimeError:
                pass

            p = mp.Pool(maxCores * 32)
            print(i*maxCores, min(i*maxCores+maxCores, len(tabouOGMThreads)))
            p.map(startTabouOGMWrapper, range(i*maxCores, min(i*maxCores+maxCores, len(tabouOGMThreads))))
            p.close()
        return (worstsTabouOGMShared, ramTabouOGMShared, timeTabouOGMShared)

    if("tabouOGM" in algos):
        worstsTabouOGM, ramTabouOGM, timeTabouOGM = MultiprocessOGM(cores // 2)

    x = [i for i in range(minSize, maxSize, padding)]

    dataset = []
    if("tabou" in algos):
        dataset.append({ "label": "Tabou", "worst": worstsTabu, "ram": ramTabu, "time": timeTabu })
    if("genetic" in algos):
        dataset.append({ "label": "Génétique", "worst": worstsGen, "ram": ramGen, "time": timeGen })
    if("tabouOGM" in algos):
        dataset.append({ "label": "Taboulé OGM", "worst": worstsTabouOGM, "ram": ramTabouOGM, "time": timeTabouOGM })

    return (x, dataset)

def showStats(x, dataset, maxGraphSize, type):

    datasetWithRegression = []

    for k, data in enumerate(dataset):

        print("-----------------------")
        print(data["worst"])
        print(data["ram"])
        print(data["time"])
        

        # Calculate regression
        coef = np.polyfit(x, data[type], 1)
        poly1d_fn = np.poly1d(coef)
        datasetWithRegression.append({
            "label": data["label"],
            "value": data[type],
            "regValue": poly1d_fn(x)
        })

    # Draw graph on plt
    plt.figure(figsize=(20,10))
    plt.xlabel("Taille du graphe")
    plt.ylabel("Pire cas trouvé" if type == "worst" else "RAM utilisée" if type == "ram" else "Temps d'exécution")

    colors = ["bo", "yo", "go"]
    for k, data in enumerate(datasetWithRegression):
        plt.plot(x, data["value"], colors[k%len(colors)], x, data["regValue"], label=data["label"])

    plt.xlim(0, maxGraphSize)
    plt.legend()
    plt.show()