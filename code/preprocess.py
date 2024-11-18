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
    return full_data


def sample_dat(dat, prop, seed):
    """
    docstring
    """
    # uniform sample of the indices
    np.random.seed(seed)
    sample_idx = np.random.randint(0, len(dat), int(len(dat) * prop))

    return dat.iloc[sample_idx]

def drop_missing_vals(dat, column):
    """
    docstring
    """
    dat_na_dropped = dat[dat[column].notnull()]
    return dat_na_dropped
