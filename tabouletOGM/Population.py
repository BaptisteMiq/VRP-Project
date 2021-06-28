# Population object
import copy, random
from . import ADNtrajet
from . import tabu

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
        print(tabuPath)
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
        progress = 0.00
        progressState = 10
        for nbGen in range(maxGen):
            progress = nbGen / maxGen * 100
            if progress >= progressState:
                if self.debug: print(progressState, "%")
                progressState += 10
            for i in range(round(self.populationSize/2)):
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