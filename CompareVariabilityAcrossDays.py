import sys
import os
import pandas as pd
import plotly.graph_objects as go

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
        # data = data[data["NumJourneys"] >= 2]
        variabilities[file.decode("utf-8")] = data.StdDev.mean()

    #print(list(variabilities.keys()))
    xAxisDays = list((pd.Series(list(variabilities.keys()))).map(days))
    # #print(xAxisDays)
    xAxisDates = [x[-6:-4] for x in list(variabilities.keys())]
    # #print(xAxisDates)
    xAxis = [str(day) + " " + str(date) for day,date in zip(xAxisDays,xAxisDates)]
    # #print(xAxis)
    fig = go.Figure(data = go.Scatter(
        x = xAxis,
        y = list(variabilities.values()),
        mode='lines+markers'))
    fig.update_layout(title='StdDev across All Interstop Trips per Day',
                   xaxis_title = "Day",
                   yaxis_title = "Mean Standard Deviation on Day")

    fig.show()


if __name__ == '__main__':
    main(sys.argv[1])
