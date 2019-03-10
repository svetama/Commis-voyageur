import itertools
import numpy
import math
import pandas as pd
import time
from function import *

nCity = 5
costMatrix = [[math.inf, 10, 25, 25, 10], [1, math.inf, 10, 15, 2], [8, 9, math.inf, 20, 10],
              [14, 10, 24, math.inf, 15], [10, 8, 25, 27, math.inf]]
timeForChange = 1
timeForWork = 4


start_time = time.time()

# Floyd algorithm
matrixShortcut = numpy.ones((nCity, nCity)) * (-1)
matrixShortcut = matrixShortcut.astype(int)
k = 0
while k <= nCity - 1:
    i = 0
    while i <= nCity - 1:
        j = 0
        while j <= nCity - 1:
            if (costMatrix[k][i] + costMatrix[j][k] + timeForChange < costMatrix[j][i]) and (costMatrix[j][i] != math.inf):
                costMatrix[j][i] = costMatrix[k][i] + costMatrix[j][k] + timeForChange
                matrixShortcut[j][i] = k
            j += 1
        i += 1
    k += 1

# modification of matrix into DataFrame
listCity = [0]
for i in range(1, nCity):
    listCity.append(i)
matrixWithHeaders = pd.DataFrame(costMatrix, index=[_ for _ in listCity], columns=[_ for _ in listCity])

# basics
workingWay = []
excludeWay = []
matrixSize = nCity
valuation = 0
listShortcut = []

# first iteration
minimumLine = matrixWithHeaders.min(axis=1)
valuation += numpy.sum(minimumLine)
convertTableLin(matrixWithHeaders)
minimumCol = matrixWithHeaders.min(axis=0)
valuation += numpy.sum(minimumCol)
convertTableCol(matrixWithHeaders)

while matrixSize != 2:
    # создание списка звеньев с нулями, поиск максимальной суммы минимумов
    maxTotal, maxTotalWay = getMaxWay(matrixWithHeaders)

    departure = maxTotalWay[0]
    arrival = maxTotalWay[1]

    # развитие ветки без данного звена
    matrixWithout = matrixWithHeaders.copy()
    matrixWithout.set_value(departure, arrival, math.inf)

    minimumLine = matrixWithout.min(axis=1).copy()
    valuationWithout = valuation + numpy.sum(minimumLine)
    convertTableLin(matrixWithout)
    minimumCol = matrixWithout.min(axis=0)
    valuationWithout += numpy.sum(minimumCol)
    convertTableCol(matrixWithout)

    # развитие ветки с данным звеном
    matrixWith = matrixWithHeaders.copy()
    matrixWith = matrixWith.drop(arrival, axis=1)
    matrixWith = matrixWith.drop(departure, axis=0)
    index = list(matrixWith.index.values)
    columns = list(matrixWith.columns.values)
    maxLine = list(matrixWith.max(axis=1))
    maxCol = list(matrixWith.max(axis=0))
    stepI = 0
    for i in maxLine:
        stepJ = 0
        for j in maxCol:
            if i != math.inf and j != math.inf:
                matrixWith.iat[stepI, stepJ] = math.inf
            stepJ += 1
        stepI += 1

    minimumLine = matrixWith.min(axis=1).copy()
    valuationWith = valuation + numpy.sum(minimumLine)
    convertTableLin(matrixWith)
    minimumCol = matrixWith.min(axis=0)
    valuationWith += numpy.sum(minimumCol)
    convertTableCol(matrixWith)

    if valuationWith >= valuationWithout:
        valuation = valuationWithout.copy()
        matrixWithHeaders = matrixWithout.copy()
        excludeWay.append(maxTotalWay)
    else:
        valuation = valuationWith.copy()
        matrixWithHeaders = matrixWith.copy()
        workingWay.append(maxTotalWay)
        listShortcut.append(matrixShortcut[maxTotalWay[0]][maxTotalWay[1]])
        matrixSize -= 1

column = list(matrixWithHeaders.columns.values)
index = list(matrixWithHeaders.index.values)
for i in column:
    for j in index:
        if matrixWithHeaders[i][j] != math.inf:
            workingWay.append([j, i])
            listShortcut.append(matrixShortcut[j][i])
            valuation += matrixWithHeaders[i][j]

wayDraft = []
shortcutDraft = []
i = 0
p = range(len(workingWay))
previousEnd = 0
while len(wayDraft) < len(workingWay):
    for i in range(len(workingWay)):
        if workingWay[i][0] == previousEnd:
            wayDraft.append(workingWay[i])
            previousEnd = workingWay[i][1]
            shortcutDraft.append(listShortcut[i])
            if len(wayDraft) == len(workingWay):
                break

wayFinal = []
i = 0
while i <= len(shortcutDraft) - 1:
    if shortcutDraft[i] == -1:
        wayFinal.append(wayDraft[i])
    else:
        wayRound1 = [wayDraft[i][0], shortcutDraft[i]]
        wayRound2 = [shortcutDraft[i], wayDraft[i][1]]
        wayFinal.append(wayRound1)
        wayFinal.append(wayRound2)
    i += 1

print('The shortest way: ', wayFinal)
print('Time for travel: ', valuation)
print('Time for work: ', nCity * timeForWork)
print('Total time: ', valuation + nCity * timeForWork)
print("The program has been working for --- %s seconds ---" % (time.time() - start_time))
