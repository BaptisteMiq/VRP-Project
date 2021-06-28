import threading
from algorithms.genetic import geneticPathFinder
from numba import jit, cuda

class GeneticThread(threading.Thread):
    def __init__(self, ind, g, worstsGen):
        threading.Thread.__init__(self)
        self.ind = ind
        self.g = g
        self.worstsGen = worstsGen
               
    def run(self):
        
        print("Starting thread", self.ind)
        
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
        worst = geneticPathFinder(mutationRate, populationSize, nbCamion, maxGen, maxIteration, self.g, position)
        self.worstsGen[self.ind] = worst
        
        print("Found a result for ind", self.ind, ":", worst)


# Wait all threads results
# while -1 in worstsGen:
#     print(worstsGen)
#     time.sleep(0.1)

# Genetic  
# Using a thread to calculate the best path with genetic algorithm helps finding a solution faster
# genThreads[it] = MultiprocessGen(it, g, worstsGen)
# genThreads[it].start()