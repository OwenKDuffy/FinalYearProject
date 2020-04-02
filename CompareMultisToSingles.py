import plotly.graph_objects as go
import pandas as pd
import numpy as np


df_stops = pd.read_csv('./ProducedData/StopsCoordsJS.csv', dtype = {'StopID': 'int32'})
# print(df_stops.head())

df_multi_journeys = pd.read_csv('variabilityBetweenMultiStopsNormalised.csv',dtype = {'Stop1': 'int32', 'Stop2': 'int32', 'Stop3': 'int32'})
df_journeys = pd.read_csv('./ProducedData/variabilityBetweenStopsNormalised.csv',dtype = {'Stop1': 'int32', 'Stop2': 'int32'})
df_multi_journeys = df_multi_journeys.sort_values("StdDev", ascending = False)
df_journeys = df_journeys.sort_values("StdDev", ascending = False)
maxStdDevMulti = df_multi_journeys["StdDev"].max()
minStdDevMulti = df_multi_journeys["StdDev"].min()
maxStdDev = df_journeys["StdDev"].max()
minStdDev = df_journeys["StdDev"].min()
df_journeys = df_journeys.head(10)
df_multi_journeys = df_multi_journeys.head(10)

# print(df_journeys)

stopsLongs = []
stopsLats = []
names = []
colours = []
for i in range(df_journeys.shape[0]):
    startStop = df_journeys["Stop1"][i]
    endStop = df_journeys["Stop2"][i]
    startStopCoords = df_stops[df_stops["StopID"] == startStop]
    # midStopCoords = df_stops[df_stops["StopID"] == midStop]
    endStopCoords = df_stops[df_stops["StopID"] == endStop]
    if(startStopCoords.shape[0] != 0 and endStopCoords.shape[0] != 0):
        # print(str(startStop) + "->" + str(endStop))
        stopsLongs.append([startStopCoords.iloc[0].Longitude, endStopCoords.iloc[0].Longitude])
        stopsLats.append([startStopCoords.iloc[0].Latitude, endStopCoords.iloc[0].Latitude])
        names.append([str(int(startStop)), str(int(endStop))])
        #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
        colourValuesMapped = ((df_journeys["StdDev"][i] - minStdDev)/ (maxStdDev - minStdDev)) * 255
        red = min(255, 2 * colourValuesMapped)
        green = min(255, 2 * (255 - colourValuesMapped))
        colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
    else:
        print("StartStop: " + str(startStop) + "Coords: " + str(startStopCoords))
        print("endStop: " + str(endStop) + "Coords: " + str(endStopCoords))

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
    line={'color': "blue"},
    name = str(names[0][0]  + "->" + names[0][1])))

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
        line={'color': "blue"},
        name = str(traceName[0] + "->" + traceName[1])))

stopsLongs = []
stopsLats = []
names = []
colours = []
for i in range(df_multi_journeys.shape[0]):
    startStop = df_multi_journeys["Stop1"][i]
    midStop = df_multi_journeys["Stop2"][i]
    endStop = df_multi_journeys["Stop3"][i]
    startStopCoords = df_stops[df_stops["StopID"] == startStop]
    midStopCoords = df_stops[df_stops["StopID"] == midStop]
    endStopCoords = df_stops[df_stops["StopID"] == endStop]
    if(startStopCoords.shape[0] != 0 and midStopCoords.shape[0] != 0 and endStopCoords.shape[0] != 0):
        # print(str(startStop) + "->" + str(midStop) + "->" + str(endStop))
        stopsLongs.append([startStopCoords.iloc[0].Longitude, midStopCoords.iloc[0].Longitude, endStopCoords.iloc[0].Longitude])
        stopsLats.append([startStopCoords.iloc[0].Latitude, midStopCoords.iloc[0].Latitude, endStopCoords.iloc[0].Latitude])
        names.append([str(int(startStop)), str(int(midStop)), str(int(endStop))])
        #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
        colourValuesMapped = ((df_multi_journeys["StdDev"][i] - minStdDev)/ (maxStdDev - minStdDev)) * 255
        red = min(255, 2 * colourValuesMapped)
        green = min(255, 2 * (255 - colourValuesMapped))
        colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
    else:
        print("StartStop: " + str(startStop) + "Coords: " + str(startStopCoords))
        print("midStop: " + str(midStop) + "Coords: " + str(midStopCoords))
        print("endStop: " + str(endStop) + "Coords: " + str(endStopCoords))

for i in range(0, len(stopsLongs)):
    lo = stopsLongs[i]
    la = stopsLats[i]
    traceName = names[i]
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = lo,
        lat = la,
        marker = dict(
            size = 10
            ),
        text = traceName,
        hoverinfo = 'text',
        line={'color': "red"},
        name = str(traceName[0]  + "->" + traceName[1] + "->" + traceName[2])))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'style': "stamen-terrain",
        'center': {'lon': -6.2, 'lat': 53.34},
        'zoom': 10})

fig.show()
