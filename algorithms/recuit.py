import random, copy, numpy as np, math, matplotlib.pyplot as plt, time
#data = randomDataGenerator(1, 23, False)
#data = [[0, 0.039, 0.04, 0.043, 0.042, 0.044, 0.044, 0.047, 0.047, 0.052], [0.039, 0, 0.049, 0.042, 0.04, 0.037, 0.044, 0.047, 0.049, 0.046], [0.04, 0.049, 0, 0.038, 0.04, 0.041, 0.045, 0.044, 0.038, 0.043], [0.043, 0.042, 0.038, 0, 0.048, 0.048, 0.04, 0.045, 0.043, 0.044], [0.042, 0.04, 0.04, 0.048, 0, 0.053, 0.038, 0.041, 0.043, 0.046], [0.044, 0.037, 0.041, 0.048, 0.053, 0, 0.052, 0.045, 0.052, 0.044], [0.044, 0.044, 0.045, 0.04, 0.038, 0.052, 0, 0.048, 0.038, 0.048], [0.047, 0.047, 0.044, 0.045, 0.041, 0.045, 0.048, 0, 0.051, 0.05], [0.047, 0.049, 0.038, 0.043, 0.043, 0.052, 0.038, 0.051, 0, 0.048], [0.052, 0.046, 0.043, 0.044, 0.046, 0.044, 0.048, 0.05, 0.048, 0]]
#print(data)
# Permet la génération d'un tour random de point
def generate_random_tour(cities):
    tour = random.sample(range(len(cities)), k=len(cities))
    newTour = tour
    newTour.append(tour[0])
    return newTour
def get_best_random_tour(cities):
    generate_tour = generate_random_tour(cities)
    distanceTour = distance(generate_tour, cities)
    # iteration pour générer des tours plus court que celui créé précédement
    for i in range(100000):
        newTour = generate_random_tour(cities)
        newDistance = distance(newTour, cities)
        if newDistance < distanceTour:
            distanceTour = newDistance
            generate_tour = copy.copy(newTour)
    return generate_tour

def distance(tour, cities):
    maxDist = 0
    for i in range(len(tour)-1):
        maxDist += cities[tour[i]][tour[i+1]]
    return maxDist

def distance_between(tour, cities, i, j):
    distanceBetween = 0
    for k in [i,j-1]:
        distanceBetween += cities[tour[k]][tour[k+1]]
    return distanceBetween;
def distanceNext(tour, cities, index):
    return cities[tour[index % len(tour)]][tour[(index+1) % len(tour)]]
def temperature_noninteractive(number):
    return np.logspace(0,5,number)[::-1]
        
def generatePointList(cities):
    point = []
    for i in range(len(cities)):
        point.append([np.random.randint(0, (i+1)*(i+1)), np.random.randint(0, (i+1)*(i+1))])
    return point

def arrayloop(arr, start, end):
    arr_len = len(arr)
    ret = []
    if start > end:
        nb_elements = arr_len - start
        nb_elements += end
    else:
        if end+1 == arr_len:
            return arr[start:(end+1)]
        else:
            return arr[start:(end+1) % arr_len]
    
    for i in range(nb_elements):
        ret.append(arr[(start + i) % arr_len])

    ret.append(arr[(start + nb_elements) % arr_len])
    return ret

def RecuitSimule(cities, temps):
    iteration = 0
    tour = get_best_random_tour(cities)
    sizeCities = len(cities)
    lowTour = None
    lowDistance = np.inf
    try:
        for temp in temps(50000):
            iteration += 1
            [i, j] = sorted(random.sample(range(sizeCities),2))
            newTour = tour[:i] + tour[j:j+1] + tour[i+1:j] + tour[i:i+1] + tour[j+1:-1]
            newTour.append(newTour[0])
            #print(i, j)
            oldDist = distance_between(tour, cities, i, j)
            newDist = distance_between(newTour, cities, i, j)
            newTourDist = distance(newTour, cities)
            if math.exp((oldDist - newDist) / temp) > 1:
                tour = copy.copy(newTour)
            if newTourDist < lowDistance:
                lowDistance = newTourDist
                lowTour = copy.copy(tour)

            if(iteration % 500000 == 0):
                tempsPasse = time.time() - time_start
                print("Iteration: " + str(iteration))
                print("Elapsed: {:10.4f}s".format(tempsPasse))
                print("Nouvelle distance: {:10.4f}".format(newTourDist))
                print("Meilleur distance: {:10.4f}".format(lowDistance))
                print("Temperature: " + str(temp))
                print("======")
                #live_plot(lowTour, cities)
    except (RuntimeError, TypeError, NameError):
        print(RuntimeError, TypeError, NameError)
    if lowTour == None:
        return tour
    else:
        return lowTour
    
def generateCamionPath(bestPath, tourCamion, k, depot, data):
    firstCity = bestPath.index(depot)
    positionNextCity = 0
    resultDistance = distance(tourCamion, data)
    camionTour = copy.copy(bestPath)
    for truck in range(k-1):
        distance_cumulee = 0
        oneValue = 0
        while distance_cumulee < (resultDistance / k):
            curr = camionTour[(firstCity + positionNextCity) % len(camionTour)]
            depotTour = copy.copy(camionTour)
            depotTour.insert((firstCity + positionNextCity) % len(depotTour), depot)
            distanceNextVar = distanceNext(camionTour, data, firstCity + positionNextCity)
            distanceNextVarDepot = distanceNext(depotTour, data, firstCity + positionNextCity)
            depotDist = distance_cumulee + distanceNextVarDepot
            if depotDist >= (resultDistance / k):
                if oneValue == 1:
                    positionNextCity += 1
                distance_cumulee += distanceNextVarDepot
            else:
                distance_cumulee += distanceNextVar
                positionNextCity += 1
                oneValue += 1
            #print("distcum: " + str(distance_cumulee) + "distmax: " + str((resultDistance / k)))
        if (firstCity + positionNextCity) % len(camionTour) != 0 and (firstCity + positionNextCity) != len(camionTour):
            camionTour.insert((firstCity + positionNextCity+1) % len(camionTour), depot)
        elif camionTour[(firstCity + positionNextCity) % len(camionTour) + 1] != depot:
            camionTour.insert((firstCity + positionNextCity+1) % len(camionTour), depot)
        positionNextCity += 1
        #print("camionTour: " + str(camionTour))
    return (camionTour)

def generateTourCamion(tourCamion, k, depot, data):
    camionTour = generateCamionPath(tourCamion, tourCamion, k, depot, data)
    for i in range(2):
        camionTour = generateCamionPath(tourCamion, camionTour, k, depot, data)
    zero_positions = [i for i, value in enumerate(camionTour) if value == depot]
    number_zeros = len(zero_positions)
    truck_tour = []
    for zero_pos_i in range(len(zero_positions)):
        tour_start_index = zero_positions[zero_pos_i]
        tour_end_index = zero_positions[(zero_pos_i + 1) % number_zeros]
        truck_tour.append(arrayloop(camionTour, tour_start_index, tour_end_index))
    return truck_tour
    
        
# def makeGraph(truck_tour):
#     plt.ion()
#     plt.show()
#     cities_x = []
#     cities_y = []
#     plt.clf()
#     for j in range(len(truck_tour)):
#         for i in range(len(truck_tour[j])+1):
#             cities_x.append(pointList[truck_tour[j][i % len(truck_tour[j])]][0])
#             cities_y.append(pointList[truck_tour[j][i % len(truck_tour[j])]][1])
#         print(cities_y)
#         plt.plot(cities_x, cities_y, label="camion : " + str(j+1) + " distance : "+ str(distance(truck_tour[j], data)))
#     plt.legend()
    # plt.pause(0.1)

def getBestRS(iteration, k, depot, data):
    pointList = generatePointList(data)

    bestPath = []
    camionPath = []
    RS = RecuitSimule(data, temperature_noninteractive)
    RS.pop()
    bestPath = copy.copy(RS)
    CamionTourHigh = 10000
    for i in range(iteration):
        tempsPasse = time.time() - time_start
        for j in range(iteration):
            RS = RecuitSimule(data, temperature_noninteractive)
            RS.pop()
            if k > 1:
                generatePathCamion = copy.copy(generateTourCamion(RS, k, depot, data))
                if len(camionPath) > 0:
                    badValue = 0
                    for p in range(len(generatePathCamion)):
                        if distance(generatePathCamion[p], data) > badValue:
                            badValue = distance(generatePathCamion[p], data)
                    if badValue < CamionTourHigh:
                        camionPath = []
                        camionPath = copy.copy(generatePathCamion)
                        CamionTourHigh = badValue
                        bestPath = copy.copy(RS)
                else:
                    camionPath = []
                    camionPath = generatePathCamion
            else:
                badValue = distance(RS, data)
                if CamionTourHigh > badValue:
                    CamionTourHigh = badValue
        # print("====================")
        # print("Iteration: " + str(i+1) + "/" +str(iteration))
        # print("Elapsed: {:10.4f}s".format(tempsPasse))
        # print("BestPath: " + str(bestPath))
        # print("CamionTourHigh: " + str(CamionTourHigh))
        # print("====================")            
        
    return (camionPath, CamionTourHigh)


time_start = time.time()
#result = RecuitSimule(data, temperature_noninteractive)
# (result, bigPath) = getBestRS(6, 7, 0)
# makeGraph(result)
# print(result, bigPath)
#generateTourCamion(result, 2, 0)