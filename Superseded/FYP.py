#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
from datetime import datetime
import math
from IPython.display import display, HTML

def toHumanReadable(x):
    if(not math.isnan(x)):
        return datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')
    else:
        return x
# In[2]:


data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})


# In[23]:


vehicles = data.VehicleID.unique()
journeysDF = pd.DataFrame()
# v = vehicles[0]
journeysByVehicle = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    # display(HTML(output[output.VehicleJourneyID == journeys[1]].to_html()))
    for j in journeys:
        journey = output[output.VehicleJourneyID == j]
        route = journey.iloc[0].LineID
        startTime = journey.iloc[0].TimeF
        endTime = journey.iloc[-1].TimeF
        x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp
        # duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')
        journeysByVehicle = journeysByVehicle.append({'JourneyID': j, 'Route': route, 'StartTime': startTime, 'Endtime': endTime, 'Duration': x}, ignore_index = True)

journeysByVehicle.to_csv("journeysByVehicle.csv")
routeTimes = pd.DataFrame(columns = ['Route','MinTime','Minus', 'MeanTime', 'Plus', 'MaxTime'])
print(journeysByVehicle.Route.unique())
for r in journeysByVehicle.Route.unique():
    if(r != "nan"):
        tripsOnRoute = journeysByVehicle[journeysByVehicle.Route == r]
        meanForRoute = tripsOnRoute.Duration.mean()
        minForRoute = toHumanReadable(tripsOnRoute.Duration.min())
        maxForRoute = toHumanReadable(tripsOnRoute.Duration.max())
        plusstdDev = toHumanReadable(meanForRoute + tripsOnRoute.Duration.std())
        minusstdDev = toHumanReadable(meanForRoute - tripsOnRoute.Duration.std())

        # duration = meanForRoute/(1000000) #time in seconds
        routeTimes = routeTimes.append({'Route': r, 'MeanTime': toHumanReadable(meanForRoute), 'MinTime': minForRoute, 'MaxTime': maxForRoute, 'Plus': plusstdDev, 'Minus': minusstdDev}, ignore_index = True)

routeTimes.to_csv("journeyTimeByRoute.csv")



# In[35]:


# display(HTML(o.to_html()))


# In[ ]:
