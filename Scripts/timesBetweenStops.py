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
stopsDF = pd.DataFrame(columns = ['FromStop', 'toStop', 'JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
# directory = os.fsencode(directory_in_str)

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)

data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})


# In[11]:


vehicles = data.VehicleID.unique()

for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    for j in journeys:
        journey = output[(output['VehicleJourneyID'] == j) & (output['AtStop']== 1)]
        if(journey.shape[0] != 0):
            route = journey.iloc[0].LineID
            firstStop = journey.iloc[0].StopID
            firstStopTime = journey.iloc[0].Timestamp
            for i in range(1, journey.shape[0]):
                sampleStop = journey.iloc[i].StopID
                sampleStopTime = journey.iloc[i].Timestamp
                if(sampleStop != firstStop):
                    stopsDF = stopsDF.append({'FromStop': firstStop, 'toStop': sampleStop, 'JourneyID': j, 'Route': route, 'StartTime': datetime.utcfromtimestamp(firstStopTime/1000000).strftime('%H:%M:%S'), 'EndTime': datetime.utcfromtimestamp(sampleStopTime/1000000).strftime('%H:%M:%S'), 'Duration': (sampleStopTime - firstStopTime)/1000000}, ignore_index = True)
                firstStop = sampleStop
                firstStopTime = sampleStopTime

        # journeysDF = journeysDF.append({'JourneyID': j, 'Route': route, 'StartTime': startTime, 'FromStop': startStop, 'Endtime': endTime, 'toStop': endStop, 'Duration': duration, 'RawDuration' : x/1000000}, ignore_index = True)
        # stopsDF.to_csv("AllStops.csv")
        # startTime = journey.iloc[0].TimeF
        # startStop = journey.iloc[0].StopID
        # endTime = journey.iloc[-1].TimeF
        # endStop = journey.iloc[-1].StopID
        # x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp
        # duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')

stopsDF.to_csv("./ProducedData/AllStops.csv")
            # In[12]:


            # display(HTML(journeysDF.head().to_html()))


            # In[15]:


            # print(journeysDF.shape[0])


            # In[ ]:
