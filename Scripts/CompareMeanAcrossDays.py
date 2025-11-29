"""Todo docs"""

import os
import math
import sys
import multiprocessing
from multiprocessing import Manager
import pandas as pd


def get_mean_comparison(data, procnum, return_dict):
    """?"""
    # data = [Stop1, Stop2, Stop3,MeanTime,Day,Date]
    normalised_means = pd.DataFrame()
    for s1 in data.Stop1.unique():
        journeys_from_stop = data[data.Stop1 == s1]
        for s2 in journeys_from_stop.Stop2.unique():
            journeys_to_stop = journeys_from_stop[journeys_from_stop.Stop2 == s2]
            for s3 in journeys_to_stop.Stop3.unique():
                journeys_final_stop = journeys_to_stop[journeys_to_stop.Stop3 == s3]
                mean_time = journeys_final_stop.MeanTime.mean()
                journeys_final_stop["NormalisedMean"] = (
                    journeys_final_stop.MeanTime / mean_time
                )
                # if(journeysFinalStop.shape[0] >= 2):
                #     stanDev = stdev(journeysFinalStop.NormalisedDuration, meanTime)
                # else:
                #     stanDev = 0
                normalised_means = normalised_means.append(journeys_final_stop)
    return_dict[procnum] = normalised_means


def main(folder):
    """Reads from specified folder and compares mean traveltime across days"""
    days = pd.read_csv(
        "DaysofWeek.csv", index_col=0, squeeze=True, header=None
    ).to_dict()
    directory = os.listdir(os.fsencode(folder))
    full_data_set = pd.DataFrame()
    for file in directory:
        dataset = folder + "/" + file.decode("utf-8")
        # TODO: Make usable for Pairstops
        data = pd.read_csv(dataset, usecols=["Stop1", "Stop2", "Stop3", "MeanTime"])
        data["Day"] = days[file.decode("utf-8")[-12:]]
        data["Date"] = file.decode("utf-8")[-12:-4]
        full_data_set = full_data_set.append(data, ignore_index=True)

    mgr = Manager()
    return_dict = mgr.dict()
    num_threads = 50
    stops = full_data_set.Stop1.unique()
    num_stops = len(stops)
    stops_per_thread = math.ceil(num_stops / num_threads)
    start_index = 0
    end_index = stops_per_thread
    jobs = []

    for s in range(num_threads):
        proc = multiprocessing.Process(
            target=get_mean_comparison,
            args=(
                full_data_set[
                    full_data_set.Stop1.isin(
                        stops[start_index : min(end_index, num_stops)]
                    )
                ],
                s,
                return_dict,
            ),
        )
        jobs.append(proc)
        proc.start()
        start_index = end_index
        end_index = end_index + stops_per_thread

    for j in jobs:
        j.join()
        print("Joined Thread:" + str(j))
    output_data = pd.DataFrame()

    for val in return_dict.values():
        output_data = output_data.append(val, ignore_index=True)

    output_data.to_csv("../ProducedData/MeansByDay.csv")

if __name__ == "__main__":
    main(sys.argv[1])
