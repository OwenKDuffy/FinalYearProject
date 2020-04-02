import os
import pandas as pd


directory_in_str = os.getcwd() + '/Datasets'
print(directory_in_str)
directory = os.fsencode(directory_in_str)
#
for file in os.listdir(directory):
    filename = directory_in_str + '/' + file.decode("utf-8")
    data = pd.read_csv(filename, names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})
    print(data.shape[0])
