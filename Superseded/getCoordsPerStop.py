import pandas as pd

data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])

stopCoords = pd.DataFrame(columns = ["StopID", "Long", "Lat"])
atStops = data[data.AtStop == 1]
for s in atStops.StopID.unique():
    stopInstances = atStops[atStops.StopID == s]
    stopCoords = stopCoords.append({"StopID": s, "Long": stopInstances.Long.mean(), "Lat": stopInstances.Lat.mean()}, ignore_index = True)

stopCoords.to_csv("stopCoords.csv")
