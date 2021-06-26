# Population element DNA object :

import random

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