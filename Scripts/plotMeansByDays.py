"""Take file ../ProducedData/MeansByDay.csv and plots to a graph"""
import pandas as pd
import plotly.graph_objects as go

def set_colour_by_day(day_string: str) -> str:
    """Returns colour string with red for weekend and blue for weekday"""
    if(day_string[:3] == "Sat" or day_string[:3] == "Sun"):
        return "red"
    return "blue"

def main():
    """Take file ../ProducedData/MeansByDay.csv and plots to a graph"""
    data = pd.read_csv("../ProducedData/MeansByDay.csv", usecols = {"Day", "Date", "NormalisedMean"})
    graph_data = {}
    dates = data.Date.unique()
    dates.sort()
    print(dates)
    for d in dates:
        this_day = data[data["Date"] == d]
        mean = this_day.NormalisedMean.mean()
        graph_data[this_day.Day.values[0][:3] + " " + str(d)[-2:] + "/" + str(d)[-4:-2]] = mean

    fig = go.Figure(data = go.Scatter(
        x = list(graph_data.keys()),
        y = list(graph_data.values()),
        mode='markers+lines',
        marker = {"size": 8, "color" : list(map(set_colour_by_day, list(graph_data.keys())))},
        line = {"color": "black"}))
    fig.update_layout(title='Mean Journey Time Comparisons',
                   xaxis_title = "Day",
                   yaxis_title = "Journey time as compared to mean")

    fig.show()


if __name__ == '__main__':
    main()
