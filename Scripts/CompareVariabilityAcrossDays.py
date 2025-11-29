"""Compare Variability acorss days"""
import sys
import os
import pandas as pd
import plotly.graph_objects as go


def main(folder):
    """Compare Variability acorss days"""
    # directory_in_str = os.getcwd() + '/Datasets'
    days = pd.read_csv(
        "DaysofWeek.csv", index_col=0, header=None
    ).to_dict()
    directory = os.listdir(os.fsencode(folder))
    variabilities = {}
    for file in directory:
        dataset = folder + "/" + file.decode("utf-8")
        data = pd.read_csv(dataset)
        data = data[data["NumJourneys"] >= 2]
        variabilities[file.decode("utf-8")] = data.StdDev.mean()

    x_axis_days = list((pd.Series(list(variabilities.keys()))).map(days))
    x_axis_dates = [x[-6:-4] for x in list(variabilities.keys())]
    x_axis = [str(day) + " " + str(date) for day, date in zip(x_axis_days, x_axis_dates)]
    fig = go.Figure(
        data=go.Scatter(x=x_axis, y=list(variabilities.values()), mode="lines+markers")
    )
    fig.update_layout(
        title="StdDev across All Interstop Trips per Day",
        xaxis_title="Day",
        yaxis_title="Mean Standard Deviation on Day",
    )

    fig.show()


if __name__ == "__main__":
    main(sys.argv[1])
