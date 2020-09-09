import pandas as pd

JS = pd.read_csv("StopsCoordsJS.csv", dtype = {"StopID": "int32"})
PY = pd.read_csv("stopCoordsPY.csv", usecols = [1,2,3] ,dtype = {"StopID": "int32"})
PY.rename({"Long": "Longitude", "Lat": "Latitude"}, axis = "columns", inplace = True)
print(len(PY.StopID.unique()))
PY = PY.drop_duplicates(subset ="StopID", keep = 'first')
print(len(PY.StopID.unique()))
haveStops = JS.index.unique()
print(len(haveStops))
print(len(PY.StopID.unique()) - len(haveStops))
PY = PY[~PY["StopID"].isin(haveStops)]
print(len(PY.StopID.unique()))
outputData = JS.append(PY)
print(len(outputData.StopID.unique()))
outputData.to_csv("StopsCoordsJS1.csv", index = False)
