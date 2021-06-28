# from graphGeneration import randomDataGenerator
from graphChecker import calcPathEfficiency

def tabu(graph, nbVehicules, nbIter, startPoint):
    initGraph = graph
    #startPoint = 0
    
    # Init tabou list (will store a path between 2 points)
    tabuList = [[] for i in range(nbVehicules)]
    maxTabuListSize = 50
    
    bestPathIteration = {}
        
    for it in range(nbIter):
        
        currentElements = [startPoint] * nbVehicules
        bestPaths = [[startPoint] for i in range(nbVehicules)]
        bestDistances = [[] for i in range(nbVehicules)]
        visited = [startPoint]
        
        totLens = [0] * nbVehicules
        totPoints = len(graph)
        
        prematurateEnd = False
        
        while len(visited) < len(graph) and not prematurateEnd:
            #print(len(visited), len(graph))

            # Loop for every vehicule
            for v in range(nbVehicules):

                if(len(visited) >= len(graph)):
                    break

                # Worst case
                bestDistance = 9999
                bestNeighbour = startPoint

                # Search nearest neighbour
                for j in range(totPoints):
                    # Check if the path is not used (including other vehicules) + Check if path exists in tabu
                    if(currentElements[v] != j and j not in visited and (currentElements[v], j) not in tabuList[v]):
                        neighbour = graph[currentElements[v]][j]
                        if(neighbour <= bestDistance):
                            bestDistance = neighbour
                            bestNeighbour = j
                            tabuList[v].append((currentElements[v], j))
                            if(len(tabuList[v]) > maxTabuListSize):
                                tabuList[v].pop(0)

                # Could not find a solution => All combinaisons in tabou have been tried
                if(bestNeighbour == startPoint):
                    #print("NO SOLUTION", (currentElements[v], j))
                    # Search nearest neighbour
                    for j in range(totPoints):
                        # Check if the path is not used (including other vehicules) + Check if path exists in tabu
                        if(currentElements[v] != j and j not in visited):
                            neighbour = graph[currentElements[v]][j]
                            if(neighbour <= bestDistance):
                                bestDistance = neighbour
                                bestNeighbour = j

                bestPaths[v].append(bestNeighbour)
                visited.append(bestNeighbour)
                currentElements[v] = bestNeighbour
                totLens[v] += bestDistance
                bestDistances[v].append(bestDistance)

        for v in range(nbVehicules):
            # Return to start point
            bestPaths[v].append(startPoint)
            totLens[v] += graph[currentElements[v]][startPoint]
            bestDistances[v].append(graph[currentElements[v]][startPoint])
            
        worst, worstIndex, tot = calcPathEfficiency(initGraph, bestPaths, False)
        #print("ITER ", it, worst)
        if bestPathIteration.get("worst") is None or worst < bestPathIteration["worst"]:
            #print("New best for it", it, worst)
            bestPathIteration = {
                "bestPaths": bestPaths,
                "bestDistances": bestDistances,
                "totLens": totLens,
                "worst": worst
            }

    #print(tabuList)
    print(bestPathIteration["worst"])

    resultPath = list()
    for i, o in enumerate(bestPathIteration["bestPaths"]):
        for y in range(len(o)-1):
            resultPath.append(o[y])
    resultPath.append(startPoint)
    
    return resultPath

# graph = randomDataGenerator(1, 200, False)
# (bestPath, bestDistance, totalLength) = tabu(graph, 6, 10)