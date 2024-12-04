import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm



## Time Series Modeling - Trend, Seasonality decomposition
def decompose(dat, column):
    """
    Decomposes a time series into its trend, seasonal, and residual components using STL decomposition.

    Parameters:
    -----------
    dat : pandas.DataFrame
        The input DataFrame containing the time series data.
    column : str
        The name of the column in the DataFrame that contains the datetime values.

    Returns:
    --------
    pandas.Series
        The seasonal component of the time series extracted using STL decomposition.

    """
    dat[column] = pd.to_datetime(dat[column])
    dat.set_index(column, inplace = True)
    stl = STL(dat, seasonal = 7)
    result = stl.fit()
    plt.figure(figsize = (15,15))
    result.plot()
    plt.xticks(rotation=45)
    plt.show()
    return result.seasonal


## Feature Importance
## Linear Regression, Tree-based methods
def linear_regression_model(data, features, target):
    """
    Perform linear regression and evaluate results.

    Parameters:
    ----------
    data : pd.DataFrame
        The dataset containing the features and target.
    features : list
        A list of feature column names.
    target : str
        The target column name.

    Returns:
    -------
    tuple
        The trained linear regression model and statsmodels summary.
    """

    # One-hot encoding for categorical variables
    data_encoded = pd.get_dummies(data, columns=['weather_category', 'temperature_cat', 'borough', 'time_of_day'], drop_first=True)
 
    # Select features and target
    X = data_encoded[features]
    y = data_encoded[target]
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Initialize the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluation
    print("Linear Regression Results:")
    print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}")
    print(f"R² Score: {r2_score(y_test, y_pred):.2f}")
    print("Feature Coefficients:")
    for feature, coef in zip(model.feature_names_in_, model.coef_):
        print(f"{feature}: {coef:.2f}")
    
    # Using statsmodels for additional evaluation
    X_train_sm = sm.add_constant(X_train)
    sm_model = sm.OLS(y_train, X_train_sm).fit()
    print(sm_model.summary())
    
    return model, sm_model.summary()