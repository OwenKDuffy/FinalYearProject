from statistics import stdev
import pandas as pd

data = pd.read_csv("AllStops.csv")
variabilityBetweenStops = pd.DataFrame(columns = ["Stop1", "Stop2", "MeanTime", "StdDev", "NumJourneys"])
for s1 in data.FromStop.unique():
    journeysFromStop = data[data.FromStop == s1]
    for s2 in journeysFromStop.toStop.unique():
        journeysToStop = journeysFromStop[journeysFromStop.toStop == s2]
        meanTime = journeysToStop.Duration.mean()
        if(journeysToStop.shape[0] >= 2):
            stanDev = stdev(journeysToStop.Duration, meanTime)
        else:
            stanDev = 0
        variabilityBetweenStops = variabilityBetweenStops.append({"Stop1": s1, "Stop2": s2, "MeanTime": meanTime, "StdDev": stanDev, "NumJourneys": journeysToStop.shape[0]}, ignore_index = True)

variabilityBetweenStops = variabilityBetweenStops.sort_values("StdDev", ascending = False)
variabilityBetweenStops.to_csv("variabilityBetweenStops.csv")
