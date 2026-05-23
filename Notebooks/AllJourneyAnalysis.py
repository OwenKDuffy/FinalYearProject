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
def _(HTML, display):
    display(HTML("<style>.container { width:100% !important; }</style>"))
    return


@app.cell
def _(pd):
    data = pd.read_csv("../Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {"LineID": str})
    return (data,)


@app.cell
def _(HTML, data, display):
    display(HTML(data.head(10).to_html()))
    return


@app.cell
def _(data, datetime, pd):
    vehicles = data.VehicleID.unique()
    journeysDF = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime','StartStop', 'Endtime', 'EndStop', 'Duration'])
    for v in vehicles:
        pings = data[data.VehicleID == v]
        output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
        output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.fromtimestamp(x/1_000_000).strftime('%Y-%m-%d %H:%M:%S'))
        journeys = output.VehicleJourneyID.unique()
        o = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime','StartStop', 'Endtime', 'EndStop', 'Duration'])
        for j in journeys:
            journey = output[output.VehicleJourneyID == j]
            route = journey.iloc[0].LineID
            startTime = journey.iloc[0].TimeF
            startStop = journey.iloc[0].StopID
            endTime = journey.iloc[-1].TimeF
            endStop = journey.iloc[-1].StopID
            x = journey.iloc[-1].Timestamp - journey.iloc[0].Timestamp 
            duration = datetime.fromtimestamp(x/1_000_000).strftime('%H:%M:%S')
            journeysDF = pd.concat([journeysDF, pd.DataFrame({'JourneyID': [j], 'Route': [route], 'StartTime': [startTime], 'StartStop': [startStop], 'Endtime': [endTime], 'EndStop': [endStop], 'Duration': [duration]})], ignore_index = True)
    return (journeysDF,)


@app.cell
def _(HTML, display, journeysDF):
    display(HTML(journeysDF.head(10).to_html()))
    return


@app.cell
def _(journeysDF):
    print(journeysDF.shape[0])
    return


if __name__ == "__main__":
    app.run()
