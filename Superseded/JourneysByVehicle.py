import pandas as pd
from datetime import datetime

#Timestamp micro since 1970 01 01 00:00:00 GMT','Line ID','Direction','Journey Pattern ID','Time Frame (The start date of the production time table - in Dublin the production time table starts at 6am and ends at 3am)'Vehicle Journey ID (A given run on the journey pattern)'Operator (Bus operator, not the driver)'Congestion [0=no,1=yes]'Lon WGS84','Lat WGS84','Delay (seconds, negative if bus is ahead of schedule)'Block ID (a section ID of the journey pattern)'Vehicle ID','Stop ID','At Stop [0=no,1=yes]
data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])

vehicles = data.VehicleID.unique()
journeysDF = pd.DataFrame()
# for v in vehicles[0]:
v = vehicles[0]
pings = data[data.VehicleID == v]
output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop']].copy()
output['Timestamp'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
output.to_csv("Vehicle" + str(v) + "Journeys.csv")
