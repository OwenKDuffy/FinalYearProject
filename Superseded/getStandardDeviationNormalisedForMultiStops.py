from statistics import stdev
import pandas as pd

data = pd.read_csv("ProducedData/AllTriplesStops.csv")
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

variabilityBetweenStops = variabilityBetweenStops.sort_values("StdDev", ascending = False)
variabilityBetweenStops.to_csv("variabilityBetweenMultiStopsNormalised.csv")
