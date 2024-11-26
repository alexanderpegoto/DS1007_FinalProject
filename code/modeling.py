import pandas as pd 
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt

## Time Series Modeling - Trend, Seasonality decomposition 
def decompose(dat, column):
    """
    
    """
    dat[column] = pd.to_datetime(dat[column])
    dat.set_index(column, inplace = True)
    stl = STL(dat, seasonal = 7)
    result = stl.fit()
    plt.figure(figsize = (10,13))
    result.plot()
    plt.show()
    return result.seasonal


## Feature Importance 
## Linear Regression, Tree-based methods 