import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from IPython.display import display, HTML

    return HTML, display, pd, plt


@app.cell
def _(pd):
    #reading in data
    stopVariability = pd.read_csv("../ProducedData/variabilityBetweenStops.csv")
    stopCoords = pd.read_csv("../ProducedData/stopCoords.csv")
    return stopCoords, stopVariability


@app.cell
def _(HTML, display, stopVariability):
    stopVariability_1 = stopVariability.sort_values('StdDev', ascending=False)
    topTenHighestVariable = stopVariability_1.head(10)
    display(HTML(topTenHighestVariable.to_html()))
    return (topTenHighestVariable,)


@app.cell
def _(HTML, display, stopCoords, topTenHighestVariable):
    highVariableStops = list(set(topTenHighestVariable.Stop1.unique()) | set(topTenHighestVariable.Stop2.unique()))
    highestVariableStopsCoords = stopCoords[stopCoords["StopID"].isin(highVariableStops)]
    froms = stopCoords[stopCoords["StopID"].isin(topTenHighestVariable.Stop1)]
    tos = stopCoords[stopCoords["StopID"].isin(topTenHighestVariable.Stop2)]
    BBox = ((highestVariableStopsCoords.Long.min(), highestVariableStopsCoords.Long.max(), highestVariableStopsCoords.Lat.min(), highestVariableStopsCoords.Lat.max()))

    print(BBox)
    display(HTML(froms.to_html()))
    display(HTML(tos.to_html()))
    return BBox, froms, tos


@app.cell
def _(BBox, froms, plt, tos):
    mapImg = plt.imread('../Images/map.png')
    #drawing plot
    fig, ax = plt.subplots(figsize = (24,21))
    ax.scatter(froms.Long, froms.Lat, zorder=1, alpha= 1, c='r', s=100)
    ax.scatter(tos.Long, tos.Lat, zorder=1, alpha= 1, c='b', s=100)
    ax.set_title('Most Variable Bus Stops in Dublin')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(mapImg, zorder=0, extent = BBox, aspect= 'equal')
    return


if __name__ == "__main__":
    app.run()
