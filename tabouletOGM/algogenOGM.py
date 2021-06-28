from . import Population

# Alfo génétique pour solution problème voyageur de commerce complet :
def iterateGeneticPathFinderOGM(mutationChance, graphSize, nbVehicule, maxGeneneration, nbIteration, graph, startPosition, isDebug):
    if isDebug: print("--- STARTING GENETIC ALGORITHME GRAPH PATH FINDING ---")
    
    bestPath = list()
    bestFitnessList = list()
    bestVehiculePath = list()
    bestFitness = 0
    bestGlobalFitness = 0

    for nbIte in range(nbIteration):
        if isDebug: print("------ Entering new iteration:", nbIte)
        pop = Population.Population(mutationChance, graphSize, nbVehicule, graph, startPosition, isDebug)
        pop.start(maxGeneneration)
        if pop.bestFitness > bestFitness:
            bestPath = pop.bestPath
            bestFitness = pop.bestFitness
            bestFitnessList = pop.bestFitnessList
            bestVehiculePath = pop.bestVehiculePath
            bestGlobalFitness = pop.bestGlobalFitness

    if isDebug:
        print("-------------------------------------------------")
        print("--- !!! FINISHED !!! ---")
        print(bestPath)
        print("worst fitness:",bestFitness)
        print("global fitness:", bestGlobalFitness)
        print("detailed vehicule fitness list:")
        print(bestVehiculePath)
        print(bestFitnessList)
        for i in range(len(bestFitnessList)):
            print("Vehicule N°", i, "-", bestVehiculePath[i], "-", bestFitnessList[i])


# Alfo génétique pour solution problème voyageur de commerce complet :
def geneticPathFinderOGM(mutationChance, graphSize, nbVehicule, maxGeneneration, graph, startPosition, isDebug):
    if isDebug: print("--- STARTING GENETIC ALGORITHME GRAPH PATH FINDING ---")
    
    pop = Population.Population(mutationChance, graphSize, nbVehicule, graph, startPosition, isDebug)
    pop.start(maxGeneneration)
    
    bestPath = pop.bestPath
    bestFitness = pop.bestFitness
    bestFitnessList = pop.bestFitnessList
    bestVehiculePath = pop.bestVehiculePath
    bestGlobalFitness = pop.bestGlobalFitness

    if isDebug:
        print("-------------------------------------------------")
        print("--- !!! FINISHED !!! ---")
        print(bestPath)
        print("worst fitness:",bestFitness)
        print("global fitness:", bestGlobalFitness)
        print("detailed vehicule fitness list:")
        print(bestVehiculePath)
        print(bestFitnessList)
        for i in range(len(bestFitnessList)):
            print("Vehicule N°", i, "-", bestVehiculePath[i], "-", bestFitnessList[i])
        
    return bestFitness