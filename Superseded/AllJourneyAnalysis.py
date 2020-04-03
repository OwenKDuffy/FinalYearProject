#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from datetime import datetime
from IPython.display import display, HTML


# In[10]:
# import os
# directory_in_str = os.getcwd() + '/Datasets'
# print(directory_in_str)
journeysDF = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime','StartStop', 'Endtime', 'EndStop', 'Duration'])
# directory = os.fsencode(directory_in_str)

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)

data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])


# In[11]:


vehicles = data.VehicleID.unique()

for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    o = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime','StartStop', 'Endtime', 'EndStop', 'Duration', 'RawDuration'])
    for j in journeys:
        journey = output[output.VehicleJourneyID == j]
        route = journey.iloc[0].LineID
        startTime = journey.iloc[0].TimeF
        startStop = journey.iloc[0].StopID
        endTime = journey.iloc[-1].TimeF
        endStop = journey.iloc[-1].StopID
        x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp
        duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')
        journeysDF = journeysDF.append({'JourneyID': j, 'Route': route, 'StartTime': startTime, 'StartStop': startStop, 'Endtime': endTime, 'EndStop': endStop, 'Duration': duration, 'RawDuration' : x/1000000}, ignore_index = True)

journeysDF.to_csv("AllJourneys.csv")
            # In[12]:


            # display(HTML(journeysDF.head().to_html()))


            # In[15]:


            # print(journeysDF.shape[0])


            # In[ ]:
