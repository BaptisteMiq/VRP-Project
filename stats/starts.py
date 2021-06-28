from tabouletOGM.algogenOGM import geneticPathFinderOGM
from algorithms.genetic import geneticPathFinder
import tracemalloc
import time

class StartAlgorithm:
    def Genetic(ind, worstsGenShared, ramGenShared, timeGenShared, data):
        print("Calculating genetic", ind)

        tracemalloc.start()

        startTime = time.time()

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
        worst = geneticPathFinder(mutationRate, populationSize, data["nbVehicules"], maxGen, maxIteration, data["g"], position)
        worstsGenShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramGenShared[ind] = peak / 10**6

        timeGenShared[ind] = time.time() - startTime

        print("Found a result for genetic", ind, ":", worst)

    def TabouOGM(ind, worstsTabouOGMShared, ramTabouOGMShared, timeTabouOGMShared, data):
        print("Calculating taboulet OGM", ind)

        tracemalloc.start()

        startTime = time.time()

        mutationRate = 1
        populationSize = 40
        maxGen = 5000
        maxIteration = 1
        position = 0
        nbCamion = 6

        #pop = Population(mutationRate,populationSize, nbCamion, graph, position, True)
        # pop.tabuADNGenerator()

        worst = geneticPathFinderOGM(mutationRate, len(data["g"]), data["nbVehicules"], maxGen, data["g"], 0, True)
        worstsTabouOGMShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramTabouOGMShared[ind] = peak / 10**6

        timeTabouOGMShared[ind] = time.time() - startTime

        print("Found a result for taboulet OGM", ind, ":", worst)
