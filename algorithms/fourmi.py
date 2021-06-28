## Partie des Imports
import numpy as np
from random import random
from random import randrange
from random import shuffle
from statistics import mean
import matplotlib.pyplot as plt

# antColonyAlg - Algorithme de colonies de fourmis
def antColonyAlg(dataPondArray, nombreCamions):

    ## Définition des variables
    
    dataArray= list(dataPondArray)
    dataArray = np.array(dataArray)
    nbVilles = dataArray[0].size

    nbInteration = 50
    evaporation = 0.5
    nbFourmis = 50
    nbCamions = nombreCamions

    villeOr = 0
    nbVillesOBJ = []
    for eachValue in range(nbVilles):
        nbVillesOBJ.append(eachValue)
    nbVillesOBJ = list(nbVillesOBJ)
    nbVillesOBJ.remove(0)
    shuffle(nbVillesOBJ)

    allCity = []
    for countVille in range(nbVilles):
         allCity.append(countVille) 

    pheromone= dataArray.copy()
    pheromone.fill(0)

    wrPondLastList = []
    bestPondList = []
    moyBestPondList = []

    for ite in range(nbInteration):
        # Variables de chaque itération
        nbVillesOBJCop = nbVillesOBJ.copy()
        visibilite= dataArray.copy()


        for test in range(nbCamions):
            # Variables de chaque trajet de livraison
            bestRout = []
            bestPond = 1000   
            actOBJList = nbVillesOBJCop[:int(nbVilles/nbCamions)]

            for four in range(nbFourmis):
                # Variables de chaque fourmi
                actPos = villeOr
                alrdPass = [villeOr]
                notPass = []
                actOBJ = villeOr
                pond = 0
                AntTravelOBJ = actOBJList.copy()
                temp_visibility = visibilite.copy()                 
                devLVL = ""
                route = []
                route.append(villeOr)

                # Pour chaque villes
                for nbInte in range(nbVilles): 
                    wayProbaOR= dataArray[actPos].copy()
                    wayProbaOR.fill(0)


                    # Termine le trajet si tour complet effectué
                    if int(actPos) == villeOr and nbInte != 0 and not AntTravelOBJ:
                        break


                    if not AntTravelOBJ:
                        # Termine la boucle si liste objectif vide
                        actOBJ = villeOr
                    else:
                        # Empèche de boucler sur la position actuelle
                        temp_visibility[:,actPos] = 0

                        # Met en forme la liste des probabilité de trajets
                        for x in range(nbVilles):
                            wayProbaOR=np.multiply((1-temp_visibility[actPos])+1,pheromone[actPos]+1)
                        for x in range(len(wayProbaOR)):
                            if wayProbaOR[x] == 2:
                                wayProbaOR[x] = 0
                        wayProba  = wayProbaOR.copy()

                        # Détermine liste des ville non traversés
                        setA = set(allCity)
                        setB = set(alrdPass)
                        cityNPass = list(setA - setB)                

                        # Détermine déviance
                        deviance = np.random.random_sample()
                        deviance = deviance + 1

                        # Détermine trajet avec déviance
                        if deviance > mean(wayProba):
                            #print("deviance:" + str(deviance))
                            randdevpos = randrange(len(AntTravelOBJ))
                            actOBJ = AntTravelOBJ[randdevpos]
                            devLVL = devLVL + "*"
                        else:

                            # Détermine trajet avec le plus de phéromones
                            wayCho = list(wayProba.copy())
                            calcNewPos = wayCho.index(max(wayCho))
                            while calcNewPos not in AntTravelOBJ:
                                if max(wayCho) != 0:
                                    wayCho.remove(max(wayCho))
                                    calcNewPos = wayCho.index(max(wayCho))
                                else: 
                                    calcNewPos = AntTravelOBJ[0]
                            actOBJ = int(calcNewPos)
                            
                    # met à jours:  pondérations, position actuelle, route, point de passage traversés
                    pond = pond + dataArray[actPos][actOBJ]
                    actPos = actOBJ            
                    route.append(actPos)
                    alrdPass.append(actPos)

                    # Enlève l'objectif atteint si présent dans la liste des objectifs
                    if actPos in AntTravelOBJ : 
                        AntTravelOBJ.remove(actPos)                

                # Enregistre trajet si plus optimisé
                if bestPond > pond:
                    bestPond = pond
                    bestRout = route          

            # Enregistre trajet si plus optimisé
            bestPondList.append(bestPond)
            moyBestPondList.append(mean(bestPondList))

            # Si dernière itération, enregistrer trajets
            if ite == nbInteration-1:  
                wrPondLastList.append(bestPond)

            # Gestion des phéromsones
            pheromone = (1-evaporation)*pheromone
            #pheToAdd = (1/(pond))
            if bestPond <= np.quantile(bestPondList, 0.40):
                pheToAdd = 0.8  

            # Ajout des phéromones  
            for countBR in range(len(bestRout)):
                if countBR <= len(bestRout): 
                    if countBR+1 <  len(bestRout):
                        if bestRout[countBR] < bestRout[countBR+1]:
                            pheromone[int(bestRout[countBR])][int(bestRout[countBR+1])] = pheromone[int(bestRout[countBR])][int(bestRout[countBR+1])] + pheToAdd
                        else: 
                            pheromone[int(bestRout[countBR+1])][int(bestRout[countBR])] = pheromone[int(bestRout[countBR+1])][int(bestRout[countBR])] + pheToAdd            

            # Supprime point de passage traversés
            actOBJListCop = actOBJList.copy()
            for OBJPassed in range(len(actOBJList)):
                nbVillesOBJCop.remove(actOBJList[OBJPassed])

                
    # plt.plot(bestPondList)
    # plt.plot(moyBestPondList)
    # plt.show()
    
    return max(wrPondLastList)