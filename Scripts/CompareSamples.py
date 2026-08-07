"""Compares two datasets"""
import sys
import plotly.graph_objects as go
import pandas as pd


def main(dataset1, dataset2):
    """Compares two datasets"""
    df_stops = pd.read_csv(
        "./Produced_data/Stops_coordsJS.csv", dtype={"StopID": "int32"}
    )
    # print(df_stops.head())

    df_1 = pd.read_csv(
        dataset1
    )  # , dtype = {'Stop1': 'int32', 'Stop2': 'int32', 'Stop3': 'int32'})
    df_2 = pd.read_csv(dataset2)  # , dtype = {'Stop1': 'int32', 'Stop2': 'int32'})
    df_1 = df_1.sort_values("Std_dev", ascending=False)
    df_2 = df_2.sort_values("Std_dev", ascending=False)
    max_std_dev_df2 = df_2["Std_dev"].max()
    min_std_dev_df2 = df_2["Std_dev"].min()
    df_2 = df_2.head(10)
    df_1 = df_1.head(10)

    # print(df_2)

    stops_longs = []
    stops_lats = []
    names = []
    colours = []
    for i in range(df_2.shape[0]):
        start_stop = df_2["Stop1"][i]
        start_stop_coords = df_stops[df_stops["StopID"] == start_stop]
        mid_stop = None
        if "Stop3" in df_2.columns:
            mid_stop = df_2["Stop2"][i]
            mid_stop_coords = df_stops[df_stops["StopID"] == mid_stop]
            end_stop = df_2["Stop3"][i]
        else:
            end_stop = df_2["Stop2"][i]
        end_stop_coords = df_stops[df_stops["StopID"] == end_stop]
        if start_stop_coords.shape[0] != 0 and end_stop_coords.shape[0] != 0:
            # print(str(start_stop) + "->" + str(end_stop))
            stops_longs.append(
                [start_stop_coords.iloc[0].Longitude, end_stop_coords.iloc[0].Longitude]
            )
            stops_lats.append(
                [start_stop_coords.iloc[0].Latitude, end_stop_coords.iloc[0].Latitude]
            )
            this_name = [str(int(start_stop))]
            if mid_stop is not None:
                this_name.append(str(int(mid_stop)))
            this_name.append(str(int(end_stop)))
            names.append(this_name)
            # my_color = new Color(2.0f * x, 2.0f * (1 - x), 0);
            colour_values_mapped = (
                (df_2["Std_dev"][i] - min_std_dev_df2) / (max_std_dev_df2 - min_std_dev_df2)
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
            lat=stops_lats[0],
            marker={"size": 10},
            text=names[0],
            hoverinfo="text",
            line={"color": "blue"},
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
    for i in range(df_1.shape[0]):
        start_stop = df_1["Stop1"][i]
        start_stop_coords = df_stops[df_stops["StopID"] == start_stop]
        mid_stop_coords = []
        mid_stop = []
        if "Stop3" in df_1.columns:
            mid_stop = df_1["Stop2"][i]
            mid_stop_coords = df_stops[df_stops["StopID"] == mid_stop]
            end_stop = df_1["Stop3"][i]
        else:
            end_stop = df_1["Stop2"][i]
        end_stop_coords = df_stops[df_stops["StopID"] == end_stop]
        if (
            start_stop_coords.shape[0] != 0
            and (mid_stop_coords.shape[0] != 0)
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
            this_name = [str(int(start_stop))]
            if mid_stop is not None:
                this_name.append(str(int(mid_stop)))
            this_name.append(str(int(end_stop)))
            names.append(this_name)
            colour_values_mapped = (
                (df_1["Std_dev"][i] - min_std_dev_df2) / (max_std_dev_df2 - min_std_dev_df2)
            ) * 255
            red = min(255, 2 * colour_values_mapped)
            green = min(255, 2 * (255 - colour_values_mapped))
            colours.append(str("rgb(" + str(int(red)) + "," + str(green) + ",0)"))
        else:
            print("Start_stop: " + str(start_stop) + "Coords: " + str(start_stop_coords))
            print("mid_stop: " + str(mid_stop) + "Coords: " + str(mid_stop_coords))
            print("end_stop: " + str(end_stop) + "Coords: " + str(end_stop_coords))

    for i in enumerate(stops_longs):
        lo = stops_longs[i]
        la = stops_lats[i]
        trace_name = names[i]
        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=lo,
                lat=la,
                marker=dict(size=10),
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
    main(sys.argv[1], sys.argv[2])
