# Population element DNA object :

import copy, random

class ADNtrajet:
    
    ADN = list()
    tailleADN = 0
    fitness = 0
    globalFitness = 0
    fitnessList = list()
    vehiculeADNlist = list()
    
    
    def __init__(self, values, graph):
        self.ADN = values
        self.tailleADN = len(values)
        self.calcFitness(graph)
        
    def calcFitness(self, graph):
        startPos = 0
        stopPos = 0
        self.fitnessList = list()
        self.vehiculeADNlist = list()
        currentVehiculeFitness = 0
        for i in range(self.tailleADN-1):
            currentVehiculeFitness += graph[self.ADN[i]][self.ADN[i+1]]
            if self.ADN[i+1] == self.ADN[0]:
                stopPos = i+2
                self.vehiculeADNlist.append(self.ADN[startPos:stopPos])
                startPos = i+1
                self.fitnessList.append(currentVehiculeFitness)
                currentVehiculeFitness = 0
        self.fitness = max(self.fitnessList)
        
    def calcGlobalFitness(self, graph):
        # Calcul retour au sommet de départ
        self.globalFitness = 0
        for i in range(self.tailleADN-1):
            self.globalFitness += graph[self.ADN[i]][self.ADN[i+1]]
    
    def forceMutate(self, nbMutation, graph):
        for _ in range(nbMutation):
            swapPos1 = 0
            swapPos2 = 0
            swapDone = True
            while swapDone:
                swapPos1 =  random.randint(1, self.tailleADN-2)
                swapPos2 =  random.randint(1, self.tailleADN-2)
                if swapPos1 != swapPos2:
                    self.ADN[swapPos1], self.ADN[swapPos2] = self.ADN[swapPos2], self.ADN[swapPos1]
                    swapDone = False
        self.calcFitness(graph)
        self.calcGlobalFitness(graph)
                
#END CLASS "ANDtrajet"

# Population object
class Population:
    
    populations = []
    
    nbMutation = 0.01
    populationSize = 100
    
    graph = []
    nbSommet = 0
    nbVehivule = 1
    startPosition = 0
    debug = False
    
    bestPath = list()
    bestFitness = 0
    bestFitnessList = list()
    bestVehiculePath = list()
    bestGlobalFitness = 0
    
    def __init__(self, mutation, size, vehicule, graph, startPos, isDebug):

        


        self.nbMutation = mutation
        self.populationSize = size
        self.populations = []*(size + vehicule - 1)
        
        self.graph = graph
        self.nbSommet = len(graph)
        self.nbVehicule = vehicule
        if 0 <= startPos <= self.nbSommet - 1:
            self.startPosition = startPos
        else:
            if self.debug: print("Error: start position not valid, using 0 instead")
            self.startPosition = 0
        
        self.debug = isDebug
        
        defaultPath = list()
        for i in range(self.nbSommet):
            if i == self.startPosition:
                continue
            defaultPath.append(i)
        for _ in range(self.nbVehicule-1):
            defaultPath.append(self.startPosition)
        
        #First population value come from tabu algo
        self.populations.append(ADNtrajet.ADNtrajet(self.tabuADNGenerator(), graph))
        for i in range(size-1):
            randomPath = defaultPath.copy()
            random.shuffle(randomPath)
            randomPath.insert(0,self.startPosition)
            randomPath.append(self.startPosition)
            self.populations.append(ADNtrajet.ADNtrajet(randomPath, graph))
            
        self.populations.sort(key=lambda x: x.fitness)
        self.bestPath = self.populations[0].ADN.copy()
        self.bestFitness = self.populations[0].fitness
        self.bestFitnessList = self.populations[0].fitnessList
        self.bestVehiculePath = self.populations[0].vehiculeADNlist
        self.bestGlobalFitness = self.populations[0].globalFitness


    def tabuADNGenerator(self):
        tabuPath = tabu.tabu(self.graph, self.nbVehicule, 20, self.startPosition)
        #print(tabuPath)
        return tabuPath

    def getPopADNs(self):
        ADNs = list()
        for o in self.populations:
            ADNs.append(o.ADN)
        return ADNs
    
    def isDuplicate(self, i):
        ADNlist = self.getPopADNs()
        ADNlist.pop(i)
        if self.populations[i].ADN in ADNlist:
            return True
        else:
            return False
    
    def printPop(self):
        for o in self.populations:
            print(o.ADN, o.fitness)

    def start(self, maxGen):

        checkSmallSize = (self.nbSommet**2 - self.nbSommet) / 2
        if checkSmallSize <= self.populationSize:
            self.populationSize = round(checkSmallSize) - 1
            self.populations = self.populations[0:self.populationSize]
            maxGen = self.populationSize + 10

        progress = 0.00
        progressState = 10
        for nbGen in range(maxGen):
            progress = nbGen / maxGen * 100
            if progress >= progressState:
                if self.debug: print(progressState, "%")
                progressState += 10
            for i in range(round(self.populationSize/2)-1):
                self.populations[i+round(self.populationSize/2)] = copy.deepcopy(self.populations[i])
            for i in range(round(self.populationSize/2), self.populationSize):
                self.populations[i].forceMutate(self.nbMutation, self.graph)
                while self.isDuplicate(i):
                    self.populations[i].forceMutate(self.nbMutation, self.graph)
            self.populations.sort(key=lambda x: x.fitness)
            self.bestPath = self.populations[0].ADN.copy()
            self.bestFitness = self.populations[0].fitness
            self.bestFitnessList = self.populations[0].fitnessList
            self.bestVehiculePath = self.populations[0].vehiculeADNlist
            self.bestGlobalFitness = self.populations[0].globalFitness

# END CLASS "Population"

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

def calcPathEfficiency(graph, paths, doPrint = True):
    nbVehicules = len(paths)
    size = len(graph)
    
    totLen = 0
    totLenVehicules = [0 for i in range(nbVehicules)]
    
    # Check data validity
    prefix = "[INVALID PATH]"
    for v in range(nbVehicules):
        if(paths[v][0] != paths[v][len(paths[v])-1]):
            print(prefix, "Path for vehicule", v, "does not return to starting point!")
    concatPaths = [j for i in paths for j in i]
    for i in range(size):
        if(i not in concatPaths):
            print(prefix, "The point", i, "is not taken by any vehicule!")
    if(len(concatPaths) > size + (len(paths)*2)-1):
        print(prefix, "Invalid path length! (Some points are taken multiple times?)")
        print("> Got", len(concatPaths), "expected", size + (len(paths)*2)-1)
    
    # Calculate path length
    for v in range(nbVehicules):
        for i in range(len(paths[v])):
            if(i+1 >= len(paths[v])):
                break
            current = paths[v][i]
            neighbour = paths[v][i+1]
            weight = graph[current][neighbour]
            totLen += weight
            totLenVehicules[v] += weight
    
    if(doPrint):
        print("Total weight:", totLen)
    if(doPrint):
        for i in range(nbVehicules): print(" - Weight for vehicule", i, ":", totLenVehicules[i])
    worst = max(totLenVehicules)
    worstIndex = totLenVehicules.index(worst)
    if(doPrint):
        print("Worst weight found for vehicule", worstIndex, "(", worst, ")")
    
    return (worst, worstIndex, totLenVehicules)

def tabu(graph, nbVehicules, nbIter, startPoint):
    initGraph = graph
    #startPoint = 0
    
    # Init tabou list (will store a path between 2 points)
    tabuList = [[] for i in range(nbVehicules)]
    maxTabuListSize = 50
    
    bestPathIteration = {}
        
    for it in range(nbIter):
        
        currentElements = [startPoint] * nbVehicules
        bestPaths = [[startPoint] for i in range(nbVehicules)]
        bestDistances = [[] for i in range(nbVehicules)]
        visited = [startPoint]
        
        totLens = [0] * nbVehicules
        totPoints = len(graph)
        
        prematurateEnd = False
        
        while len(visited) < len(graph) and not prematurateEnd:
            #print(len(visited), len(graph))

            # Loop for every vehicule
            for v in range(nbVehicules):

                if(len(visited) >= len(graph)):
                    break

                # Worst case
                bestDistance = 99999999999
                bestNeighbour = startPoint

                # Search nearest neighbour
                for j in range(totPoints):
                    # Check if the path is not used (including other vehicules) + Check if path exists in tabu
                    if(currentElements[v] != j and j not in visited and (currentElements[v], j) not in tabuList[v]):
                        neighbour = graph[currentElements[v]][j]
                        if(neighbour <= bestDistance):
                            bestDistance = neighbour
                            bestNeighbour = j
                            tabuList[v].append((currentElements[v], j))
                            if(len(tabuList[v]) > maxTabuListSize):
                                tabuList[v].pop(0)

                # Could not find a solution => All combinaisons in tabou have been tried
                if(bestNeighbour == startPoint):
                    #print("NO SOLUTION", (currentElements[v], j))
                    # Search nearest neighbour
                    for j in range(totPoints):
                        # Check if the path is not used (including other vehicules) + Check if path exists in tabu
                        if(currentElements[v] != j and j not in visited):
                            neighbour = graph[currentElements[v]][j]
                            if(neighbour <= bestDistance):
                                bestDistance = neighbour
                                bestNeighbour = j

                bestPaths[v].append(bestNeighbour)
                visited.append(bestNeighbour)
                currentElements[v] = bestNeighbour
                totLens[v] += bestDistance
                bestDistances[v].append(bestDistance)

        for v in range(nbVehicules):
            # Return to start point
            bestPaths[v].append(startPoint)
            totLens[v] += graph[currentElements[v]][startPoint]
            bestDistances[v].append(graph[currentElements[v]][startPoint])
            
        worst, worstIndex, tot = calcPathEfficiency(initGraph, bestPaths, False)
        #print("ITER ", it, worst)
        if bestPathIteration.get("worst") is None or worst < bestPathIteration["worst"]:
            #print("New best for it", it, worst)
            bestPathIteration = {
                "bestPaths": bestPaths,
                "bestDistances": bestDistances,
                "totLens": totLens,
                "worst": worst
            }

    #print(tabuList)
    print(bestPathIteration["worst"])

    resultPath = list()
    for i, o in enumerate(bestPathIteration["bestPaths"]):
        for y in range(len(o)-1):
            resultPath.append(o[y])
    resultPath.append(startPoint)
    
    return resultPath