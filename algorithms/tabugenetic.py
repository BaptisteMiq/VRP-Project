# Population element DNA object :
from algorithms.tabu import tabu

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

        if self.nbSommet == 0 or self.nbSommet == 1:
            print("Error: graph node number is null or ")
            return

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
        self.populations.append(ADNtrajet(self.tabuADNGenerator(), graph))
        for i in range(size-1):
            randomPath = defaultPath.copy()
            random.shuffle(randomPath)
            randomPath.insert(0,self.startPosition)
            randomPath.append(self.startPosition)
            self.populations.append(ADNtrajet(randomPath, graph))
            
        self.populations.sort(key=lambda x: x.fitness)
        self.bestPath = self.populations[0].ADN.copy()
        self.bestFitness = self.populations[0].fitness
        self.bestFitnessList = self.populations[0].fitnessList
        self.bestVehiculePath = self.populations[0].vehiculeADNlist
        self.bestGlobalFitness = self.populations[0].globalFitness


    def tabuADNGenerator(self):
        tabuPath = tabu(self.graph, self.nbVehicule, 20, self.startPosition, True)
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

        if self.nbSommet == 2:
            self.bestPath = [0,1,0]
            self.bestFitness = (self.graph[0][2] * 2)
            #self.bestFitnessList = self.populations[0].fitnessList
            #self.bestVehiculePath = self.populations[0].vehiculeADNlist
            #self.bestGlobalFitness = self.populations[0].globalFitness
            return

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
        pop = Population(mutationChance, graphSize, nbVehicule, graph, startPosition, isDebug)
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
    
    pop = Population(mutationChance, graphSize, nbVehicule, graph, startPosition, isDebug)
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
