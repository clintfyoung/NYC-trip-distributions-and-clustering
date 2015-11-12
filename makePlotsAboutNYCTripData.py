import math
from os import listdir
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.cbook as cbook
import re
from matplotlib import collections  as mc

NYCFile = cbook.get_sample_data('/home/youngc/dataIncubator/nyc.jpg') #I hope this is fair use. I got it from http://www.nyctourist.com/map1.htm
img = imread(NYCFile)
"""
for counter in range(1, 20):
    lst = sortedList[counter-1]
    fig = plt.figure()
    #fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    if counter == 1:
        title = 'Most popular taxi trip in 2013'
    elif counter%10 == 1:
        title = str(counter)+'st most popular taxi trip in 2013'
    elif counter%10 == 2:
        title = str(counter)+'nd most popular taxi trip in 2013'
    elif counter%10 == 3:
        title = str(counter)+'rd most popular taxi trip in 2013'
    else:
        title = str(counter)+'th most popular taxi trip in 2013'

    ax.set_title(title)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    plt.imshow(img, zorder=0, extent=[-74.28, -73.675, 40.468, 40.945])
    start = plt.scatter([lst[1]], [lst[0]], s=40, color='b', marker = 'x')
    end = plt.scatter([lst[3]], [lst[2]], s=40, color='r', marker = 'o')
    plt.legend((start, end), ('Starting point', 'Destination'), scatterpoints=1, loc='upper right', fontsize=8)
    #plt.show()
    plt.savefig('figs/popularTrip_'+str(counter)+'.eps')
"""


"""
N = 24

ind = np.arange(N)  # the x locations for the groups
width = 1.       # the width of the bars

fig, ax = plt.subplots()
rects = ax.bar(ind, distLGAToJFK, width, color='r')

# add some text for labels, title and axes ticks
tickrange = np.arange(9)
ax.set_xlabel('Time of day')
ax.set_title('Average number of trips between LGA and JFK')
ax.set_xticks(3*(tickrange)+width/2.)
ax.set_xticklabels(('00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00','00:00'))

#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        #ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
        #        '%d' % int(height),
        #        ha='center', va='bottom')

autolabel(rects)

plt.savefig('figs/tripsBetweenLGAAndJFK2013.eps')

"""

KClustersLGALat = []
KClustersLGALong = []
KClustersJFKLat = []
KClustersJFKLong = []

for cluster in KClustersLGA:
    lat = minLat + dLat*cluster[0]
    longi = minLong + dLong*cluster[1]
    KClustersLGALat.append(lat)
    KClustersLGALong.append(longi)

for cluster in KClustersJFK:
    lat = minLat + dLat*cluster[0]
    longi = minLong + dLong*cluster[1]
    KClustersJFKLat.append(lat)
    KClustersJFKLong.append(longi)

for i in range(0, 10):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_title('Location of a cluster of '+str(int(math.floor(meanNormLGA[i])))+' trips to or from JFK')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    #print(KClustersLGALong[i], KClustersLGALat[i])

    plt.imshow(img, zorder=0, extent=[-74.28, -73.675, 40.468, 40.945])
    start = plt.scatter([KClustersJFKLong[i]], [KClustersJFKLat[i]], s=70, color='b', marker = 'o')
    #plt.legend((start), ('A cluster of '+str(meanNormLGA[i])+' trips'), scatterpoints=1, loc='upper right', fontsize=8)
    plt.show()
    #plt.savefig('figs/clusterToLGA_'+str(counter)+'.eps')


































"""
fig, ax = plt.subplots()
rects = ax.bar(ind, averageMPH, width, color='r')
ax.set_xlabel('Time of day')
ax.set_title('Average MPH of a taxi trip in 2013')
ax.set_xticks(3*(tickrange)+width/2.)
ax.set_xticklabels(('00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00','00:00'))

plt.show()
"""

#plt.imshow(img, zorder=0, extent=[-74.28, -73.675, 40.468, 40.945])
#plt.scatter(KClustersLGALat, KClustersLGALong)
#plt.set_ylim([minLat, maxLat])
#plt.set_xlim([minLong, maxLong])
#plt.show()


#fig, ax = plt.subplots()
#ax.set_title('Clustering of trips to or from LGA')
#ax.set_xlabel('Longitude')
#ax.set_ylabel('Latitude')

#plt.imshow(img, zorder=0, extent=[-74.28, -73.675, 40.468, 40.945])
##ax = plt.add_subplot()
#plt.scatter(KClustersLGALat, KClustersLGALong)
#plt.show()
