import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys

def main(dataset1, dataset2):
    df_stops = pd.read_csv('./ProducedData/StopsCoordsJS.csv', dtype = {'StopID': 'int32'})
    # print(df_stops.head())

    df_1 = pd.read_csv(dataset1) #, dtype = {'Stop1': 'int32', 'Stop2': 'int32', 'Stop3': 'int32'})
    df_2 = pd.read_csv(dataset2) #, dtype = {'Stop1': 'int32', 'Stop2': 'int32'})
    df_1 = df_1.sort_values("StdDev", ascending = False)
    df_2 = df_2.sort_values("StdDev", ascending = False)
    maxStdDevdf_1 = df_1["StdDev"].max()
    minStdDevdf_1 = df_1["StdDev"].min()
    maxStdDevdf_2 = df_2["StdDev"].max()
    minStdDevdf_2 = df_2["StdDev"].min()
    df_2 = df_2.head(10)
    df_1 = df_1.head(10)

    # print(df_2)

    stopsLongs = []
    stopsLats = []
    names = []
    colours = []
    for i in range(df_2.shape[0]):
        startStop = df_2["Stop1"][i]
        startStopCoords = df_stops[df_stops["StopID"] == startStop]
        midStop = None
        if "Stop3" in df_2.columns:
            midStop = df_2["Stop2"][i]
            midStopCoords = df_stops[df_stops["StopID"] == midStop]
            endStop = df_2["Stop3"][i]
        else:
            endStop = df_2["Stop2"][i]
        endStopCoords = df_stops[df_stops["StopID"] == endStop]
        if(startStopCoords.shape[0] != 0 and endStopCoords.shape[0] != 0):
            # print(str(startStop) + "->" + str(endStop))
            stopsLongs.append([startStopCoords.iloc[0].Longitude, endStopCoords.iloc[0].Longitude])
            stopsLats.append([startStopCoords.iloc[0].Latitude, endStopCoords.iloc[0].Latitude])
            thisName = [str(int(startStop))]
            if midStop is not None:
                thisName.append(str(int(midStop)))
            thisName.append(str(int(endStop)))
            names.append(thisName)
            #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
            colourValuesMapped = ((df_2["StdDev"][i] - minStdDevdf_2)/ (maxStdDevdf_2 - minStdDevdf_2)) * 255
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
    for i in range(df_1.shape[0]):
        startStop = df_1["Stop1"][i]
        startStopCoords = df_stops[df_stops["StopID"] == startStop]
        midStop = None
        if "Stop3" in df_1.columns:
            midStop = df_1["Stop2"][i]
            midStopCoords = df_stops[df_stops["StopID"] == midStop]
            endStop = df_1["Stop3"][i]
        else:
            endStop = df_1["Stop2"][i]
        endStopCoords = df_stops[df_stops["StopID"] == endStop]
        if(startStopCoords.shape[0] != 0 and midStopCoords.shape[0] != 0 and endStopCoords.shape[0] != 0):
            # print(str(startStop) + "->" + str(midStop) + "->" + str(endStop))
            stopsLongs.append([startStopCoords.iloc[0].Longitude, midStopCoords.iloc[0].Longitude, endStopCoords.iloc[0].Longitude])
            stopsLats.append([startStopCoords.iloc[0].Latitude, midStopCoords.iloc[0].Latitude, endStopCoords.iloc[0].Latitude])
            thisName = [str(int(startStop))]
            if midStop is not None:
                thisName.append(str(int(midStop)))
            thisName.append(str(int(endStop)))
            names.append(thisName)
            #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
            colourValuesMapped = ((df_1["StdDev"][i] - minStdDevdf_2)/ (maxStdDevdf_2 - minStdDevdf_2)) * 255
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

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
