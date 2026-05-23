import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    from datetime import datetime
    import math
    from IPython.display import display, HTML

    return datetime, pd


@app.cell
def _(pd):
    data = pd.read_csv("../Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})
    return (data,)


@app.cell
def _(data, pd):
    vehicles = data.VehicleID.unique()
    journeysDF = pd.DataFrame()
    # v = vehicles[0]
    journeysByVehicle = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
    return journeysByVehicle, vehicles


@app.cell
def _(data, datetime, journeysByVehicle, pd, vehicles):
    for _v in vehicles:
        _pings = data[data.VehicleID == _v]
        output = _pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
        output['TimeF'] = _pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x / 1000000).strftime('%Y-%m-%d %H:%M:%S'))
        _journeys = output.VehicleJourneyID.unique()
        for _j in _journeys:
            _journey = output[(output.VehicleJourneyID == _j) & (output.AtStop == 1)]
            if _journey.__len__ == 0:
                continue
            route = _journey.LineID.first
            startTime = _journey.TimeF.first
            stopAt = _journey.StopID.first
            for i in _journey:
                if i.StopID != stopAt:
                    interStopTime = pd.concat([interStopTime, pd.Dataframe({'From': stopAt, 'To': i.StopID, 'Time': startTime})])
            endTime = _journey.iloc[-1].TimeF
            x = _journey.iloc[-1].Timestamp - _journey.iloc[0].Timestamp
            journeysByVehicle_1 = journeysByVehicle.append({'JourneyID': _j, 'Route': route, 'StartTime': startTime, 'Endtime': endTime, 'Duration': x}, ignore_index=True)
    return (interStopTime,)


@app.cell
def _(data, datetime, vehicles):
    _v = vehicles[0]
    _pings = data[data.VehicleID == _v]
    output_1 = _pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output_1['Timestamp'] = _pings.Timestamp.apply(lambda x: datetime.fromtimestamp(x / 1000000).strftime('%Y-%m-%d %H:%M:%S'))
    return (output_1,)


@app.cell
def _(output_1):
    _journeys = output_1.VehicleJourneyID.unique()
    print
    _j = _journeys[0]
    _journey = output_1[(output_1.VehicleJourneyID == _j) & (output_1.AtStop == 1)]
    print(_journey)
    return


if __name__ == "__main__":
    app.run()
