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
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    print("Linear Regression Results:")
    print(f"R^2 Score: {r2_score(y_test, y_pred):.2f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.2f}")
    print("Feature Coefficients:", dict(zip(features, lr.coef_)))

    # Using statsmodels for p-values
    X_train_sm = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train_sm).fit()
    print(model.summary())
    return lr, model.summary()
