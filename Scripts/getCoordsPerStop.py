import pandas as pd
import multiprocessing
from multiprocessing import Pool, Manager
import os
import math


def getAllStops(filename, procnum, return_dict):
    data = pd.read_csv(filename, usecols = [8, 9, 13, 14], names = ['Long','Lat','StopID','AtStop'])

    stopCoords = pd.DataFrame(columns = ["StopID", "Long", "Lat"])
    atStops = data[data.AtStop == 1]
    for s in atStops.StopID.unique():
        stopInstances = atStops[atStops.StopID == s]
        if(math.isnan(s)):
            print("NAN: " + str(s) + " in file: " + filename[-13:])
        else:
            stopCoords = stopCoords.append({"StopID": int(s), "Long": stopInstances.Long.mean(), "Lat": stopInstances.Lat.mean()}, ignore_index = True)
    return_dict[procnum] = stopCoords

def main():
    mgr = Manager()
    return_dict = mgr.dict()
    jobs = []
    folder = "./Datasets"
    directory = os.fsencode(folder)
    directory = os.listdir(directory)
    for s in range(len(directory)):
        dataset = folder + '/' + directory[s].decode("utf-8")
        proc = multiprocessing.Process(target = getAllStops, args = (dataset, s, return_dict))
        jobs.append(proc)
        proc.start()
    for j in jobs:
        j.join()
        print("Joined Thread:" + str(j))


    outputData = pd.DataFrame()
    for val in return_dict.values():
        outputData = outputData.append(val, ignore_index = True)

    outputData = outputData.drop_duplicates(subset ="StopID", keep = 'first')
    outputData.to_csv("stopCoordsPY.csv")

if __name__ == '__main__':
    main()
