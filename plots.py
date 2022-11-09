import datetime
import numpy as np
from math import ceil
from ah.data import align
from ah.data import average
from ah.misc import decimal
from ah.data import replace_outliers
from ah.data import get_server_history
from ah.data import get_region_history

import warnings
warnings.filterwarnings("ignore")

PLUS_ONE_HOUR     = lambda dt:  dt + datetime.timedelta(hours=1)
PLUS_HALF_HOUR    = lambda dt:  dt + datetime.timedelta(minutes=30)
MINUS_ONE_HOUR    = lambda dt:  dt - datetime.timedelta(hours=1)
MINUS_HALF_HOUR   = lambda dt:  dt - datetime.timedelta(minutes=30)
MINUS_TWO_HOURS   = lambda dt:  dt - datetime.timedelta(hours=2)
MINUS_THREE_HOURS = lambda dt:  dt - datetime.timedelta(hours=3)
MINUS_FOUR_HOURS  = lambda dt:  dt - datetime.timedelta(hours=4)
SCALE_FACTOR = lambda prices:  100 if prices[-1] < 10000 else 10000


from matplotlib import pyplot as plt




def generate_figure(times: list, prices: list, quantities: list = None) -> plt.Figure:
    """
    Generates a figure from the given data.

    Parameters
    ----------
    `times`: List of times.
    `prices`: List of prices. Can be just one list, but needs to be enclosed in `[]`. If passing in two, server prices should be first.
    `quantities`: List of quantities. Default is `None`, meaning only price will be plotted. Note, only one list can be passed in for quantities.

    Returns
    -------
    A `matplotlib` figure.
    """
    global ylabel
    global serverYlabel
    if quantities is None:
        if not isinstance(prices[0], list):     # If only one list is passed in, then it's the server prices.
            scale = SCALE_FACTOR(prices)
            prices = [price/scale for price in prices]
            ylabel = "Price (silver)" if scale==100 else "Price (gold)"
            fig, ax = plt.subplots()
            ax.plot(times, prices)
            fig.set_linewidth(1.5)
            fig.set_edgecolor('#000000')
            ax.fill_between(times, prices, 0, alpha=0.2)
            ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', labelpad=20)
            ax.tick_params(axis='y', which='major', labelsize=11)
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax.set_xlim(MINUS_THREE_HOURS(times[0]), PLUS_ONE_HOUR(times[-1]))
            ax.set_ylim(min(prices)*0.6, max(prices)*1.3)
            ax.grid(axis='x', which='both', color='#000000', linewidth=0.5, linestyle='-', alpha=0)
            ax.grid(axis='y', which='both', color='#CCCCCC', linewidth=0.5, linestyle='-', alpha=0.5)
            return fig
        else:                                   # If two lists are passed in, then it's the server prices and region prices.
            serverPrices = prices[0]
            regionPrices = prices[1]
            serverScale = SCALE_FACTOR(serverPrices)
            regionScale = SCALE_FACTOR(regionPrices)
            serverPrices = [price/serverScale for price in serverPrices]
            regionPrices = [price/regionScale for price in regionPrices]
            serverYlabel = "Price (silver)" if serverScale==100 else "Price (gold)"
            regionYlabel = "Price (silver)" if regionScale==100 else "Price (gold)"
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            fig.set_linewidth(1.5)
            fig.set_edgecolor('#000000')
            ax1.plot(times, serverPrices, label='Server price')
            ax2.plot(times, regionPrices, label='Region price', color="#FF9B44")
            ax1.fill_between(times, serverPrices, 0, alpha=0.2)
            ax1.set_ylabel(serverYlabel, fontsize=14, fontweight='bold', labelpad=20)
            ax1.tick_params(axis='y', which='major', labelsize=11)
            ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)     # Hide the right y-axis.
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines + lines2, labels + labels2, loc=0, fontsize=10)
            ax1.set_xlim(MINUS_HALF_HOUR(times[0]), (times[-1]))
            ax1.set_ylim( min(min(serverPrices),min(regionPrices))*0.6, max(max(serverPrices),max(regionPrices))*1.3 )
            ax2.set_ylim( min(min(serverPrices),min(regionPrices))*0.6, max(max(serverPrices),max(regionPrices))*1.3 )
            ax1.grid(axis='x', which='both', color='#000000', linewidth=1.5, alpha=0)
            ax1.grid(axis='y', which='both', color='#CCCCCC', linewidth=0.5, linestyle='-', alpha=0.5)
            ax2.grid(False)
            return fig
    else:
        if isinstance(prices[0], list):
            print("\n>>> Error: If quantities are passed in, only one price list should be passed in.\n")
            return None
        else:
            scale = SCALE_FACTOR(prices)
            prices = [price/scale for price in prices]
            ylabel = "Price (silver)" if scale==100 else "Price (gold)"
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            fig.set_linewidth(1.5)
            fig.set_edgecolor('#000000')
            ax1.plot(times, prices, label='Price')
            ax2.plot(times, quantities, label='Quantity', color="#FF9B44")
            ax1.fill_between(times, prices, 0, alpha=0.2)
            ax1.set_ylabel(ylabel, fontsize=14, fontweight='bold', labelpad=20)
            ax1.tick_params(axis='y', which='major', labelsize=11)
            ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)     # Hide the right y-axis.
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines + lines2, labels + labels2, loc=0, fontsize=10)
            ax1.set_xlim(MINUS_TWO_HOURS(times[0]), PLUS_ONE_HOUR(times[-1]))
            ax1.set_ylim(min(prices)*0.6, max(prices)*1.3)
            ax2.set_ylim(min(quantities)*0.8, max(quantities)*5)
            ax1.grid(axis='x', which='both', color='#000000', linewidth=1.5, alpha=0)
            ax1.grid(axis='y', which='both', color='#CCCCCC', linewidth=0.5, linestyle='-', alpha=0.5)
            ax2.grid(False)
            return fig



def price(item: str, numDays: int = None, server: str = "Skyfury", faction: str = "Alliance", replaceOutliers: bool = False, threshold: int = 2) -> None:
    """
    Plots the price of an item over time.

    Parameters
    ----------
    `item`: The name of the item to plot.
    `numDays`: The number of days to plot. If `None`, then the default is 7 days.
    `server`: The name of the server to plot. If `None`, then the default is "Skyfury".
    `faction`: The faction of the server to plot. If `None`, then the default is "Alliance".
    `replaceOutliers`: If `True`, then outliers will be replaced with the median price. If `False`, then outliers will be left as is. If `None`, then the default is `False`.
    `threshold`: The threshold for the prices to be considered outliers (in standard deviations). If `None`, then the default is 2.
    """
    data = get_server_history(item, server, faction, numDays)
    times = data["times"]
    prices = data["prices"]
    mean = np.mean(prices)
    numDays = ((times[-1])-(times[0])).days + 1 if numDays is None else numDays
    if replaceOutliers:
        prices = replace_outliers(prices, threshold)
    fig = generate_figure(times, prices)
    fig.gca().set_title(f"{item}: last {numDays} days", fontsize=16, fontweight='bold', pad=25)

    unit = " s" if ylabel == "Price (silver)" else " g"
    fig.gca().text(0.01, 0.96, f"Mean: {(mean/SCALE_FACTOR(prices)):.2f}{unit}", transform=fig.gca().transAxes, fontsize=12, verticalalignment='top')

    return fig





def price_and_quantity(item: str, numDays: int = None, server: str = "Skyfury", faction: str = "Alliance", replaceOutliers: bool = False, threshold: int = 2) -> None:
    """
    Plots the price and quantity of an item over time.

    Parameters
    ----------
    `item`: The name of the item to plot.
    `numDays`: The number of days to plot. If `None`, then the default is 7 days.
    `server`: The name of the server to plot. If `None`, then the default is "Skyfury".
    `faction`: The faction of the server to plot. If `None`, then the default is "Alliance".
    `replaceOutliers`: If `True`, then outliers will be replaced with the median price. If `False`, then outliers will be left as is. If `None`, then the default is `False`.
    `threshold`: The threshold for the prices to be considered outliers (in standard deviations). If `None`, then the default is 2.
    """
    data = get_server_history(item, server, faction, numDays)
    numDays = numDays = ((data["times"][-1])-(data["times"][0])).days + 1 if numDays is None else numDays
    times = data["times"]
    prices = data["prices"]
    quantities = data["quantities"]
    if replaceOutliers:
        prices = replace_outliers(prices, threshold)
    fig = generate_figure(times, prices, quantities)
    fig.gca().set_title(f"{item}: last {numDays} days", fontsize=16, fontweight='bold', pad=25)
    
    return fig







def price_and_region(item: str, numDays: int = None, server: str = "Skyfury", faction: str = "Alliance", region: str = "US", replaceOutliers: bool = False, threshold: int = 3) -> None:
    """
    Plots the price of an item over time, along with the region price.

    Parameters
    ----------
    `item`: The name of the item to plot.
    `numDays`: The number of days to plot. If `None`, then the default is 7 days.
    `server`: The name of the server to plot. If `None`, then the default is "Skyfury".
    `faction`: The faction of the server to plot. If `None`, then the default is "Alliance".
    `region`: The region to plot. If `None`, then the default is "US".
    `replaceOutliers`: If `True`, then outliers will be replaced with the median price. If `False`, then outliers will be left as is. If `None`, then the default is `False`.
    `threshold`: The threshold for the prices to be considered outliers (in multiples of the price difference between server and region price). Default is 3.
    """
    serverData = get_server_history(item, server, faction, numDays)
    regionData = get_region_history(item, region, numDays)
    serverData, regionData = align(serverData, regionData)
    if replaceOutliers:
        from ah.misc import fix_bad_data
        regionData["prices"] = fix_bad_data(serverData["prices"], regionData["prices"], threshold)

    serverPrices = serverData["prices"]
    regionPrices = regionData["prices"]
    numDays = numDays = ((serverData["times"][-1])-(serverData["times"][0])).days + 1 if numDays is None else numDays
    fig = generate_figure(serverData["times"], [serverPrices, regionPrices])
    fig.gca().set_title(f"{item}: last {numDays} days", fontsize=16, fontweight='bold', pad=25)
    
    return fig
