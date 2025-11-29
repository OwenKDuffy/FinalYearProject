"""Run threadedTimesBetweenMultiStops on all files in Dataset in sequence"""
import os
import threadedTimesBetweenMultiStops as script

directory_in_str = os.getcwd() + '/Datasets'
directory = os.fsencode(directory_in_str)
directory = os.listdir(os.fsencode(directory_in_str))
for file in directory:
    filename = directory_in_str + '/' + file.decode("utf-8")
    print("Calling on: " + filename)
    script.main(filename)
