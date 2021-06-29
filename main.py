import matplotlib.pyplot as plt
from stats.stats import GetStats, showStats
from graphGeneration import randomDataGenerator
from algorithms.tabu import tabu
from algorithms.google import googleORTools
from graphChecker import calcPathEfficiency
from tabouletOGM.algogenOGM import geneticPathFinderOGM

import numpy as np

import pandas as pd

from algorithms.fourmi import antColonyAlg

# ["tabou", "genetic", "tabouOGM", "fourmi", "recuit"]

minGraphSize = 5
maxGraphSize = 35
paddingGraph = 5

# Tabou VS Google Tabou
# https://developers.google.com/optimization/routing/routing_options
# https://developers.google.com/optimization/routing/vrp
# https://developers.google.com/optimization/routing/tsp#search_strategy
# https://console.cloud.google.com/google/maps-apis/api-list?project=vrpproject-318216
x, dataset = GetStats(minGraphSize, maxGraphSize, paddingGraph, ["recuit", "google"], "SIMULATED_ANNEALING")
showStats(x, dataset, maxGraphSize, "worst")
showStats(x, dataset, maxGraphSize, "ram")
showStats(x, dataset, maxGraphSize, "time")

# Recuit VS Google Recuit
# x, dataset = GetStats(minGraphSize, maxGraphSize, paddingGraph, ["tabou", "google"], "TABU_SEARCH")
# showStats(x, dataset, maxGraphSize, "worst")
# showStats(x, dataset, maxGraphSize, "ram")
# showStats(x, dataset, maxGraphSize, "time")

# (bestPath, bestDistance, totalLength) = tabu(graph, 6, 1)
# print(bestPath)
# calcPathEfficiency(graph, bestPath, True)

# graph = np.multiply(randomDataGenerator(1, 5, False), 100)
# graphElLen = 100000
# graph = randomDataGenerator(1, 10, False, graphElLen)
# nbVehicules = 2

# print(graph)
# print(pd.DataFrame(graph))

# mutationRate = 1
# populationSize = 40
# maxGen = 5000
# maxIteration = 1

# print("Tabou", calcPathEfficiency(graph, tabu(graph, nbVehicules, 100)[0], False)[0] / graphElLen)

# worst = geneticPathFinderOGM(mutationRate, len(graph), nbVehicules, maxGen, graph, 0, False)
# print("Taboulé OGM", worst / graphElLen)

# # print("GOOGLE", googleORTools(graph, nbVehicules)[1] / graphElLen)
# print("GOOGLE TABOU", googleORTools(graph, nbVehicules, "TABU_SEARCH")[1] / graphElLen)
# print("GOOGLE RECUIT", googleORTools(graph, nbVehicules, "SIMULATED_ANNEALING")[1] / graphElLen)





























