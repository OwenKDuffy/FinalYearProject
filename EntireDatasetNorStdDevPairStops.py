import os
import pandas as pd
import threadedStdDevNormForStops as script

def main():
    directory_in_str = os.getcwd() + '/ProducedData/Pairstops'
    print(directory_in_str)
    directory = os.fsencode(directory_in_str)
    directory = os.listdir(directory)
    # print(directory[0])
    for file in directory:
        filename = directory_in_str + '/' + file.decode("utf-8")
        print("Calling on: " + filename)
        script.main(filename)
        # data = pd.read_csv(filename, names = ['Timestamp','LineID','Direction','JourneyPatternID','TimeFrame','VehicleJourneyID','Operator','Congestion','Long','Lat','Delay','BlockID ','VehicleID','StopID','AtStop'], dtype = {'LineID': 'str'})
        # print(data.shape[0])

if __name__ == '__main__':
    main()
