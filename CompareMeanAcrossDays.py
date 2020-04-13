import sys
import os
import pandas as pd
import plotly.graph_objects as go
import multiprocessing
from multiprocessing import Pool, Manager
import math
import sys

def getMeanComparisons(data, procnum, return_dict):
    #data = [Stop1, Stop2, Stop3,MeanTime,Day,Date]
    normalisedMeans = pd.DataFrame()
    for s1 in data.Stop1.unique():
        journeysFromStop = data[data.Stop1 == s1]
        for s2 in journeysFromStop.Stop2.unique():
            journeysToStop = journeysFromStop[journeysFromStop.Stop2 == s2]
            for s3 in journeysToStop.Stop3.unique():
                journeysFinalStop = journeysToStop[journeysToStop.Stop3 == s3]
                meanTime = journeysFinalStop.MeanTime.mean()
                journeysFinalStop["NormalisedMean"] = journeysFinalStop.MeanTime / meanTime
                # if(journeysFinalStop.shape[0] >= 2):
                #     stanDev = stdev(journeysFinalStop.NormalisedDuration, meanTime)
                # else:
                #     stanDev = 0
                normalisedMeans = normalisedMeans.append(journeysFinalStop)
    return_dict[procnum] = normalisedMeans




def main(folder):
    # directory_in_str = os.getcwd() + '/Datasets'
    # #print(folder)
    days = pd.read_csv("DaysofWeek.csv", index_col=0, squeeze=True, header = None).to_dict()
    #print(days)
    directory = os.fsencode(folder)
    directory = os.listdir(directory)
    # #print(directory[0])
    variabilities = {}
    fullDataSet = pd.DataFrame()
    for file in directory:
        dataset = folder + '/' + file.decode("utf-8")
        print(dataset)
        # TODO: Make usable for Pairstops
        data = pd.read_csv(dataset, usecols = ["Stop1", "Stop2", "Stop3", "MeanTime"])
        data["Day"] = days[file.decode("utf-8")[-12:]]
        data["Date"] = file.decode("utf-8")[-12:-4]
        fullDataSet = fullDataSet.append(data, ignore_index = True)
        # variabilities[file.decode("utf-8")] = data.StdDev.mean()

    print(fullDataSet.head())
    mgr = Manager()
    return_dict = mgr.dict()
    numThreads = 50
    stops = fullDataSet.Stop1.unique()
    numStops = len(stops)
    stopsPerThread = math.ceil(numStops / numThreads)
    startIndex = 0
    endIndex = stopsPerThread
    jobs = []


    for s in range(numThreads):
        proc = multiprocessing.Process(target = getMeanComparisons, args = (fullDataSet[fullDataSet.Stop1.isin(stops[startIndex:min(endIndex, numStops)])],s, return_dict))
        jobs.append(proc)
        proc.start()
        startIndex = endIndex
        endIndex = endIndex + stopsPerThread

    for j in jobs:
        j.join()
        print("Joined Thread:" + str(j))
    outputData = pd.DataFrame()

    for val in return_dict.values():
        outputData = outputData.append(val, ignore_index = True)

    outputData.to_csv("./ProducedData/MeansByDay.csv")
    # #print(list(variabilities.keys()))
    # xAxisDays = list((pd.Series(list(variabilities.keys()))).map(days))
    # # #print(xAxisDays)
    # xAxisDates = [x[-6:-4] for x in list(variabilities.keys())]
    # # #print(xAxisDates)
    # xAxis = [str(day) + " " + str(date) for day,date in zip(xAxisDays,xAxisDates)]
    # # #print(xAxis)
    # fig = go.Figure(data = go.Scatter(
    #     x = xAxis,
    #     y = list(variabilities.values()),
    #     mode='lines+markers'))
    # fig.update_layout(title='StdDev across All Interstop Trips per Day',
    #                xaxis_title = "Day",
    #                yaxis_title = "Mean Standard Deviation on Day")
    #
    # fig.show()


if __name__ == '__main__':
    main(sys.argv[1])
