import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    from IPython.display import display, HTML
    from datetime import datetime

    return HTML, datetime, display, pd


@app.cell
def _(pd):
    data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'])
    return (data,)


@app.cell
def _(data):
    vehicles = data.VehicleID.unique()
    v = vehicles[0]
    return (v,)


@app.cell
def _(HTML, data, datetime, display, pd, v):
    pings = data[data.VehicleID == v]
    output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
    output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
    journeys = output.VehicleJourneyID.unique()
    print(journeys)
    j = journeys[3]
    o = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime','StartStop', 'Endtime', 'EndStop', 'Duration', 'RawDuration'])
    # for j in journeys:
    journey = output[(output['VehicleJourneyID'] == j)(output['AtStop']== 1)]
    # route = journey.iloc[0].LineID
    display(HTML(journey.to_html()))
    return


if __name__ == "__main__":
    app.run()
