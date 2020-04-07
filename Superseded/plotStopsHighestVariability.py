import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#reading in data
stopVariability = pd.read_csv("variabilityBetweenStops.csv")
stopCoords = pd.read_csv("stopCoords.csv")

stopVariability = stopVariability.sort_values("StdDev")
topTenHighestVariable = stopVariability.head(10)
highVariableStops = list(set(topTenHighestVariable.Stop1.unique()) | set(topTenHighestVariable.Stop2.unique()))
highestVariableStopsCoords = stopCoords[stopCoords["StopID"].isin(highVariableStops)]

BBox = ((highestVariableStopsCoords.Long.min(),   highestVariableStopsCoords.Long.max(), highestVariableStopsCoords.Lat.min(), highestVariableStopsCoords.Lat.max()))

print(BBox)
mapImg = plt.imread('map.png')
#drawing plot
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(highestVariableStopsCoords.Long, highestVariableStopsCoords.Lat, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Most Variable Bus Stops in Dublin')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(mapImg, zorder=0, extent = BBox, aspect= 'equal')
