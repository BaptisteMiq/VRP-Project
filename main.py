import matplotlib.pyplot as plt
from stats.stats import GetStats, showStats
from graphGeneration import randomDataGenerator
from algorithms.tabu import tabu
from graphChecker import calcPathEfficiency
from tabouletOGM.algogenOGM import geneticPathFinderOGM

from algorithms.fourmi import antColonyAlg

# ["tabou", "genetic", "tabouOGM", "fourmi", "recuit"]

minGraphSize = 4
maxGraphSize = 80
paddingGraph = 10

# Retrieve stats
x, dataset = GetStats(minGraphSize, maxGraphSize, paddingGraph, ["tabou", "genetic", "tabouOGM", "fourmi", "recuit"])
showStats(x, dataset, maxGraphSize, "worst")
showStats(x, dataset, maxGraphSize, "ram")
showStats(x, dataset, maxGraphSize, "time")

# graph = randomDataGenerator(1, 27, False)
# (bestPath, bestDistance, totalLength) = tabu(graph, 6, 1)
# print(bestPath)
# calcPathEfficiency(graph, bestPath, True)

# mutationRate = 1
# populationSize = 40
# maxGen = 5000
# maxIteration = 1
# position = 0
# nbCamion = 6

#pop = Population(mutationRate,populationSize, nbCamion, graph, position, True)
# pop.tabuADNGenerator()

# worst = geneticPathFinderOGM(mutationRate, len(graph), 3, maxGen, graph, 0, False)
# print("resultat", worst)
# print(calcPathEfficiency(graph, tabu(graph, 3, 100)[0], True))