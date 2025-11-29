"""TODO:docs"""

import pandas as pd
import fyp_utils as fyp

stopsDF = pd.DataFrame(
    columns=[
        "FromStop",
        "toStop",
        "JourneyID",
        "Route",
        "StartTime",
        "Endtime",
        "Duration",
    ]
)

data = fyp.read_data_set("Datasets/siri.20121106.csv")

vehicles = data.VehicleID.unique()

for v in vehicles:
    pings = data[data.VehicleID == v]
    output = pings[
        [
            "LineID",
            "Direction",
            "JourneyPatternID",
            "VehicleJourneyID",
            "StopID",
            "AtStop",
            "Timestamp",
        ]
    ].copy()
    output["TimeF"] = pings.Timestamp.apply(fyp.ticks_to_timestamp)
    journeys = output.VehicleJourneyID.unique()
    for j in journeys:
        journey = output[(output["VehicleJourneyID"] == j) & (output["AtStop"] == 1)]
        if journey.shape[0] != 0:
            route = journey.iloc[0].LineID
            firstStop = journey.iloc[0].StopID
            firstStopTime = journey.iloc[0].Timestamp
            for i in range(1, journey.shape[0]):
                sampleStop = journey.iloc[i].StopID
                sampleStopTime = journey.iloc[i].Timestamp
                if sampleStop != firstStop:
                    stopsDF = stopsDF.append(
                        {
                            "FromStop": firstStop,
                            "toStop": sampleStop,
                            "JourneyID": j,
                            "Route": route,
                            "StartTime": fyp.ticks_to_timestamp(firstStopTime),
                            "EndTime": fyp.ticks_to_timestamp(sampleStopTime),
                            "Duration": (sampleStopTime - firstStopTime) / 1000000,
                        },
                        ignore_index=True,
                    )
                firstStop = sampleStop
                firstStopTime = sampleStopTime

stopsDF.to_csv("./ProducedData/AllStops.csv")
