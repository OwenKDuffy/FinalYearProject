#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from datetime import datetime
from IPython.display import display, HTML
import sys
sys.path.append('../')

# #Timestamp micro since 1970 01 01 00:00:00 GMT',
# 'Line ID',
# 'Direction',
# 'Journey Pattern ID',
# 'Time Frame (The start date of the production time table - in Dublin the production time table starts at 6am and ends at 3am),
# 'Vehicle Journey ID (A given run on the journey pattern)'Operator (Bus operator, not the driver),
# 'Congestion [0=no,1=yes]',
# 'Lon WGS84',
# 'Lat WGS84',
# 'Delay (seconds, negative if bus is ahead of schedule),
# 'Block ID (a section ID of the journey pattern),
# 'Vehicle ID',
# 'Stop ID',
# 'At Stop [0=no,1=yes]

stopsDF = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])


data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})

data = data.head(500000)
# In[11]:

stretchLength = 3
vehicles = data.VehicleID.unique()

for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    for j in journeys:
        journey = output[(output['VehicleJourneyID'] == j) & (output['AtStop']== 1)]
        if(journey.shape[0] != 0):
            journey = journey.drop_duplicates(subset ="StopID",
                     keep = 'first')
            route = journey.iloc[0].LineID

            for i in range(0, journey.shape[0] - stretchLength):
                firstStop = journey.iloc[i].StopID
                firstStopTime = journey.iloc[i].Timestamp
                secondStop = journey.iloc[i + 1].StopID
                secondStopTime = journey.iloc[i + 1].Timestamp
            #     if(secondStop != firstStop):
            #         for j in range(i + 1, journey.shape[0]):
                thirdStopTime = journey.iloc[i + 2].Timestamp
                thirdStop = journey.iloc[i + 2].StopID
                        # if(secondStop != thirdStop):
                stopsDF = stopsDF.append({'StopA': firstStop, 'StopB': secondStop,'StopC': thirdStop, 'JourneyID': j, 'Route': route, 'StartTime': datetime.utcfromtimestamp(firstStopTime/1000000).strftime('%H:%M:%S'), 'EndTime': datetime.utcfromtimestamp(thirdStopTime/1000000).strftime('%H:%M:%S'), 'Duration': (thirdStopTime - firstStopTime)/1000000}, ignore_index = True)
            #                 break
                # firstStop = secondStop
                # firstStopTime = secondStopTime

        #         firstStop = sampleStop
        #         firstStopTime = sampleStopTime
        #
        # # journeysDF = journeysDF.append({'JourneyID': j, 'Route': route, 'StartTime': startTime, 'FromStop': startStop, 'Endtime': endTime, 'toStop': endStop, 'Duration': duration, 'RawDuration' : x/1000000}, ignore_index = True)
        # stopsDF.to_csv("AllStops.csv")
        # startTime = journey.iloc[0].TimeF
        # startStop = journey.iloc[0].StopID
        # endTime = journey.iloc[-1].TimeF
        # endStop = journey.iloc[-1].StopID
        # x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp
        # duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')

stopsDF.to_csv("AllTriplesStops.csv")
            # In[12]:


            # display(HTML(journeysDF.head().to_html()))


            # In[15]:


            # print(journeysDF.shape[0])


            # In[ ]:
