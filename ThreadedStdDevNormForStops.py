from statistics import stdev
import pandas as pd
import multiprocessing
from multiprocessing import Pool, Manager
import math

def main(argv)
    inputFile = argv
    outputFile = "./ProducedData/Multistops/Normalised" + inputFile
    if (debug == True):
        print("I: " + inputFile)
        print("O: " + outputFile)
    data = pd.read_csv(inputFile, dtype = {"FromStop": "int32", "toStop": "int32"})

    mgr = Manager()
    ns = mgr.Namespace()
    return_dict = mgr.dict()
    numThreads = 50
    stops = data.FromStop.unique()
    numStops = len(stops)
    stopsPerThread = math.ceil(numStops / numThreads)
    startIndex = 0
    endIndex = stopsPerThread
    jobs = []
    if(debug == True):
	    print("Finished Preprocess")
    for s in range(numThreads):
        if(debug == True):
	        print("Creating proc: " + str(s))
        proc = multiprocessing.Process(target = findJourneyTimes, args = (s, return_dict, data[data.FromStop.isin(stops[startIndex:min(endIndex, numStops)])])
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

    outputData = outputData.sort_values("StdDev", ascending = False)
    outputData.to_csv(outputFile)


def normaliseSlice(procnum, return_dict, data):
    variabilityBetweenStops = pd.DataFrame(columns = ["Stop1", "Stop2", "MeanTime", "StdDev", "NumJourneys"])
    for s1 in data.FromStop.unique():
        journeysFromStop = data[data.FromStop == s1]
        for s2 in journeysFromStop.toStop.unique():
            journeysToStop = journeysFromStop[journeysFromStop.toStop == s2]
            meanTime = journeysToStop.Duration.mean()
            journeysToStop["NormalisedDuration"] = journeysToStop.Duration / meanTime
            if(journeysToStop.shape[0] >= 2):
                stanDev = stdev(journeysToStop.NormalisedDuration, meanTime)
            else:
                stanDev = 0
            variabilityBetweenStops = variabilityBetweenStops.append({"Stop1": int(s1), "Stop2": int(s2), "MeanTime": meanTime, "StdDev": stanDev, "NumJourneys": journeysToStop.shape[0]}, ignore_index = True)
    return_dict[procnum] = variabilityBetweenStops
