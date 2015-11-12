import csv
import math
from os import listdir
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook
import re
from matplotlib import collections  as mc

REarth = 6371. #Earth radius in kilometers
KmToMi = 0.621371

minLong = -74.2500
maxLong =  -73.693186
minLat  = 40.5064
maxLat  = 40.965864

#I bin the trips rather than represent them as individual points, otherwise the K-clustering will have a hard time:
#NLong = 200
#NLat  = 100
NLong = 40
NLat  = 40

dLat = (maxLat-minLat)/NLat
dLong = (maxLong-minLong)/NLong

minTripLengthKM = 5.

#The latitudes and longitudes of LGA and JFK, given as ranges:
LGALatMin  =  40.77
LGALatMax  =  40.784
LGALongMin = -73.89
LGALongMax = -73.855
JFKLatMin  =  40.6257
JFKLatMax  =  40.6537
JFKLongMin = -73.823
JFKLongMax = -73.735

#The distribution of trips, as 4 nests of lists:
dist = [[[[0. for i in range(0, NLong)] for j in range(0, NLat)] for k in range(0, NLong)] for l in range(0, NLat)]

#The distribution of trips only to (or from) LaGuardia and JFK:
distLGA = [[0. for i in range(0, NLong)] for j in range(0, NLat)]
distJFK = [[0. for i in range(0, NLong)] for j in range(0, NLat)]

#Finally, hourly distributions of trips between LaGuardia and JFK, and the hourly distribution of total driving time and distance:
distLGAToJFK = [0. for i in range(0, 24)]
distTimeEachHour = [0. for i in range(0, 24)]
distDistanceEachHour = [0. for i in range(0, 24)]

def binTrip(startLat, startLong, endLat, endLong):
    startLatBin = int(math.floor((startLat-minLat)/dLat))
    startLongBin = int(math.floor((startLong-minLong)/dLong))
    endLatBin = int(math.floor((endLat-minLat)/dLat))
    endLongBin = int(math.floor((endLong-minLong)/dLong))

    if (startLatBin>=0 and startLatBin<NLat and startLongBin>=0 and startLongBin<NLong and endLatBin>=0 and endLatBin<NLat and endLongBin>=0 and endLongBin<NLong):
        dist[startLatBin][startLongBin][endLatBin][endLongBin] += 1.

    return

def binTripToLGA(Lat, Long):
    LatBin = int(math.floor((Lat-minLat)/dLat))
    LongBin = int(math.floor((Long-minLong)/dLong))

    if (LatBin>=0 and LatBin<NLat and LongBin>=0 and LongBin<NLong):
        distLGA[LatBin][LongBin] += 1.

    return

def binTripToJFK(Lat, Long):
    LatBin = int(math.floor((Lat-minLat)/dLat))
    LongBin = int(math.floor((Long-minLong)/dLong))

    if (LatBin>=0 and LatBin<NLat and LongBin>=0 and LongBin<NLong):
        distJFK[LatBin][LongBin] += 1.

    return

#Provides an approximate measure of distance travelled, used to exclude trips which are short and best taken on the subway:
def distance(startLat, startLong, endLat, endLong):
    dx = (startLat-endLat)*(math.pi/180.)*REarth
    dy = (startLong-endLong)*(math.pi/180.)*math.sin(0.5*(startLat+endLat)*(math.pi/180.))

    return math.sqrt(dx*dx + dy*dy)

tripDataFiles = listdir('trip_data')

for name in tripDataFiles:
    with open('trip_data/'+name, 'rb') as csvfile:
        trips = csv.reader(csvfile)
        counter = 0
        for row in trips:
            counter += 1
            if counter>1:
                try:
                    hour = int(math.floor(float(row[-9].split()[1].split(':')[0])))
                except ValueError:
                    hour = -1
                try:
                    travelTime = float(row[-6])
                except ValueError:
                    travelTime = 0.
                try:
                    travelDistance = float(row[-5])
                except ValueError:
                    travelDistance = 0.
                try:
                    startLong = float(row[-4])
                except ValueError:
                    startLong = 0.
                try:
                    startLat = float(row[-3])
                except ValueError:
                    startLat = 0.
                try:
                    endLong = float(row[-2])
                except ValueError:
                    endLong = 0.
                try:
                    endLat = float(row[-1])
                except ValueError:
                    endLat = 0.
                ##Just some code that double-checked that travelDistance is in miles:
                #if(startLong != 0. and startLat != 0. and distance(startLat, startLong, endLat, endLong)*KmToMi > distance):
                #    print(travelDistance, distance(startLat, startLong, endLat, endLong)*KmToMi)

                if(hour >= 0 and hour < 24):
                    if(travelTime != 0. and travelDistance != 0.):
                        distTimeEachHour[hour] += travelTime
                        distDistanceEachHour[hour] += travelDistance
                    if((startLat >= LGALatMin and startLat <= LGALatMax and startLong >= LGALongMin and startLong <= LGALongMax
                        and endLat >= JFKLatMin and endLat <= JFKLatMax and endLong >= JFKLongMin and endLong <= JFKLongMax)
                       or (startLat >= JFKLatMin and startLat <= JFKLatMax and startLong >= JFKLongMin and startLong <= JFKLongMax
                        and endLat >= LGALatMin and endLat <= LGALatMax and endLong >= LGALongMin and endLong <= LGALongMax)):
                        distLGAToJFK[hour] += 1.

                if(startLong != 0. and startLat != 0. and endLong != 0. and endLat != 0.):
                    if(distance(startLat, startLong, endLat, endLong)>minTripLengthKM):
                        binTrip(startLat, startLong, endLat, endLong)

                if(startLat >= LGALatMin and startLat <= LGALatMax and startLong >= LGALongMin and startLong <= LGALongMax):
                    binTripToLGA(endLat, endLong)
                if(endLat >= LGALatMin and endLat <= LGALatMax and endLong >= LGALongMin and endLong <= LGALongMax):
                    binTripToLGA(startLat, startLong)

                if(startLat >= JFKLatMin and startLat <= JFKLatMax and startLong >= JFKLongMin and startLong <= JFKLongMax):
                    binTripToJFK(endLat, endLong)
                if(endLat >= JFKLatMin and endLat <= JFKLatMax and endLong >= JFKLongMin and endLong <= JFKLongMax):
                    binTripToJFK(startLat, startLong)

averageMPH = []

for i in range(0, 24):
    distLGAToJFK[i] /= 365.
    averageMPH.append(3600.*distDistanceEachHour[i]/distTimeEachHour[i])

#With the data binned, we find the most heavily weighted bins:
listOfCells = []
for i in range(0, NLat):
    startLat = minLat+(i+0.5)*dLat
    for j in range(0, NLong):
        startLong = minLong+(j+0.5)*dLong
        for k in range(0, NLat):
            endLat = minLat+(k+0.5)*dLat
            for l in range(0, NLong):
                endLong = minLong+(l+0.5)*dLong
                if(dist[i][j][k][l] > 0.):
                    listOfCells.append([startLat, startLong, endLat, endLong, dist[i][j][k][l]])

def sorter(lst):
    return lst[-1]

sortedList = sorted(listOfCells, key=sorter, reverse=True)

NYCFile = cbook.get_sample_data('/home/youngc/dataIncubator/nyc.jpg') #I hope this is fair use. I got it from http://www.nyctourist.com/map1.htm
img = imread(NYCFile)

#for lst in sortedList:
#
#    plt.imshow(img, zorder=0, extent=[-74.28, -73.675, 40.468, 40.945])
#    plt.scatter([lst[1], lst[3]],[lst[0], lst[2]])
#    plt.show()

#K-means clustering of the trips to (or from) LGA and JFK:
NClustersLGA = 10
NClustersJFK = 10
KClustersLGA = []
KClustersJFK = []

for i in range(0, NClustersLGA):
    KClustersLGA.append([randint(0, NLat), randint(0, NLong)])
for i in range(0, NClustersJFK):
    KClustersJFK.append([randint(0, NLat), randint(0, NLong)])

NewKClustersLGA = []
for i in range(0, NClustersLGA):
    NewKClustersLGA.append([0., 0.])
NewKClustersJFK = []
for i in range(0, NClustersJFK):
    NewKClustersJFK.append([0., 0.])

WhichClusterLGA = [[0 for i in range(0, NLong)] for j in range(0, NLat)]
WhichClusterJFK = [[0 for i in range(0, NLong)] for j in range(0, NLat)]

def ClustersUnchangedLGA():
    metric = 0.
    for i in range(0, NClustersLGA):
        for j in range(0, 2):
            metric += abs(NewKClustersLGA[i][j]-KClustersLGA[i][j])
    print('metric =', metric)
    if metric<1e-5:
        return True

def ClustersUnchangedJFK():
    metric = 0.
    for i in range(0, NClustersJFK):
        for j in range(0, 2):
            metric += abs(NewKClustersJFK[i][j]-KClustersJFK[i][j])
    print('metric =', metric)
    if metric<1e-5:
        return True

unchanged = False
while(not unchanged):
    #First, determine to which cluster each chunk of the distribution belongs:
    for i in range(0, NLat):
        for j in range(0, NLong):
            minDistance2 = (i-KClustersLGA[0][0])**2 + (j-KClustersLGA[0][1])**2
            for clusterI in range(1, NClustersLGA):
                distance2 = (i-KClustersLGA[clusterI][0])**2 + (j-KClustersLGA[clusterI][1])**2
                if distance2 < minDistance2:
                    WhichClusterLGA[i][j] = int(clusterI)
                    minDistance2 = distance2
    #Next, re-center the means based on a weighted average of the clusters' members:
    meanNormLGA = [0. for i in range(0, NClustersLGA)]
    for i in range(0, NClustersLGA):
        for j in range(0, 2):
            NewKClustersLGA[i][j] = 0.
    for i in range(0, NLat):
        for j in range(0, NLong):
            meanNormLGA[WhichClusterLGA[i][j]] += distLGA[i][j]
            spot = [i, j]
            for m in range(0, 2):
                NewKClustersLGA[WhichClusterLGA[i][j]][m] += distLGA[i][j]*spot[m]
    for i in range(0, NClustersLGA):
        for j in range(0, 2):
            if meanNormLGA[i] > 0.:
                NewKClustersLGA[i][j] = NewKClustersLGA[i][j]/meanNormLGA[i]

    unchanged = ClustersUnchangedLGA()
    for i in range(0, NClustersLGA):
        for j in range(0, 2):
            #Only update of meanNorm[i] > 0.:
            if(meanNormLGA[i] > 0.):
                KClustersLGA[i][j] = NewKClustersLGA[i][j]

unchanged = False
while(not unchanged):
    #First, determine to which cluster each chunk of the distribution belongs:
    for i in range(0, NLat):
        for j in range(0, NLong):
            minDistance2 = (i-KClustersJFK[0][0])**2 + (j-KClustersJFK[0][1])**2
            for clusterI in range(1, NClustersJFK):
                distance2 = (i-KClustersJFK[clusterI][0])**2 + (j-KClustersJFK[clusterI][1])**2
                if distance2 < minDistance2:
                    WhichClusterJFK[i][j] = int(clusterI)
                    minDistance2 = distance2
    #Next, re-center the means based on a weighted average of the clusters' members:
    meanNormJFK = [0. for i in range(0, NClustersJFK)]
    for i in range(0, NClustersJFK):
        for j in range(0, 2):
            NewKClustersJFK[i][j] = 0.
    for i in range(0, NLat):
        for j in range(0, NLong):
            meanNormJFK[WhichClusterJFK[i][j]] += distJFK[i][j]
            spot = [i, j]
            for m in range(0, 2):
                NewKClustersJFK[WhichClusterJFK[i][j]][m] += distJFK[i][j]*spot[m]
    for i in range(0, NClustersJFK):
        for j in range(0, 2):
            if meanNormJFK[i] > 0.:
                NewKClustersJFK[i][j] = NewKClustersJFK[i][j]/meanNormJFK[i]

    unchanged = ClustersUnchangedJFK()
    for i in range(0, NClustersJFK):
        for j in range(0, 2):
            #Only update of meanNorm[i] > 0.:
            if(meanNormJFK[i] > 0.):
                KClustersJFK[i][j] = NewKClustersJFK[i][j]
