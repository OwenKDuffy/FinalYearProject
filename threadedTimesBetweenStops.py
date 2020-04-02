#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from datetime import datetime
import multiprocessing
from multiprocessing import Pool, Manager
import math

debug = False
# In[9]:
def main(argv):
    inputFile = argv
    outputFile = "./ProducedData/Pairstops/" + inputFile[(inputFile.index(".")+1):]
    if (debug == True):
        print("I: " + inputFile)
        print("O: " + outputFile)
    data = pd.read_csv(inputFile, names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})

    vehicles = data.VehicleID.unique()
    mgr = Manager()
    ns = mgr.Namespace()
    return_dict = mgr.dict()
    # ns.df = data
    stretchLength = 3
    numThreads = 50
    vehicles = data.VehicleID.unique()
    numVehicles = len(vehicles)
    vehiclesPerThread = math.ceil(numVehicles / numThreads)
    startIndex = 0
    endIndex = vehiclesPerThread
    jobs = []
    if(debug == True):
	    print("Finished Preprocess")
    for s in range(numThreads):
        if(debug == True):
	        print("Creating proc: " + str(s))
        proc = multiprocessing.Process(target = findJourneyTimes, args = (s, return_dict, data[data["VehicleID"].isin(vehicles[startIndex:min(endIndex, numVehicles)])], vehicles[startIndex:min(endIndex, numVehicles)]))
        jobs.append(proc)
        proc.start()
        startIndex = endIndex
        endIndex = endIndex + vehiclesPerThread

    for j in jobs:
        j.join()
    if(debug == True):
	    print("Joined Thread:" + str(j))
    outputData = pd.DataFrame()

    for val in return_dict.values():
        outputData = outputData.append(val, ignore_index = True)

    outputData.to_csv(outputFile)


def findJourneyTimes(procnum, return_dict, data, vehicles):
    stopsDF = pd.DataFrame(columns = ['FromStop', 'toStop', 'JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
    for v in vehicles:
        pings = data[data.VehicleID == v]
        output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
        output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
        journeys = output.VehicleJourneyID.unique()
        for j in journeys:
            journey = output[(output['VehicleJourneyID'] == j) & (output['AtStop']== 1)]
            if(journey.shape[0] != 0):
                journey = journey.drop_duplicates(subset ="StopID",
                keep = 'first')
                route = journey.iloc[0].LineID
                for i in range(0, journey.shape[0] - 1):
                    firstStop = journey.iloc[i].StopID
                    firstStopTime = journey.iloc[i].Timestamp
                    sampleStop = journey.iloc[i + 1].StopID
                    sampleStopTime = journey.iloc[i + 1].Timestamp
                    if(sampleStop != firstStop):
                        stopsDF = stopsDF.append({'FromStop': firstStop, 'toStop': sampleStop, 'JourneyID': j, 'Route': route, 'StartTime': datetime.utcfromtimestamp(firstStopTime/1000000).strftime('%H:%M:%S'), 'EndTime': datetime.utcfromtimestamp(sampleStopTime/1000000).strftime('%H:%M:%S'), 'Duration': (sampleStopTime - firstStopTime)/1000000}, ignore_index = True)
    return_dict[procnum] = stopsDF

if __name__ == '__main__':
    main()



            # display(HTML(journeysDF.head().to_html()))


            # In[15]:


            # print(journeysDF.shape[0])


            # In[ ]:
