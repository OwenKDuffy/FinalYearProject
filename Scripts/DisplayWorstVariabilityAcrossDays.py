import sys
import os
import pandas as pd
import plotly.graph_objects as go

def main(folder):
    # directory_in_str = os.getcwd() + '/Datasets'
    # #print(folder)
    days = pd.read_csv("DaysofWeek.csv", index_col=0, squeeze=True, header = None).to_dict()
    df_stops = pd.read_csv('StopsCoordsJS.csv')
    directory = os.fsencode(folder)
    directory = os.listdir(directory)
    # #print(directory[0])
    fig = go.Figure()
    for file in directory:
        # #print(file)
        dataset = folder + '/' + file.decode("utf-8")
        if (dataset.lower().endswith('.csv')):
            data = pd.read_csv(dataset)
            data = data.sort_values("StdDev", ascending = False)
            traceName = []
            startStop = data["Stop1"][0]
            startStopCoords = df_stops[df_stops["StopID"] == startStop]
            if(startStopCoords.shape[0] != 0):
                lo = [startStopCoords.iloc[0].Longitude]
                la = [startStopCoords.iloc[0].Latitude]
                traceName.append(str(int(startStop)))
            else:
                print("Error on startStop " + str(startStop) + " for file: " + dataset[13:])
                continue
            if "Stop3" in data.columns:
                midStop = data["Stop2"][0]
                midStopCoords = df_stops[df_stops["StopID"] == midStop]
                if(midStopCoords.shape[0] != 0):
                    lo.append(midStopCoords.iloc[0].Longitude)
                    la.append(midStopCoords.iloc[0].Latitude)
                    traceName.append(str(int(midStop)))
                else:
                    print("Error on: " + str(midStop))
                    continue
                endStop = data["Stop3"][0]
            else:
                endStop = data["Stop2"][0]
            # print(startStopCoords)
            endStopCoords = df_stops[df_stops["StopID"] == endStop]
            if(endStopCoords.shape[0] != 0):
                lo.append(endStopCoords.iloc[0].Longitude)
                la.append(endStopCoords.iloc[0].Latitude)
                traceName.append(str(int(endStop)))
            else:
                print("Error on: " + str(endStop))
                continue
            fig.add_trace(go.Scattermapbox(
                mode = "markers+lines",
                lon = lo,
                lat = la,
                marker = dict(
                    size = 10
                    ),
                text = traceName,
                hoverinfo = 'text',
                # line={'color': colours[j]},
                name = file.decode("utf-8")[-6:-4] + "/" + file.decode("utf-8")[-8:-6]))
            #myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
            # colourValuesMapped = ((data["StdDev"][i] - minStdDev)/ (maxStdDev - minStdDev)) * 255
            # red = min(255, 2 * colourValuesMapped)
            # green = min(255, 2 * (255 - colourValuesMapped))
            # colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
    #print(list(variabilities.keys()))
    # xAxisDays = list((pd.Series(list(variabilities.keys()))).map(days))
    # # #print(xAxisDays)
    # xAxisDates = [x[-6:-4] for x in list(variabilities.keys())]
    # # #print(xAxisDates)
    # xAxis = [str(day) + " " + str(date) for day,date in zip(xAxisDays,xAxisDates)]
    # # #print(xAxis)
    #
    #
    # for j in range(1, len(stopsLongs)):
    #     lo = stopsLongs[j]
    #     la = stopsLats[j]
    #     traceName = names[j]
    #     fig.add_trace(go.Scattermapbox(
    #         mode = "markers+lines",
    #         lon = lo,
    #         lat = la,
    #         marker = dict(
    #             size = 10
    #             ),
    #         text = traceName,
    #         hoverinfo = 'text',
    #         line={'color': colours[j]},
    #         name = str(traceName[0]  + "->" + traceName[1])))

    fig.update_layout(title='Highest StdDev Interstop Trips per Day',
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'style': "stamen-terrain",
            'center': {'lon': -6.2, 'lat': 53.34},
            'zoom': 10})

    fig.show()


if __name__ == '__main__':
    main(sys.argv[1])
