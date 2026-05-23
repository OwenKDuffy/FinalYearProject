import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import datetime
    from IPython.display import display, HTML

    return HTML, datetime, display, pd


@app.cell
def _(HTML, display, pd):
    data = pd.read_csv("../Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {"LineID": str})
    display(HTML(data.head(10).to_html()))
    return (data,)


@app.cell
def _(HTML, data, datetime, display):
    data['Timestamp'] = data['Timestamp'].apply(lambda ticks: datetime.datetime.fromtimestamp(ticks/1_000_000))
    display(HTML(data.head(10).to_html()))
    return


if __name__ == "__main__":
    app.run()
