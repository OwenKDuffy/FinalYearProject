import sys
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def SetColor(x):
        if(x[:3] == "Sat" or x[:3] == "Sun"):
            return "red"
        else:
            return "blue"

def main(folder):
    # directory_in_str = os.getcwd() + '/Datasets'
    # #print(folder)
    days = pd.read_csv("DaysofWeek.csv", index_col=0, squeeze=True, header = None).to_dict()
    #print(days)
    directory = os.fsencode(folder)
    directory = os.listdir(directory)
    # #print(directory[0])
    variabilities = {}
    for file in directory:
        # #print(file)
        dataset = folder + '/' + file.decode("utf-8")
        data = pd.read_csv(dataset)
        variabilities[file.decode("utf-8")] = data.StdDev.mean()

    #print(list(variabilities.keys()))
    xAxisDays = list((pd.Series(list(variabilities.keys()))).map(days))
    # #print(xAxisDays)
    xAxisDates = [str(x[-6:-4] + "/" + x[-8:-6]) for x in list(variabilities.keys())]
    # #print(xAxisDates)
    xAxis = [str(day)[:3] + " " + str(date) for day,date in zip(xAxisDays,xAxisDates)]
    # #print(xAxis)
    fig = make_subplots(rows = 1, cols = 2)
    fig.add_trace(go.Scatter(
        x = xAxis,
        y = list(variabilities.values()),
        mode='lines+markers',
        name = "StdDev"), row = 1, col = 1)
    fig.update_layout(title='StdDev & Mean across All Interstop Trips per Day',
                   xaxis_title = "Day")


    meansData = pd.read_csv("./ProducedData/MeansByDay.csv", usecols = {"Day", "Date", "NormalisedMean"})
    graphData = {}
    # print(meansData.Date.unique())
    dates = meansData.Date.unique()
    dates.sort()
    print(dates)
    for d in dates:
        thisDay = meansData[meansData["Date"] == d]
        mean = thisDay.NormalisedMean.mean()
        graphData[thisDay.Day.values[0][:3] + " " + str(d)[-2:] + "/" + str(d)[-4:-2]] = mean

    fig.add_trace(go.Scatter(
    x = list(graphData.keys()),
    y = list(graphData.values()),
    mode='markers+lines',
    marker = {"size": 8, "color" : list(map(SetColor, list(graphData.keys())))},
    line = {"color": "black"},
    name = "Means"),
    row = 1, col = 2)
    '''
    fig.update_layout(title='Mean Journey Time Comparisons',
    xaxis_title = "Day",
    yaxis_title = "Journey time as compared to mean")

    fig.show()
    '''
    fig.show()


if __name__ == '__main__':
    main(sys.argv[1])
