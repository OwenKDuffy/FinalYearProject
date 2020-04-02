from statistics import stdev
import pandas as pd

data = pd.read_csv("./ProducedData/AllStops.csv", dtype = {"FromStop": "int32", "toStop": "int32"})
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

variabilityBetweenStops = variabilityBetweenStops.sort_values("StdDev", ascending = False)
variabilityBetweenStops.to_csv("variabilityBetweenStopsNormalised.csv")
