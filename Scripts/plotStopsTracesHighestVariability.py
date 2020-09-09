import plotly.graph_objects as go
import pandas as pd

df_stops = pd.read_csv('stopCoords.csv')
print(df_stops.head())

df_journeys = pd.read_csv('variabilityBetweenStops.csv')
print(df_journeys.head())

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode = 'USA-states',
    lon = df_stops['Long'],
    lat = df_stops['Lat'],
    hoverinfo = 'text',
    text = df_stops['StopID'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

journey_path = []
for i in range(len(df_journeys)):
    startStop = df_journeys["Stop1"][i]
    endStop = df_journeys["Stop2"][i]
    startLong = df_stops[df_stops["StopID"] == startStop].Long.values
    endLong = df_stops[df_stops["StopID"] == endStop].Long.values
    startLat = df_stops[df_stops["StopID"] == startStop].Lat.values
    endLat = df_stops[df_stops["StopID"] == endStop].Lat.values
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = [startLong, endLong],
            lat = [startLat, endLat],
            mode = 'lines',
            line = dict(width = 1,color = 'red'),
            opacity = float(df_journeys['StdDev'][i]) / float(df_journeys['StdDev'].max()),
        )
    )

fig.update_layout(
    title_text = 'High Variabilty Bus Journeys<br>(Hover for stop Numbers)',
    showlegend = False,
    geo = dict(
        scope = 'europe',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

fig.show()
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# #reading in data
# stopVariability = pd.read_csv("variabilityBetweenStops.csv")
# stopCoords = pd.read_csv("stopCoords.csv")
#
# stopVariability = stopVariability.sort_values("StdDev")
# topTenHighestVariable = stopVariability.head(10)
# highVariableStops = list(set(topTenHighestVariable.Stop1.unique()) | set(topTenHighestVariable.Stop2.unique()))
# highestVariableStopsCoords = stopCoords[stopCoords["StopID"].isin(highVariableStops)]
#
# BBox = ((highestVariableStopsCoords.Long.min(),   highestVariableStopsCoords.Long.max(), highestVariableStopsCoords.Lat.min(), highestVariableStopsCoords.Lat.max()))
#
# lines = []
# for i in topTenHighestVariable:
#     s1 = stopCoords[stopCoords["StopID"] == i.Stop1]
#     s2 = stopCoords[stopCoords["StopID"] == i.Stop2]
#     x = [s1.Long, s2.Long]
#     y = [s1.Lat, s2.Lat]
#     lines.append([x, y])
#
#
# print(BBox)
# mapImg = plt.imread('map.png')
# #drawing plot
# fig, ax = plt.subplots(figsize = (8,7))
# # ax.scatter(highestVariableStopsCoords.Long, highestVariableStopsCoords.Lat, zorder=1, alpha= 0.2, c='b', s=10)
# for l in lines:
#     x = l[0]
#     y = l[1]
#     print(x)
#     print(y)
#     plt.plot(l[0], l[1])
#     # plt.plot('x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
# ax.set_title('Most Variable Bus Stops in Dublin')
# ax.set_xlim(BBox[0],BBox[1])
# ax.set_ylim(BBox[2],BBox[3])
# ax.imshow(mapImg, zorder=0, extent = BBox, aspect= 'equal')
