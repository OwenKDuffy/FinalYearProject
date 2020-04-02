import plotly.express as px
import pandas as pd

data = pd.read_csv("AllJourneys.csv")
routes = data.Route.unique()
routeTimes = {}
for r in routes:
    journeysOnRoute = data[data.Route == r]
    meanForRoute = journeysOnRoute.RawDuration.mean()
    routeTimes[r] = meanForRoute

data['Variance'] = data.apply(lambda row: row['RawDuration'] + routeTimes[row['Route']], axis=1)

data.to_csv("JourneyTimesWithVariance.csv")
