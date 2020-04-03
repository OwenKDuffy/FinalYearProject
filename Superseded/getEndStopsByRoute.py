import json
import pandas as pd

data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})

Routes = data.LineID.unique();
stopsByRoute = {}
for r in Routes:
    # routeStops = data[data.LineID == r]
    # stops = list(set(routeStops.FromStop.unique()) | set(routeStops.toStop.unique()))
    stops = {"Start": 0, "End": 1, "Dir": -1}
    stopsByRoute[r] = stops

with open('endStopsByRoute.json', 'w') as fp:
    json.dump(stopsByRoute, fp)
