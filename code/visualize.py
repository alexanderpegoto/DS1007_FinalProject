


## Visualization format 
## Title, axis labels, axis ticks, legend, gridlines (optional), 


def boxplot(dat, xvar, yvar, title, xlabel, ylabel):
    """
    
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
    
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def lineplot(x, y, title, xlabel, ylabel):
    """
    
    """
    plt.figure(figsize=(16, 8))
    plt.plot(x,y, color = 'blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation =45)
    plt.tight_layout()
    plt.show()