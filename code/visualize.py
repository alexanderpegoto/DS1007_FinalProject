import matplotlib.pyplot as plt
import seaborn as sns


def boxplot(dat, xvar, yvar, title, xlabel, ylabel, x_order = None):
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
    x_order : list, optional
        The desired order of categories on the X-axis.
    """
    plt.figure(figsize = (10,10))
    sns.boxplot(x= xvar, y= yvar, data = dat, palette='Set3', order = x_order)
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

def plot_bar(data, x, y, title, xlabel, ylabel):
    """
    Plots a bar chart for the given data.

    Parameters:
    ----------
    data : pd.DataFrame
        DataFrame containing the data to plot.
    x : str
        Column name for the x-axis.
    y : str
        Column name for the y-axis.
    title : str
        Title of the chart.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    color : str, optional
        Bar color (default is 'blue').

    Returns:
    -------
    None
    """
    plt.figure(figsize=(8, 5))
    plt.bar(data[x], data[y], color='blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def barplot_with_annotations(data, x, mean_col, median_col, title, xlabel, ylabel):
    """
    Plots a combined bar chart with mean and median values and adds annotations.

    Parameters:
    ----------
    data : pd.DataFrame
        The dataset containing the values for the plot.
    x : str
        The column name for the x-axis (categorical variable).
    mean_col : str
        The column name for the mean values.
    median_col : str
        The column name for the median values.
    title : str
        Title of the chart.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    """
    plt.figure(figsize=(12, 8))

    # Plot Mean Fare
    mean_bars = sns.barplot(data=data, x=x, y=mean_col, color='skyblue', label='Mean Fare')

    # Overlay Median Fare as a barplot
    median_bars = sns.barplot(data=data, x=x, y=median_col, color='lightgreen', label='Median Fare')

    # Fetch the bar positions
    mean_positions = [bar.get_x() + bar.get_width() / 2 for bar in mean_bars.patches]
    median_positions = [bar.get_x() + bar.get_width() / 2 for bar in median_bars.patches]

    # Add annotations for mean and median values
    for idx, (mean_height, median_height) in enumerate(zip(data[mean_col], data[median_col])):
        # Annotate Mean Fare
        plt.text(mean_positions[idx], mean_height + 1, f"${mean_height:.2f}", ha='center', fontsize=10, color='blue')

        # Annotate Median Fare
        plt.text(median_positions[idx], median_height + 1, f"${median_height:.2f}", ha='center', fontsize=10, color='green')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(title='Fare Type')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
