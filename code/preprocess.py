import numpy as np
import pandas as pd
from pathlib import Path
import os

def merge_parquets(dir, output_file_name='data.parquet'):
    """
    Reads and merges all Parquet files into a single Pandas DataFrame. It saves this merged DataFrame in the data folder
    for posterior use.

    Parameters:
    ----------
    dir : str
        The directory path containing the `.parquet` files to be merged.
    output_file_name : str, optional
        The name of the output file where the merged data will be saved. Default is 'merged_data.parquet'.

    Returns:
    -------
    pd.DataFrame
        A merged DataFrame containing data from all `.parquet` files,
        with duplicate rows removed and filtered based on the `total_amount` column.
    """
    # setting appropriate file path
    data_dir = Path(dir)
    output_file_path = data_dir / output_file_name

    # Check if the merged file already exists
    if output_file_path.exists():
        print(f"{output_file_name} already exists. Loading the file...")
        return pd.read_parquet(output_file_path)

    # concatenate all the parquet files and merge them
    relevant_files = [
        parquet_file for parquet_file in data_dir.glob('*.parquet')
        if 'yellow_tripdata_' in parquet_file.name
    ]
    # Concatenate all relevant parquet files
    print("Concatenating all yellow_tripdata parquets...")
    full_data = pd.concat(
        pd.read_parquet(parquet_file) for parquet_file in relevant_files
    )
    full_data = full_data[full_data.columns[:-1]]

    # Remove duplicates and filter rows
    print("Removing duplicates and filtering invalid rows...")
    full_data.drop_duplicates(inplace=True)
    full_data = full_data[full_data['total_amount'] > 0]

    # Save the merged data to a Parquet file
    print(f"Saving merged data to {output_file_name}...")
    full_data.to_parquet(output_file_path)

    return full_data


def sample_dat(dat, prop, seed):
    """
    Samples a proportion of rows from the dataset.

    Parameters:
    ----------
    dat : pd.DataFrame
        The dataset to sample from.
    prop : float
        Proportion of rows to sample (0 < prop <= 1).
    seed : int
        Random seed for reproducibility.

    Returns:
    -------
    pd.DataFrame
        A sampled DataFrame.
    """
    # Set random seed
    np.random.seed(seed) # use seed = 1

    # Generate sample indices and return sampled data
    sample_idx = np.random.choice(np.arange(0, len(dat)), size = int(len(dat) * prop), replace=False)
    return dat.iloc[sample_idx]

def drop_missing_vals(dat, column):
    """
    Drops rows with missing values in a specified column.

    Parameters:
    ----------
    dat : pd.DataFrame
        The dataset to clean.
    column : str
        Column to check for missing values.

    Returns:
    -------
    pd.DataFrame
        A DataFrame with rows containing missing values in the specified column removed.
    """

    dat_na_dropped = dat[dat[column].notnull()]
    return dat_na_dropped


def extract_dt(date):
    """
    Extracts date components including month, hour, weekday name, and the raw date from a datetime field.

    Parameters:
    ----------
    date : pd.Series
        A pandas Series containing datetime values.

    Returns:
    -------
    tuple
        A tuple containing:
        - date : pd.Series
            The date component (YYYY-MM-DD)
        - month : pd.Series
            The month component (1–12)
        - hour : pd.Series
            The hour component (0–23)
        - weekname : pd.Series
            The day name
    """
    month = date.dt.month
    hour = date.dt.hour
    weekname = date.dt.day_name()
    date = date.dt.date

    return date, month, hour, weekname

def split_hours(hour):
    """
    Categorizes hours of the day into predefined time periods.

    Parameters:
    ----------
    hour : array-like
        A pandas Series or array containing hour values (0–23) representing the time of day.

    Returns:
    -------
    np.ndarray
        A numpy array with time period labels for each hour:
        - 1.Morning (6am-10am)
        - 2.Midday (10am - 4pm)
        - 3.Evening Rush (4pm - 7pm)
        - 4.Night (8pm - 5am)
    """
    conditions = [
    (hour >= 6) & (hour < 10),
    (hour >= 10) & (hour< 16),
    (hour >= 16) & (hour < 20),
    (hour >= 20) | (hour < 6)
]
    choices = ['1.Morning (6am-10am)', '2.Midday (10am - 4pm)', '3.Evening Rush (4pm - 7pm)', '4.Night (8pm - 5am)']
    return np.select(conditions, choices, default="Unknown")


def remove_outliers(group, column):
    """
    Removes outliers from a specified column using the IQR method.

    Parameters:
    ----------
    group : pd.DataFrame
        The dataset to remove outliers.
    column : str
        Column to remove outliers from.

    Returns:
    -------
    pd.DataFrame
        A DataFrame with outliers removed from the specified column.
    """
    Q1 = group[column].quantile(0.25)
    Q3 = group[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group[column] >= lower_bound) &
                 (group[column] <= upper_bound)]


def merge_with_weather(main_data, weather_path, save_path):
    """
    Merges the main dataset with weather data on date and hour, and saves the result locally.

    Parameters:
    ----------
    main_data : pd.DataFrame
        The main dataset (already cleaned and sampled).
    weather_path : str
        Path to the weather dataset.
    save_path : str
        Path to save the merged dataset.

    Returns:
    -------
    pd.DataFrame
        The merged dataset.
    """
    # Load weather data
    weather_df = pd.read_csv(weather_path, parse_dates=['time'])

    # Extract date and hour from both datasets
    main_data['date'] = main_data['tpep_pickup_datetime'].dt.date
    main_data['hour'] = main_data['tpep_pickup_datetime'].dt.hour
    weather_df['date'] = weather_df['time'].dt.date
    weather_df['hour'] = weather_df['time'].dt.hour

    # Merge datasets
    merged_data = pd.merge(main_data, weather_df, on=['date', 'hour'], how='inner')

    # Save the merged dataset locally
    merged_data.to_parquet(save_path, index=False)

    return merged_data


def temperature_categories(temperature):
    """
    Categorizes temperature values into defined ranges.

    Parameters:
    -----------
    temperature : array
        An array or series of temperature values (in °C) to be categorized.

    Returns:
    --------
    array
        A series or array with temperature categories:
        - 'Warm (>=15)' for temperatures 15°C and above.
    """
    conditions = [(temperature < 15),
                  (temperature >= 15)]
    choices = ['Cold/Moderate (<15)', 'Warm (>=15)']
    return np.select(conditions, choices, default='Unknown')

def categorize_weather(data, column_name, threshold=0):
    """
    Categorizes weather conditions based on precipitation values.

    Parameters:
    ----------
    data : pd.DataFrame
        DataFrame containing weather data.
    column_name : str
        Column name for precipitation data.
    threshold : float, optional
        Precipitation threshold to distinguish between categories (default is 0).

    Returns:
    -------
    pd.Series
        Categorical weather conditions.
    """
    return np.where(data[column_name] > threshold, "Precipitation", "No Precipitation (Clear)")

## Run below to remove outliers in trip distance, duration, and fares

# sampled_dat['time_duration_in_mins'] = (sampled_dat['tpep_dropoff_datetime'] - sampled_dat['tpep_pickup_datetime']).dt.seconds // 60
# sampled_dat['trip_distance_round'] = np.floor(sampled_dat['trip_distance'])

# sampled_dat2 = sampled_dat.groupby('trip_distance_round', group_keys=False).apply(lambda group: remove_outliers(group, 'total_amount'))
# sampled_dat2 = sampled_dat2.groupby('trip_distance_round', group_keys=False).apply(lambda group: remove_outliers(group, 'time_duration_in_mins'))
# sampled_dat2 = sampled_dat2.groupby('time_duration_in_mins', group_keys=False).apply(lambda group: remove_outliers(group, 'trip_distance_round'))


# Q3 Preprocessing
