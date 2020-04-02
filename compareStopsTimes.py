import plotly.express as px
import pandas as pd

data = pd.read_csv("AllStops.csv")
routes = data.Route.unique()
routeTimes = {}
for r in routes:
    journeysOnRoute = data[data.Route == r]
    meanForRoute = journeysOnRoute.RawDuration.mean()
    routeTimes[r] = meanForRoute

data['Variance'] = data.apply(lambda x: getVariance(x['RawDuration'], routeTimes, x['Route']))
data.to_csv("JourneyTimesWithVariance.csv")

def getVariance(time, meanMap, route):
    return time - meanMap[route]
