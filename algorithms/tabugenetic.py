#Importation de l'algorithme tabou
from algorithms.tabu import tabu
import copy, random

#Classe ADN de trajet
# - Objet décrivant un élément contenu dans la liste population
# - Possède toutes les attributs et méthodes nécessaire à la situation(score de fitness) d'un  élément dans la population
class ADNtrajet:
    
    ADN = list()                #Liste descriptive du trajet ou configuration de trajet totale (tout camion confondu)
    tailleADN = 0               #Taille de la liste ADN
    fitness = 0                 #Score de fitness, correspond à la somme de pondération du pire trajet d'un camion
    globalFitness = 0           #Score de fitness total tout camion confondu
    fitnessList = list()        #Liste des différentes fitness, pour chaque camion
    vehiculeADNlist = list()    #Liste des trajet par camion
    
    #Initialisation de l'objet élément ADNtrajet
    def __init__(self, values, graph):
        self.ADN = values
        self.tailleADN = len(values)
        self.calcFitness(graph)


    #Méthode de calcul et de mise à jour des fitness de l'élément
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
        
    #Méthode de calcul de la fitness globale
    def calcGlobalFitness(self, graph):
        # Calcul retour au sommet de départ
        self.globalFitness = 0
        for i in range(self.tailleADN-1):
            self.globalFitness += graph[self.ADN[i]][self.ADN[i+1]]
    
    #Méthode de mutation de l'ADN (configuration du trajet) de l'élément
    #La mutation s'effectue par la permutation de deux sommets dans l'ADN
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
    
    populations = []            #Liste des éléments de la population

    nbMutation = 1              #Nombre de mutaion à effectuer sur les éléments concernés
    populationSize = 100        #Taille de la population (taille de liste)
    
    graph = []                  #Graphe complet avec pondération, où on peut récupérer les données de sommet et de pondération
    nbSommet = 0                #Nombre de sommet dans le graphe
    nbVehivule = 1              #Nombre de véhicules qui doivent parcourir le graphe
    startPosition = 0           #Position de départ (ou dépôt) des véhicule dans le graphe
    debug = False               #Mode de debug (affichage des prints)
    
    bestPath = list()           #Meilleure configuration de trajet globale enregistrée
    bestFitness = 0             #Meilleure score de fitness (du pire trajet de camion) provenant du meilleur élément de la population
    bestFitnessList = list()    #Meilleure liste de fitness par véhicule
    bestVehiculePath = list()   #Meilleure configuration de trajet par véhicule
    bestGlobalFitness = 0       #Meilleure fitness globale
    
    #Initialisation de la population
    # - Création de tous les éléments dans la population
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

    #Méthode utilisant le tabou afin de créer une configuration de base pour la nouvelle population
    def tabuADNGenerator(self):
        tabuPath = tabu(self.graph, self.nbVehicule, 20, self.startPosition, True)
        #print(tabuPath)
        return tabuPath

    #Méthode retournant toutes les ADNs (configuration de trajet) des éléments
    def getPopADNs(self):
        ADNs = list()
        for o in self.populations:
            ADNs.append(o.ADN)
        return ADNs
    
    #Méthode permettant de vérifier si un élément est en double dans la liste de population
    def isDuplicate(self, i):
        ADNlist = self.getPopADNs()
        ADNlist.pop(i)
        if self.populations[i].ADN in ADNlist:
            return True
        else:
            return False
    
    #Méthode permettant d'afficher les ADNs des élements
    def printPop(self):
        for o in self.populations:
            print(o.ADN, o.fitness)

    #Méthode permettant de lancer l'algorithme tabou-génétique en fonction du nombre de génération maximale à effectuer
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

#Fonction permettant d'effectuer plusieurs itérations sur l'algorithme
def iterateGeneticPathFinderOGM(mutationChance, graphSize, nbVehicule, maxGeneneration, nbIteration, graph, startPosition, isDebug):
    if isDebug: print("--- LANCEMENT DE L'ALGORITHME DE RECHERCHE TABOU GENETIQUE ---")
    
    bestPath = list()
    bestFitnessList = list()
    bestVehiculePath = list()
    bestFitness = 0
    bestGlobalFitness = 0

    for nbIte in range(nbIteration):
        if isDebug: print("------ Nouvelle itération:", nbIte)
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
        print("--- !!! FINI !!! ---")
        print(bestPath)
        print("Camion avec la pire pondération cumulée:",bestFitness)
        print("Somme des pondérations cumulées:", bestGlobalFitness)
        print("Trajets des camions:")
        # print(bestVehiculePath)
        # print(bestFitnessList)
        for i in range(len(bestFitnessList)):
            print("Véhicule N°", i, "-", bestVehiculePath[i], "-", bestFitnessList[i])


#Fonction permettant de lancer l'algorithme tabou-génétique (une seule itérations)
def geneticPathFinderOGM(mutationChance, graphSize, nbVehicule, maxGeneneration, graph, startPosition, isDebug, returnList = False):
    if isDebug: print("--- LANCEMENT DE L'ALGORITHME DE RECHERCHE TABOU GENETIQUE ---")
    
    pop = Population(mutationChance, graphSize, nbVehicule, graph, startPosition, isDebug)
    pop.start(maxGeneneration)
    
    bestPath = pop.bestPath
    bestFitness = pop.bestFitness
    bestFitnessList = pop.bestFitnessList
    bestVehiculePath = pop.bestVehiculePath
    bestGlobalFitness = pop.bestGlobalFitness

    if isDebug:
        print("-------------------------------------------------")
        print("--- !!! FINI !!! ---")
        print("Camion avec la pire pondération cumulée:",bestFitness)
        print("Somme des pondérations cumulées:", bestGlobalFitness)
        print("Trajets des camions:")
        for i in range(len(bestFitnessList)):
            print("Véhicule N°", i, "-", bestVehiculePath[i], "-", bestFitnessList[i])
        
    if(returnList):
        return bestVehiculePath
    else:
        return bestFitness
