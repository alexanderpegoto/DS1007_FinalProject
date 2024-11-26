def boxplot(dat, xvar, yvar, title, xlabel, ylabel):
    """
    Creates a boxplot to visualize the distribution of a variable across categories.

    Parameters:
    ----------
    dat : pd.DataFrame
        The input DataFrame containing the data for the plot.
    xvar : str
        The column name for the categorical variable on the X-axis.
    yvar : str
        The column name for the numerical variable on the Y-axis.
    title : str
        The title of the plot.
    xlabel : str
        The label for the X-axis.
    ylabel : str
        The label for the Y-axis.

    Returns:
    -------
    None
        Displays the boxplot.
    """
    plt.figure(figsize = (10,10))
    sns.boxplot(x= xvar, y= yvar, data = dat, palette='Set3')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis = 'y')
    plt.show()


def heatmap(data, title, xlabel, ylabel):
    """
    Creates a heatmap to visualize correlations or relationships in a 2D dataset.

    Parameters:
    ----------
    data : pd.DataFrame or np.ndarray
        The input data for the heatmap.
    title : str
        The title of the heatmap.
    xlabel : str
        The label for the X-axis.
    ylabel : str
        The label for the Y-axis.

    Returns:
    -------
    None
        Displays the heatmap.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def lineplot(x, y, title, xlabel, ylabel, use_seaborn = False, data = None, hue = None):
    """
     Creates a line plot to visualize trends or relationships between two variables.

    This function supports both Matplotlib and Seaborn plotting libraries, allowing for 
    grouped line plots with Seaborn's `hue` parameter.

    Parameters:
    ----------
    x : array-like or str
        The data for the X-axis. 
    y : array-like or str
        The data for the Y-axis. 
    title : str
        The title of the plot.
    xlabel : str
        The label for the X-axis.
    ylabel : str
        The label for the Y-axis.
    use_seaborn : bool, optional (default=False)
        Whether to use Seaborn for the plot. If True, additional arguments like `data` and `hue` are used.
    data : pd.DataFrame, optional
        The input DataFrame for Seaborn plots. Required if `use_seaborn` is True.
    hue : str, optional
        The column name in `data` for grouping in Seaborn plots. Ignored if `use_seaborn` is False.

    Returns:
    -------
    None
        Displays the line plot.
    """
    plt.figure(figsize=(16, 8))
    if use_seaborn:
        sns.lineplot(data=data,x=x,y=y,hue=hue, palette="tab10",linewidth=2)
        plt.legend(title=hue)
    else:
        plt.plot(x,y, color = 'blue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.xticks(rotation =45)
        plt.tight_layout()
        plt.show()