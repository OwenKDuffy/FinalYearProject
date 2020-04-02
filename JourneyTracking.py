#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
from datetime import datetime
import math
from IPython.display import display, HTML


# In[2]:


data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})


# In[3]:



vehicles = data.VehicleID.unique()
journeysDF = pd.DataFrame()
# v = vehicles[0]
journeysByVehicle = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])


# In[4]:


for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    interStopTime = pd.DataFrame(columns = ["Route", "JourneyID", "From", "To", "Time"])
    # display(HTML(output[output.VehicleJourneyID == journeys[1]].to_html()))
    for j in journeys:
        journey = output[output.VehicleJourneyID == j]
        route = journey.iloc[0].LineID
        stops = journey[journey.AtStop == 1]
        # startTime = journey.iloc[0].TimeF
        stopAt = stops.iloc[0].StopID
        stopTime = stops.iloc[0].Timestamp
        for i in stops:
            if(i.StopID != stopAt):
                interStopTime = interStopTime.append({"Route": route, "JourneyID": j, "From": stopAt, "To": i.StopID, "Time": startTime - i.Timestamp})
        # endTime = journey.iloc[-1].TimeF
        # x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp
        # duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')

    interStopTime.to_csv("interStopTime.csv")

# In[ ]:
