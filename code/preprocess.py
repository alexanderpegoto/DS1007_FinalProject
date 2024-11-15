import numpy as np
import pandas as pd 
from pathlib import Path 
import os 

def merge_parquets(dir):
    """
    Read and Merge all the parquet files 
    """
    data_dir = Path(dir)
    
    full_data = pd.concat(
        pd.read_parquet(parquet_file) 
        for parquet_file in data_dir.glob('*.parquet')
    )

    return full_data



