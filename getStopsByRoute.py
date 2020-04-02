import json
import pandas as pd

data = pd.read_csv("./ProducedData/AllStops.csv")

Routes = data.Route.unique();
stopsByRoute = {}
for r in Routes:
    routeStops = data[data.Route == r]
    stops = list(set(routeStops.FromStop.unique()) | set(routeStops.toStop.unique()))
    stopsByRoute[r] = stops

with open('stopsByRoute.json', 'w') as fp:
    json.dump(stopsByRoute, fp)
