import numpy
import math
def convertTableLin(arr):
    minimumLine = list(arr.min(axis=1))
    k = 0
    column = list(arr.columns.values)
    index = list(arr.index.values)
    for i in index:
        for j in column:
            a = minimumLine[k]
            b = arr[j][i]
            arr.set_value(i, j, b - a)
        k += 1


def convertTableCol(arr):
    minimumLine = list(arr.min(axis=0))
    k = 0
    column = list(arr.columns.values)
    index = list(arr.index.values)
    for i in column:
        for j in index:
            a = minimumLine[k]
            b = arr[i][j]
            arr.set_value(j, i, b - a)
        k += 1

def getMaxWay(arr):
    maxTotalWay = []
    maxTotal = 0
    column = list(arr.columns.values)
    index = list(arr.index.values)
    for i in index:
        for j in column:
            if round(arr[j][i]) == 0:
                line = arr.loc[i]
                newLine = line.drop(j)
                minLine = min(newLine)
                col = arr[j]
                newColumn = col.drop(i)
                minColumn = min(newColumn)
                if minLine + minColumn >= maxTotal:
                    maxTotal = minLine + minColumn
                    maxTotalWay = [i, j]
    return maxTotal, maxTotalWay
