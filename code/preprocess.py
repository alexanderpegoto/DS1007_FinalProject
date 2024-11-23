import numpy as np
import pandas as pd 
from pathlib import Path 
import os 

def merge_parquets(dir):
    """
    Read and Merge all the parquet files 
    """
    # setting appropriate file path 
    data_dir = Path(dir)
    
    # concatenate all the parquet files and merge them 
    full_data = pd.concat(
        pd.read_parquet(parquet_file) 
        for parquet_file in data_dir.glob('*.parquet')
    )
    full_data = full_data[full_data.columns[:-1]]
    # Make sure there are no duplicate rows in the dataset 
    full_data.drop_duplicates(inplace = True)
    full_data = full_data[full_data['total_amount'] > 0]
    return full_data


def sample_dat(dat, prop):
    """
    docstring 
    """
    # uniform sample of the indices 
    sample_idx = np.random.randint(0, len(dat), int(len(dat) * prop))
    return dat.iloc[sample_idx]

def drop_missing_vals(dat, column):
    """
    docstring
    """
    dat_na_dropped = dat[dat[column].notnull()] 
    return dat_na_dropped 


def extract_dt(date):
    """
    return month, hour, weekday of a date field 
    """
    month = date.dt.month
    hour = date.dt.hour 
    weekname = date.dt.day_name() 
    date = date.dt.date

    return date, month, hour, weekname 

def split_hours(hour):
    conditions = [
    (hour >= 6) & (hour < 10),
    (hour >= 10) & (hour< 16),
    (hour >= 16) & (hour < 20),
    (hour >= 20) | (hour < 6)
]
    choices = ['1.Morning (6am-10am)', '2.Midday (10am - 4pm)', '3.Evening Rush (4pm - 7pm)', '4.Night (8pm - 5am)']
    return np.select(conditions, choices)




### Create a function that would filter out the fare amount outliers 
## Filter for fare amount > 0 

def remove_outliers(group, column):
    Q1 = group[column].quantile(0.25)
    Q3 = group[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group[column] >= lower_bound) & 
                 (group[column] <= upper_bound)]

## Run below to remove outliers in trip distance, duration, and fares

# sampled_dat['time_duration_in_mins'] = (sampled_dat['tpep_dropoff_datetime'] - sampled_dat['tpep_pickup_datetime']).dt.seconds // 60
# sampled_dat['trip_distance_round'] = np.floor(sampled_dat['trip_distance'])

# sampled_dat2 = sampled_dat.groupby('trip_distance_round', group_keys=False).apply(lambda group: remove_outliers(group, 'total_amount'))
# sampled_dat2 = sampled_dat2.groupby('trip_distance_round', group_keys=False).apply(lambda group: remove_outliers(group, 'time_duration_in_mins'))
# sampled_dat2 = sampled_dat2.groupby('time_duration_in_mins', group_keys=False).apply(lambda group: remove_outliers(group, 'trip_distance_round'))
