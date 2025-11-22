import plotly.graph_objects as go
import pandas as pd
import numpy as np


df_stops = pd.read_csv('./ProducedData/StopsCoordsJS.csv')
# print(df_stops.head())

df_journeys = pd.read_csv('variabilityBetweenMultiStopsNormalised.csv')
df_journeys = df_journeys.sort_values("StdDev", ascending = False)
maxStdDev = df_journeys["StdDev"].max()
minStdDev = df_journeys["StdDev"].min()
df_journeys = df_journeys.head(40)
# print(df_journeys)

stopsLongs = []
stopsLats = []
names = []
colours = []
for i in range(df_journeys.shape[0]):
    startStop = df_journeys["Stop1"][i]
    midStop = df_journeys["Stop2"][i]
    endStop = df_journeys["Stop3"][i]
    print(str(startStop) + "->" + str(midStop) + "->" + str(endStop))
    startStopCoords = df_stops[df_stops["StopID"] == startStop]
    midStopCoords = df_stops[df_stops["StopID"] == midStop]
    endStopCoords = df_stops[df_stops["StopID"] == endStop]
    if(startStopCoords.shape[0] != 0 and midStopCoords.shape[0] != 0 and endStopCoords.shape[0] != 0):
        stopsLongs.append([startStopCoords.iloc[0].Longitude, midStopCoords.iloc[0].Longitude, endStopCoords.iloc[0].Longitude])
        stopsLats.append([startStopCoords.iloc[0].Latitude, midStopCoords.iloc[0].Latitude, endStopCoords.iloc[0].Latitude])
        names.append([str(int(startStop)), str(int(midStop)), str(int(endStop))])
        #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
        colourValuesMapped = ((df_journeys["StdDev"][i] - minStdDev)/ (maxStdDev - minStdDev)) * 255
        red = min(255, 2 * colourValuesMapped)
        green = min(255, 2 * (255 - colourValuesMapped))
        colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))

#
# print(stopsLongs[0])
# print(stopsLats[0])
# print(stopsLongs[1])
# print(stopsLats[1])
# print(colourName)
fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = stopsLongs[0],
    lat = stopsLats[0],
    marker = {'size': 10},
    text = names[0],
    hoverinfo = 'text',
    line={'color': colours[0]},
    name = str(names[0][0]  + "->" + names[0][1] + "->" + names[0][2])))

for j in range(1, len(stopsLongs)):
    lo = stopsLongs[j]
    la = stopsLats[j]
    traceName = names[j]
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = lo,
        lat = la,
        marker = dict(
            size = 10
            ),
        text = traceName,
        hoverinfo = 'text',
        line={'color': colours[j]},
        name = str(traceName[0]  + "->" + traceName[1] + "->" + traceName[2])))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon': -6.2, 'lat': 53.34},
        'zoom': 10})

fig.show()
