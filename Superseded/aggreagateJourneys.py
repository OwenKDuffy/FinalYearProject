"""
Aggregate all journeys test
"""

from datetime import datetime
import pandas as pd

# Timestamp micro since 1970 01 01 00:00:00 GMT',
# 'Line ID',
# 'Direction',
# 'Journey Pattern ID',
# 'Time Frame (The start date of the production time table
#   - in Dublin the production time table starts at 6am and ends at 3am)'
# Vehicle Journey ID (A given run on the journey pattern)
# 'Operator (Bus operator, not the driver)
# 'Congestion [0=no,1=yes]
# 'Lon WGS84',
# 'Lat WGS84',
# 'Delay (seconds, negative if bus is ahead of schedule)
# 'Block ID (a section ID of the journey pattern)
# 'Vehicle ID',
# 'Stop ID',
# 'At Stop [0=no,1=yes]

data = pd.read_csv(
    "./Datasets/siri.20121106.csv",
    names=[
        "Timestamp",
        "LineID",
        "Direction",
        "JourneyPatternID",
        "TimeFrame",
        "VehicleJourneyID",
        "Operator",
        "Congestion",
        "Long",
        "Lat",
        "Delay",
        "BlockID ",
        "VehicleID",
        "StopID",
        "AtStop",
    ],
    dtype={"LineID": "str"},
)
journeys = data.VehicleJourneyID.unique()
journeys_df = pd.DataFrame(
    columns=[
        "JourneyID",
        "Route",
        "StartTimeF",
        "EndtimeF",
        "JourneyTime",
        "Duration",
    ]
)
# for j in journeys:
j = journeys[0]
pings = data[data.VehicleJourneyID == j]
pings.sort_values(by=['Timestamp'])
# print(pings)
# pings.to_csv("j.csv")
startTime = datetime.fromtimestamp(pings.iloc[0].Timestamp / 1_000_000)
startTimeF = startTime.strftime("%Y-%m-%d %H:%M:%S")
endTime = datetime.fromtimestamp(pings.iloc[-1].Timestamp / 1_000_000)
endTimeF = endTime.strftime("%Y-%m-%d %H:%M:%S")
journeyTime = endTime - startTime
journeyDuration = journeyTime.total_seconds()
route = pings.iloc[0].LineID
journeys_df.loc[len(journeys_df)] = [
                    j,
                    route,
                    startTimeF,
                    endTimeF,
                    journeyTime,
                    journeyDuration,
                ]
# print(data.head)
print(journeys_df)
journeys_df.to_csv("Journeys.csv")
