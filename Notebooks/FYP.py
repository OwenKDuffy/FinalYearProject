import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    from datetime import datetime
    from IPython.display import display, HTML

    return HTML, datetime, display, pd


@app.cell
def _(pd):
    data = pd.read_csv("../Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])
    return (data,)


@app.cell
def _(data):
    data.shape[0]
    return


@app.cell
def _(data):
    vehicles = data.VehicleID.unique()
    print(len(vehicles))
    return (vehicles,)


@app.cell
def _(data, datetime, pd, vehicles):
    journeysDF = pd.DataFrame()
    v = vehicles[0]
    pings = data[data.VehicleID == v]
    print(len(pings.VehicleJourneyID.unique()))
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    return (output,)


@app.cell
def _(HTML, display, output):
    display(HTML(output.head(10).to_html()))
    return


@app.cell
def _(HTML, display, output):
    journeys = output.VehicleJourneyID.unique()
    display(HTML(output[output.VehicleJourneyID == journeys[1]].head(10).to_html()))
    return (journeys,)


@app.cell
def _(datetime, journeys, output, pd):
    o = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
    for j in journeys:
        journey = output[output.VehicleJourneyID == j]
        route = journey.iloc[0].LineID
        startTime = journey.iloc[0].TimeF
        endTime = journey.iloc[-1].TimeF
        x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp 
        duration = datetime.utcfromtimestamp(x/1000000).strftime('%H:%M:%S')
        o = pd.concat([o, pd.DataFrame({'JourneyID': [j], 'Route': [route], 'StartTime': [startTime], 'Endtime': [endTime], 'Duration': [duration]})], ignore_index = True)
    return (o,)


@app.cell
def _(HTML, display, o):
    display(HTML(o.to_html()))
    return


if __name__ == "__main__":
    app.run()
