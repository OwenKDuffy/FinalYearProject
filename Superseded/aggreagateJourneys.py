import pandas as pd
from datetime import datetime

#Timestamp micro since 1970 01 01 00:00:00 GMT','Line ID','Direction','Journey Pattern ID','Time Frame (The start date of the production time table - in Dublin the production time table starts at 6am and ends at 3am)'Vehicle Journey ID (A given run on the journey pattern)'Operator (Bus operator, not the driver)'Congestion [0=no,1=yes]'Lon WGS84','Lat WGS84','Delay (seconds, negative if bus is ahead of schedule)'Block ID (a section ID of the journey pattern)'Vehicle ID','Stop ID','At Stop [0=no,1=yes]
data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])
journeys = data.VehicleJourneyID.unique()
journeysDF = pd.DataFrame(columns = ['JourneyID', 'Route', 'StartTime', 'StartTimeF', 'Endtime', 'EndtimeF', 'JourneyTime', 'Duration'], index = ['JourneyID'])
# for j in journeys:
j = journeys[0]
pings = data[data.VehicleJourneyID == j]
# print(pings)
pings.to_csv("j.csv")
startTime = (pings.iloc[0].Timestamp)/1000000
startTimeF = datetime.utcfromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S')
endTime = (pings.iloc[-1].Timestamp)/1000000
endTimeF = datetime.utcfromtimestamp(endTime).strftime('%Y-%m-%d %H:%M:%S')
journeyTime = endTime - startTime
journeyDuration = datetime.utcfromtimestamp(journeyTime).strftime('%Y-%m-%d %H:%M:%S')
route = pings.iloc[0].LineID
journeysDF= journeysDF.append({'JourneyID': j, 'Route': route, 'StartTime': startTime, 'Endtime': endTime, 'StartTimeF': startTimeF, 'EndtimeF': endTimeF, 'JourneyTime': journeyTime, 'Duration': journeyDuration}, ignore_index = True)
# print(data.head)
print(journeysDF)
journeysDF.to_csv("Journeys.csv")
