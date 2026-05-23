import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import plotly.graph_objects as go
    import pandas as pd

    df_stops = pd.read_csv('stopCoords.csv')
    print(df_stops.head())

    df_journeys = pd.read_csv('variabilityBetweenStops.csv')
    print(df_journeys.head())
    df_journeys = df_journeys.sort_values("StdDev", ascending = False)
    df_journeys = df_journeys.head(3)
    fig = go.Figure()
    return df_journeys, df_stops, fig, go


@app.cell
def _(df_journeys, df_stops, fig, go):
    fig.add_trace(go.Scattergeo(
        locations = ["Ireland"],
        locationmode = 'country names',
        lon = df_stops['Long'],
        lat = df_stops['Lat'],
        hoverinfo = 'text',
        text = df_stops['StopID'],
        mode = 'markers',
        marker = dict(
            size = 2,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))
    journey_path = []
    for i in range(len(df_journeys)):
        startStop = df_journeys["Stop1"][i]
        endStop = df_journeys["Stop2"][i]
        startLong = df_stops[df_stops["StopID"] == startStop].Long.values
        endLong = df_stops[df_stops["StopID"] == endStop].Long.values
        startLat = df_stops[df_stops["StopID"] == startStop].Lat.values
        endLat = df_stops[df_stops["StopID"] == endStop].Lat.values
        fig.add_trace(
            go.Scattergeo(
                locations = ["Ireland"],
                locationmode = 'country names',
                lon = [startLong, endLong],
                lat = [startLat, endLat],
                mode = 'lines',
                line = dict(width = 1,color = 'red'),
                opacity = float(df_journeys['StdDev'][i]) / float(df_journeys['StdDev'].max()),
            )
        )
        fig.update_layout(
        title_text = 'High Variabilty Bus Journeys<br>(Hover for stop Numbers)',
        showlegend = False,
        geo = dict(
            scope = 'europe',
            projection_type = 'azimuthal equal area',
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )

    fig.show()
    return


if __name__ == "__main__":
    app.run()
