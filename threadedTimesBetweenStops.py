#!/usr/bin/env python
# coding: utf-8

# In[9]:
debug = False

def findJourneyTimes(procnum, data, vehicles):
    for v in vehicles:
        pings = data[data.VehicleID == v]
        output = pings[['LineID', 'Direction', 'JourneyPatternID', 'VehicleJourneyID', 'StopID', 'AtStop', 'Timestamp']].copy()
        output['TimeF'] = pings.Timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000000).strftime('%Y-%m-%d %H:%M:%S'))
        journeys = output.VehicleJourneyID.unique()
        for j in journeys:
            journey = output[(output['VehicleJourneyID'] == j) & (output['AtStop']== 1)]
            if(journey.shape[0] != 0):
                route = journey.iloc[0].LineID
                firstStop = journey.iloc[0].StopID
                firstStopTime = journey.iloc[0].Timestamp
                for i in range(1, journey.shape[0]):
                    sampleStop = journey.iloc[i].StopID
                    sampleStopTime = journey.iloc[i].Timestamp
                    if(sampleStop != firstStop):
                        stopsDF = stopsDF.append({'FromStop': firstStop, 'toStop': sampleStop, 'JourneyID': j, 'Route': route, 'StartTime': datetime.utcfromtimestamp(firstStopTime/1000000).strftime('%H:%M:%S'), 'EndTime': datetime.utcfromtimestamp(sampleStopTime/1000000).strftime('%H:%M:%S'), 'Duration': (sampleStopTime - firstStopTime)/1000000}, ignore_index = True)
                    firstStop = sampleStop
                    firstStopTime = sampleStopTime
def main():
    import pandas as pd
    from datetime import datetime
    from IPython.display import display, HTML


    # In[10]:
    # import os
    # directory_in_str = os.getcwd() + '/Datasets'
    # print(directory_in_str)
    stopsDF = pd.DataFrame(columns = ['FromStop', 'toStop', 'JourneyID','Route', 'StartTime', 'Endtime', 'Duration'])
    # directory = os.fsencode(directory_in_str)

    # for file in os.listdir(directory):
    #     filename = os.fsdecode(file)

    data = pd.read_csv("Datasets/siri.20121106.csv", names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})

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
        proc = multiprocessing.Process(target = findJourneyTimes, args = (s, data[data[VehicleID].isin(vehicles[startIndex:min(endIndex, numVehicles)])], vehicles[startIndex:min(endIndex, numVehicles)]))
        jobs.append(proc)
        proc.start()
        startIndex = endIndex
        endIndex = endIndex + vehiclesPerThread

    for j in jobs:
        j.join()
    if(debug == True):
	    print("Joined Threads")
    outputData = pd.DataFrame()

    for val in return_dict.values():
        outputData = outputData.append(val, ignore_index = True)

    outputData.to_csv("./ProducedData/AllStops.csv")

if __name__ == '__main__':
    main()



            # display(HTML(journeysDF.head().to_html()))


            # In[15]:


            # print(journeysDF.shape[0])


            # In[ ]:
