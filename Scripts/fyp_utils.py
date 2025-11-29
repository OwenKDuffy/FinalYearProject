"""Utility functions for fyp scripts"""
from datetime import datetime
import pandas as pd

def ticks_to_timestamp(ticks: int) -> str:
    """Takes ticks, divides by 1 million and formats as datetime string"""
    datetime.fromtimestamp(ticks / 1_000_000).strftime("%Y-%m-%d %H:%M:%S")

def read_data_set(file_name: str) -> pd.DataFrame:
    """Return Pandas Dataframe with the correct column names for the input data"""
    return pd.read_csv(
        file_name,
        names=[
            "Timestamp",
            "LineID",
            "Direction",
            "JourneyPatternID",
            "TimeFrame",
            "VehicleJourneyID",
            "Operator",
            "Congestion",
            "Long",
            "Lat",
            "Delay",
            "BlockID ",
            "VehicleID",
            "StopID",
            "AtStop",
        ],
        dtype={"LineID": "str"},
    )
