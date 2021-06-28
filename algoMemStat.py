# Importer les bon trucs
import tracemalloc
import matplotlib.pyplot as plt
import algogenOGM.geneticPathFinderOGM
from graphGeneration import randomDataGenerator

def genMemoryStat(minSize, maxSize, populationSize):
    peakMemoryList = list()
    graphSizeList = list()
    for i in range(minSize-1, maxSize):
        # print(i)
        tracemalloc.start()
        dataGraph = randomDataGenerator(1, i, False)
        geneticPathFinderOGM(mutationRate, populationSize, 3, 5000, 1, dataGraph, 0, False)
        # Memory allocation display
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if i == minSize-1: continue
        peakMemoryList.append(peak / 10**6)
        graphSizeList.append(i)
        
    coefGen = np.polyfit(graphSizeList, peakMemoryList, 1)
    poly1d_fnGen = np.poly1d(coefGen)
        
    plt.figure(figsize=(20,10))
    plt.xlabel("Taille du graphe")
    plt.ylabel("Pic d'utilisation mémoire (en MB)")
    plt.plot(graphSizeList, peakMemoryList, "bo", graphSizeList, poly1d_fnGen(graphSizeList) label="gen")
    plt.show()
    
    return peakMemoryList