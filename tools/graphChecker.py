def calcPathEfficiency(graph, paths, doPrint = True):
    nbVehicules = len(paths)
    size = len(graph)
    
    totLen = 0
    totLenVehicules = [0 for i in range(nbVehicules)]
    
    # Check data validity
    prefix = "[INVALID PATH]"
    for v in range(nbVehicules):
        if(paths[v][0] != paths[v][len(paths[v])-1]):
            print(prefix, "Path for vehicule", v, "does not return to starting point!")
    concatPaths = [j for i in paths for j in i]
    for i in range(size):
        if(i not in concatPaths):
            print(prefix, "The point", i, "is not taken by any vehicule!")
    if(len(concatPaths) > size + (len(paths)*2)-1):
        print(prefix, "Invalid path length! (Some points are taken multiple times?)")
        print("> Got", len(concatPaths), "expected", size + (len(paths)*2)-1)
    
    # Calculate path length
    for v in range(nbVehicules):
        for i in range(len(paths[v])):
            if(i+1 >= len(paths[v])):
                break
            current = paths[v][i]
            neighbour = paths[v][i+1]
            weight = graph[current][neighbour]
            totLen += weight
            totLenVehicules[v] += weight
    
    if(doPrint):
        print("Total weight:", totLen)
    if(doPrint):
        for i in range(nbVehicules): print(" - Weight for vehicule", i, ":", totLenVehicules[i])
    worst = max(totLenVehicules)
    worstIndex = totLenVehicules.index(worst)
    if(doPrint):
        print("Worst weight found for vehicule", worstIndex, "(", worst, ")")
    
    return (worst, worstIndex, totLenVehicules)