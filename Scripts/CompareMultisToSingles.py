"""
Compares files from ./Produced_data/Multistops/Normalised/
and ./Produced_data/Pairstops/Normalised/ for a particlar date specified
"""
import sys
import plotly.graph_objects as go
import pandas as pd

def main(date: str):
    """
    Compares files from ./Produced_data/Multistops/Normalised/
    and ./Produced_data/Pairstops/Normalised/ for a particlar date specified
    """
    df_stops = pd.read_csv(
        "./Produced_data/Stops_coordsJS.csv", dtype={"StopID": "int32"}
    )

    df_multi_journeys = pd.read_csv(
        ("./Produced_data/Multistops/Normalised/" + str(date) + ".csv"),
        dtype={"Stop1": "int32", "Stop2": "int32", "Stop3": "int32"},
    )
    df_journeys = pd.read_csv(
        ("./Produced_data/Pairstops/Normalised/" + str(date) + ".csv"),
        dtype={"Stop1": "int32", "Stop2": "int32"},
    )
    df_multi_journeys = df_multi_journeys.sort_values("Std_dev", ascending=False)
    df_journeys = df_journeys.sort_values("Std_dev", ascending=False)
    max_std_dev = df_journeys["Std_dev"].max()
    min_std_dev = df_journeys["Std_dev"].min()
    df_journeys = df_journeys.head(10)
    df_multi_journeys = df_multi_journeys.head(10)

    # print(df_journeys)

    stops_longs = []
    stops_longs = []
    names = []
    colours = []
    for i in range(df_journeys.shape[0]):
        start_stop = df_journeys["Stop1"][i]
        end_stop = df_journeys["Stop2"][i]
        start_stop_coords = df_stops[df_stops["StopID"] == start_stop]
        # mid_stop_coords = df_stops[df_stops["StopID"] == mid_stop]
        end_stop_coords = df_stops[df_stops["StopID"] == end_stop]
        if start_stop_coords.shape[0] != 0 and end_stop_coords.shape[0] != 0:
            stops_longs.append(
                [start_stop_coords.iloc[0].Longitude, end_stop_coords.iloc[0].Longitude]
            )
            stops_longs.append(
                [start_stop_coords.iloc[0].Latitude, end_stop_coords.iloc[0].Latitude]
            )
            names.append([str(int(start_stop)), str(int(end_stop))])
            colour_values_mapped = (
                (df_journeys["Std_dev"][i] - min_std_dev) / (max_std_dev - min_std_dev)
            ) * 255
            red = min(255, 2 * colour_values_mapped)
            green = min(255, 2 * (255 - colour_values_mapped))
            colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
        else:
            print("Start_stop: " + str(start_stop) + "Coords: " + str(start_stop_coords))
            print("end_stop: " + str(end_stop) + "Coords: " + str(end_stop_coords))

    fig = go.Figure(
        go.Scattermapbox(
            mode="markers+lines",
            lon=stops_longs[0],
            lat=stops_longs[0],
            marker={"size": 10},
            text=names[0],
            hoverinfo="text",
            line={"color": "blue"},
            name=str(names[0][0] + "->" + names[0][1]),
        )
    )

    for j in range(1, len(stops_longs)):
        lo = stops_longs[j]
        la = stops_longs[j]
        trace_name = names[j]
        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=lo,
                lat=la,
                marker={"size":10},
                text=trace_name,
                hoverinfo="text",
                line={"color": "blue"},
                name=str(trace_name[0] + "->" + trace_name[1]),
            )
        )

    stops_longs = []
    stops_lats = []
    names = []
    colours = []
    for i in range(df_multi_journeys.shape[0]):
        start_stop = df_multi_journeys["Stop1"][i]
        mid_stop = df_multi_journeys["Stop2"][i]
        end_stop = df_multi_journeys["Stop3"][i]
        start_stop_coords = df_stops[df_stops["StopID"] == start_stop]
        mid_stop_coords = df_stops[df_stops["StopID"] == mid_stop]
        end_stop_coords = df_stops[df_stops["StopID"] == end_stop]
        if (
            start_stop_coords.shape[0] != 0
            and mid_stop_coords.shape[0] != 0
            and end_stop_coords.shape[0] != 0
        ):
            stops_longs.append(
                [
                    start_stop_coords.iloc[0].Longitude,
                    mid_stop_coords.iloc[0].Longitude,
                    end_stop_coords.iloc[0].Longitude,
                ]
            )
            stops_lats.append(
                [
                    start_stop_coords.iloc[0].Latitude,
                    mid_stop_coords.iloc[0].Latitude,
                    end_stop_coords.iloc[0].Latitude,
                ]
            )
            names.append([str(int(start_stop)), str(int(mid_stop)), str(int(end_stop))])
            colour_values_mapped = (
                (df_multi_journeys["Std_dev"][i] - min_std_dev) / (max_std_dev - min_std_dev)
            ) * 255
            red = min(255, 2 * colour_values_mapped)
            green = min(255, 2 * (255 - colour_values_mapped))
            colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
        else:
            print("Start_stop: " + str(start_stop) + "Coords: " + str(start_stop_coords))
            print("mid_stop: " + str(mid_stop) + "Coords: " + str(mid_stop_coords))
            print("end_stop: " + str(end_stop) + "Coords: " + str(end_stop_coords))

    for i, stops_long in enumerate(stops_longs):
        lo = stops_long
        la = stops_lats[i]
        trace_name = names[i]
        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=lo,
                lat=la,
                marker={"size":10},
                text=trace_name,
                hoverinfo="text",
                line={"color": "red"},
                name=str(trace_name[0] + "->" + trace_name[1] + "->" + trace_name[2]),
            )
        )

    fig.update_layout(
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
