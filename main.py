import matplotlib.pyplot as plt
from stats.stats import GetStats, showStats
from graphGeneration import randomDataGenerator
from algorithms.tabu import tabu
from graphChecker import calcPathEfficiency

minGraphSize = 20
maxGraphSize = 150
paddingGraph = 20

# Retrieve stats
x, dataset = GetStats(minGraphSize, maxGraphSize, paddingGraph, ["tabou", "genetic", "tabouOGM"])
showStats(x, dataset, maxGraphSize, "worst")
showStats(x, dataset, maxGraphSize, "ram")
showStats(x, dataset, maxGraphSize, "time")