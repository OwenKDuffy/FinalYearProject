import sys
import os
import pandas as pd
import plotly.graph_objects as go

def SetColor(x):
        if(x[:3] == "Sat" or x[:3] == "Sun"):
            return "red"
        else:
            return "blue"

def main():
    # # directory_in_str = os.getcwd() + '/Datasets'
    # # #print(folder)
    # days = pd.read_csv("DaysofWeek.csv", index_col=0, squeeze=True, header = None).to_graphData()
    # #print(days)
    # directory = os.fsencode(folder)
    # directory = os.listdir(directory)
    # # #print(directory[0])
    # variabilities = {}
    # for file in directory:
    #     # #print(file)
    #     dataset = folder + '/' + file.decode("utf-8")
    #     data = pd.read_csv(dataset)
    #     variabilities[file.decode("utf-8")] = data.StdDev.mean()
    data = pd.read_csv("./ProducedData/MeansByDay.csv", usecols = {"Day", "Date", "NormalisedMean"})
    graphData = {}
    print(data.Date.unique())
    dates = data.Date.unique()
    dates.sort()
    print(dates)
    for d in dates:
        thisDay = data[data["Date"] == d]
        mean = thisDay.NormalisedMean.mean()
        graphData[thisDay.Day.values[0][:3] + " " + str(d)[-2:] + "/" + str(d)[-4:-2]] = mean

    fig = go.Figure(data = go.Scatter(
        x = list(graphData.keys()),
        y = list(graphData.values()),
        mode='markers+lines',
        marker = {"size": 8, "color" : list(map(SetColor, list(graphData.keys())))},
        line = {"color": "black"}))
    fig.update_layout(title='Mean Journey Time Comparisons',
                   xaxis_title = "Day",
                   yaxis_title = "Journey time as compared to mean")

    fig.show()


if __name__ == '__main__':
    main()
