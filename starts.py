from genetic import geneticPathFinder

class StartAlgorithm:
    def Genetic(ind, worstsGen, data):
        print("Starting subprocess", ind)

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
        worstsGen[ind] = worst

        print("Found a result for ind", ind, ":", worst)