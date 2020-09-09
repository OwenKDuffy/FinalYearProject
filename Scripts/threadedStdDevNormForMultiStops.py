from statistics import stdev
import pandas as pd
import multiprocessing
from multiprocessing import Pool, Manager
import math
debug = False
pd.options.mode.chained_assignment = None  # default='warn'

def main(argv):
    inputFile = argv
    outputFile = "./ProducedData/Multistops/Normalised" + inputFile[(len(inputFile) - 1 - (inputFile[::-1].index("/"))):]
    if (debug == True):
        print("I: " + inputFile)
        print("O: " + outputFile)
    data = pd.read_csv(inputFile, dtype = {"StopA": "int32", "StopB": "int32", "StopC": "int32"})

    mgr = Manager()
    ns = mgr.Namespace()
    return_dict = mgr.dict()
    numThreads = 50
    stops = data.StopA.unique()
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
        proc = multiprocessing.Process(target = normaliseSlice, args = (s, return_dict, data[data.StopA.isin(stops[startIndex:min(endIndex, numStops)])]))
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
    variabilityBetweenStops = pd.DataFrame(columns = ["Stop1", "Stop2", "Stop3", "MeanTime", "StdDev", "NumJourneys"])
    for s1 in data.StopA.unique():
        journeysFromStop = data[data.StopA == s1]
        for s2 in journeysFromStop.StopB.unique():
            journeysToStop = journeysFromStop[journeysFromStop.StopB == s2]
            for s3 in journeysToStop.StopC.unique():
                journeysFinalStop = journeysToStop[journeysToStop.StopC == s3]
                meanTime = journeysFinalStop.Duration.mean()
                journeysFinalStop["NormalisedDuration"] = journeysFinalStop.Duration / meanTime
                if(journeysFinalStop.shape[0] >= 2):
                    stanDev = stdev(journeysFinalStop.NormalisedDuration, meanTime)
                else:
                    stanDev = 0
                variabilityBetweenStops = variabilityBetweenStops.append({"Stop1": s1, "Stop2": s2, "Stop3": s3, "MeanTime": meanTime, "StdDev": stanDev, "NumJourneys": journeysFinalStop.shape[0]}, ignore_index = True)
    return_dict[procnum] = variabilityBetweenStops
