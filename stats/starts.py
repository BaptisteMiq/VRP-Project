from algorithms.tabugenetic import geneticPathFinderOGM
from algorithms.genetic import geneticPathFinder
from algorithms.fourmi import antColonyAlg
from algorithms.recuit import getBestRS
from algorithms.google import googleORTools
import tracemalloc
import time

class StartAlgorithm:
    def Genetic(ind, worstsGenShared, ramGenShared, timeGenShared, data, doPrint):
        if(doPrint): print("Calculating genetic", ind, "(", len(data["g"]), ":", data["nbVehicules"], ")")

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
        # Start algorithm
        worst = geneticPathFinder(mutationRate, populationSize, data["nbVehicules"], maxGen, maxIteration, data["g"], position)
        worstsGenShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramGenShared[ind] = peak / 10**6

        timeGenShared[ind] = time.time() - startTime

        if(doPrint): print("Found a result for genetic", ind, ":", worst)

    def TabouOGM(ind, worstsTabouOGMShared, ramTabouOGMShared, timeTabouOGMShared, data, doPrint):
        if(doPrint): print("Calculating taboulet OGM", ind, "(", len(data["g"]), ":", data["nbVehicules"], ")")

        tracemalloc.start()

        startTime = time.time()

        mutationRate = 1
        maxGen = 5000

        #pop = Population(mutationRate,populationSize, nbCamion, graph, position, True)
        # pop.tabuADNGenerator()

        worst = geneticPathFinderOGM(mutationRate, len(data["g"]), data["nbVehicules"], maxGen, data["g"], 0, False)
        worstsTabouOGMShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramTabouOGMShared[ind] = peak / 10**6

        timeTabouOGMShared[ind] = time.time() - startTime

        if(doPrint): print("Found a result for taboulet OGM", ind, ":", worst)

    def Fourmi(ind, worstsFourmiShared, ramFourmiShared, timeFourmiShared, data, doPrint):
        if(doPrint): print("Calculating ant colony", ind, "(", len(data["g"]), ":", data["nbVehicules"], ")")

        tracemalloc.start()

        startTime = time.time()

        # ALGO
        worst = antColonyAlg(data["g"], data["nbVehicules"])
        worstsFourmiShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramFourmiShared[ind] = peak / 10**6

        timeFourmiShared[ind] = time.time() - startTime

        if(doPrint): print("Found a result for ant colony", ind, ":", worst)

    def Recuit(ind, worstsRecuitShared, ramRecuitShared, timeRecuitShared, data, doPrint):
        if(doPrint): print("Calculating simulated annealing", ind, "(", len(data["g"]), ":", data["nbVehicules"], ")")

        tracemalloc.start()

        startTime = time.time()

        # ALGO
        path, worst = getBestRS(4, data["nbVehicules"], 0, data["g"])
        worstsRecuitShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramRecuitShared[ind] = peak / 10**6

        timeRecuitShared[ind] = time.time() - startTime

        if(doPrint): print("Found a result for simulated annealing", ind, ":", worst)
    def Google(ind, worstsGoogleShared, ramGoogleShared, timeGoogleShared, data, gmeta, doPrint):
        if(doPrint): print("Calculating Google with " + gmeta, ind, "(", len(data["g"]), ":", data["nbVehicules"], ")")

        tracemalloc.start()

        startTime = time.time()

        # ALGO
        paths, worst = googleORTools(data["g"], data["nbVehicules"], gmeta)
        worstsGoogleShared[ind] = worst

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ramGoogleShared[ind] = peak / 10**6

        timeGoogleShared[ind] = time.time() - startTime

        if(doPrint): print("Found a result for Google", ind, ":", worst)
    