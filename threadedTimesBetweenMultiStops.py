import pandas as pd
from datetime import datetime
import multiprocessing
from multiprocessing import Pool, Manager
import math
import sys
debug = True
# In[9]:
def main(argv):
    # #Timestamp micro since 1970 01 01 00:00:00 GMT',
    # 'Line ID',
    # 'Direction',
    # 'Journey Pattern ID',
    # 'Time Frame (The start date of the production time table - in Dublin the production time table starts at 6am and ends at 3am),
    # 'Vehicle Journey ID (A given run on the journey pattern)'Operator (Bus operator, not the driver),
    # 'Congestion [0=no,1=yes]',
    # 'Lon WGS84',
    # 'Lat WGS84',
    # 'Delay (seconds, negative if bus is ahead of schedule),
    # 'Block ID (a section ID of the journey pattern),
    # 'Vehicle ID',
    # 'Stop ID',
    # 'At Stop [0=no,1=yes]
    inputFile = argv
    outputFile = "./ProducedData/Multistops/" + inputFile[(inputFile.index(".")+1):]
    if (debug == True):
        print("I: " + inputFile)
        print("O: " + outputFile)
    data = pd.read_csv(inputFile, names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})
    if(debug == True):
	    print("Read Data")
        # data = data.head(500)
    mgr = Manager()
    ns = mgr.Namespace()
    return_dict = mgr.dict()
    # ns.df = data
    stretchLength = 3
    numThreads = 50
    if(debug == True):
        data = data.head(500)
        numThreads = 5
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
        proc = multiprocessing.Process(target = findJourneyTimes, args = (s, return_dict, data, vehicles[startIndex:min(endIndex, numVehicles)]))
        jobs.append(proc)
        proc.start()
        startIndex = endIndex
        endIndex = endIndex + vehiclesPerThread

    for j in jobs:
        j.join()
        print("Joined Thread:" + str(j))
    outputData = pd.DataFrame()

    for val in return_dict.values():
        outputData = outputData.append(val, ignore_index = True)

    outputData.to_csv(outputFile)


def findJourneyTimes(procnum, return_dict, data, vehicles):
    stopsDF = pd.DataFrame(columns = ['JourneyID','Route', 'StartTime', 'EndTime', 'Duration'])
    if(debug == True):
	    print(vehicles)
    for v in vehicles:
        # if(debug == True):
	    #     print("Starting Vehicle: " + str(v))
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

                for i in range(0, journey.shape[0] - 3):
                    firstStop = journey.iloc[i].StopID
                    firstStopTime = journey.iloc[i].Timestamp
                    secondStop = journey.iloc[i + 1].StopID
                    secondStopTime = journey.iloc[i + 1].Timestamp
                    #     if(secondStop != firstStop):
                    #         for j in range(i + 1, journey.shape[0]):
                    thirdStopTime = journey.iloc[i + 2].Timestamp
                    thirdStop = journey.iloc[i + 2].StopID
                    # if(secondStop != thirdStop):
                    stopsDF = stopsDF.append({'StopA': firstStop, 'StopB': secondStop,'StopC': thirdStop, 'JourneyID': j, 'Route': route, 'StartTime': datetime.utcfromtimestamp(firstStopTime/1000000).strftime('%H:%M:%S'), 'EndTime': datetime.utcfromtimestamp(thirdStopTime/1000000).strftime('%H:%M:%S'), 'Duration': (thirdStopTime - firstStopTime)/1000000}, ignore_index = True)
    return_dict[procnum] = stopsDF

def testFunc(data, v):
    print(data.shape[0])
    print(v)

        # p = Pool(processes=numThreads)
        # ret = p.map(findJourneyTimes, data, [i for i in subVehicles])
        # p.close()
        # print(ret)
        # stopsDF.to_csv("AllTriplesStops.csv")

if __name__ == '__main__':
    main(sys.argv[1:])
