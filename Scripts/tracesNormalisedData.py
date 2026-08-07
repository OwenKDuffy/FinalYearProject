"""Display figure of normalised traces"""

import sys
import plotly.graph_objects as go
import pandas as pd


def main(input_file):
    """Take an input file and display the normalised data as figure"""
    df_stops = pd.read_csv("StopsCoordsJS.csv")

    df_journeys = pd.read_csv(input_file)
    df_journeys = df_journeys.sort_values("StdDev", ascending=False)
    max_std_dev = df_journeys["StdDev"].max()
    min_std_dev = df_journeys["StdDev"].min()
    df_journeys = df_journeys.head(20)
    print(df_journeys)

    stops_longs = []
    stops_lats = []
    names = []
    colours = []
    for i in range(df_journeys.shape[0]):
        start_stop = df_journeys["Stop1"][i]
        end_stop = df_journeys["Stop2"][i]
        start_stop_coords = df_stops[df_stops["StopID"] == start_stop]
        end_stop_coords = df_stops[df_stops["StopID"] == end_stop]
        # print(endStopCoords)
        if start_stop_coords.shape[0] != 0 and end_stop_coords.shape[0] != 0:
            stops_longs.append(
                [start_stop_coords.iloc[0].Longitude, end_stop_coords.iloc[0].Longitude]
            )
            stops_lats.append(
                [start_stop_coords.iloc[0].Latitude, end_stop_coords.iloc[0].Latitude]
            )
            names.append([str(int(start_stop)), str(int(end_stop))])
            # myColor = new Color(2.0f * x, 2.0f * (1 - x), 0);
            colour_values_mapped = (
                (df_journeys["StdDev"][i] - min_std_dev) / (max_std_dev - min_std_dev)
            ) * 255
            red = min(255, 2 * colour_values_mapped)
            green = min(255, 2 * (255 - colour_values_mapped))
            colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))

    fig = go.Figure(
        go.Scattermapbox(
            mode="markers+lines",
            lon=stops_longs[0],
            lat=stops_lats[0],
            marker={"size": 10},
            text=names[0],
            hoverinfo="text",
            line={"color": colours[0]},
            name=str(names[0][0] + "->" + names[0][1]),
        )
    )

    for j in range(1, len(stops_longs)):
        lo = stops_longs[j]
        la = stops_lats[j]
        trace_name = names[j]
        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=lo,
                lat=la,
                marker={"size": 10},
                text=trace_name,
                hoverinfo="text",
                line={"color": colours[j]},
                name=str(trace_name[0] + "->" + trace_name[1]),
            )
        )

    fig.update_layout(
        legend=dict(
            title=str(
                "Most Variable Journeys " + input_file[-6:-4] + "/" + input_file[-8:-6]
            ),
            x=0,
            y=1,
            traceorder="normal",
            font={"family":"sans-serif", "size":12, "color":"black"},
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        ),
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "style": "stamen-terrain",
            "center": {"lon": -6.2, "lat": 53.34},
            "zoom": 10,
        },
    )

    fig.show()


if __name__ == "__main__":
    main(sys.argv[1])
