"""
api.py
======

Functions that interface with the NexusHub API.
"""
import requests
from ah.misc import Datetime





def server_history(itemname: str, realm = "skyfury", faction = "alliance", timerange: int = None, convert_timezone = True, condensed = False, rounded = True) -> list:
    """
    Get historical price & quantity data for a particular item on a particular server.

    Parameters
    ----------
    `itemname`:   The standard name of the item to get data for.
    `realm`:   The server to get historical price data from.  Default is `skyfury`.
    `faction`:   The faction on the given realm.  Default is `alliance`.
    `timerange`:   The number of days worth of historical price data to retrieve.  If left as `None`, its entire history will be retrieved.
    `convert_timezone`:   Whether or not to convert the timestamps to the local timezone.  Default is `True`.
    `condensed`:   Whether or not to return the data in a condensed format (i.e., only the `marketValue` and `quantity` fields).  Default is `False`.
    `rounded`:   Whether or not to round the `marketValue`, `minBuyout`, and `quantity` fields to the nearest copper/integer.  Default is `True`.

    Returns
    -------
    List of dictionaries of the form:
    >>> [
    >>>     {
    >>>         "marketValue": 123456,
    >>>         "minBuyout": 123456,
    >>>         "quantity": 123456,
    >>>         "scannedAt": "MM-DD-YYYY HH:MM"
    >>>     },
    >>>     ...
    >>> ]
    """
    if not timerange:
        now = Datetime.now(rtype="datetime")
        timerange = (now.month-9)*30 + now.day + 2
    itemname = itemname.lower().replace(' ', '-')
    url = f"https://api.nexushub.co/wow-classic/v1/items/{realm.lower()}-{faction.lower()}/{itemname}/prices?timerange={timerange}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        if condensed:
            condensed_data = []
            for i in range(len(data)):
                condensed_data.append({
                    'marketValue': int(round(data[i]['marketValue'],0)) if rounded else data[i]['marketValue'],
                    'quantity': int(round(data[i]['quantity'],0)) if rounded else data[i]['quantity']
                })
            return condensed_data
        if convert_timezone:
            import datetime, pytz
            for i in range(len(data)):
                dt = datetime.datetime.strptime(data[i]['scannedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
                dt = dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
                data[i]['scannedAt'] = dt.strftime("%m-%d-%Y %H:%M")
                data[i]['scannedAt'] = datetime.datetime.strptime(data[i]['scannedAt'],"%m-%d-%Y %H:%M")
                # data[i]['scannedAt'] = datetime.datetime(data[i]['scannedAt'].year, data[i]['scannedAt'].month, data[i]['scannedAt'].day, data[i]['scannedAt'].hour, data[i]['scannedAt'].minute, 0)
        if rounded:
            for i in range(len(data)):
                data[i]['marketValue'] = int(round(data[i]['marketValue'],0))
                data[i]['minBuyout'] = int(round(data[i]['minBuyout'],0))
                data[i]['quantity'] = int(round(data[i]['quantity'],0))
        return data
    else: return {}










def region_history(itemname: str, region = "us", timerange: int = None, convert_timezone = True, condensed = False, rounded = True) -> list:
    """
    Get historical price & quantity data for a particular item for an entire region.

    Parameters
    ----------
    `itemname`:   The standard name of the item to get data for.
    `region`:   The region to get historical price data for.  Default is `us`.
    `timerange`:   The number of days worth of historical price data to retrieve.  If left as `None`, its entire history will be retrieved.
    `convert_timezone`:   Whether or not to convert the timestamps to the local timezone.  Default is `True`.
    `condensed`:   Whether or not to return the data in a condensed format (i.e., only the `marketValue` and `quantity` fields).  Default is `True`.
    `rounded`:   Whether or not to round the `marketValue`, `minBuyout`, and `quantity` fields to the nearest copper/integer.  Default is `True`.

    Returns
    -------
    List of dictionaries of the form:
    >>> [
    >>>     {
    >>>         "marketValue": 123456,
    >>>         "minBuyout": 123456,
    >>>         "quantity": 123456,
    >>>         "scannedAt": "MM-DD-YYYY HH:MM"
    >>>     },
    >>>     ...
    >>> ]
    """
    if not timerange:
        now = Datetime.now(rtype="datetime")
        timerange = (now.month-9)*30 + now.day + 2
    itemname = itemname.lower().replace(' ', '-')
    url = f"https://api.nexushub.co/wow-classic/v1/items/{region.lower()}/{itemname}/prices?timerange={timerange}&region=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"]
        if condensed:
            condensed_data = []
            for i in range(len(data)):
                condensed_data.append({
                    'marketValue': int(round(data[i]['marketValue'],0)) if rounded else data[i]['marketValue'],
                    'quantity': int(round(data[i]['quantity'],0)) if rounded else data[i]['quantity']
                })
            return condensed_data
        if convert_timezone:
            import datetime, pytz
            for i in range(len(data)):
                dt = datetime.datetime.strptime(data[i]['scannedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
                dt = dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
                data[i]['scannedAt'] = dt.strftime("%m-%d-%Y %H:%M")
                data[i]['scannedAt'] = datetime.datetime.strptime(data[i]['scannedAt'],"%m-%d-%Y %H:%M")
        if rounded:
            for i in range(len(data)):
                data[i]['marketValue'] = int(round(data[i]['marketValue'],0))
                data[i]['minBuyout'] = int(round(data[i]['minBuyout'],0))
                data[i]['quantity'] = int(round(data[i]['quantity'],0))
        return data
    else:
        print(response.status_code)
        return {}


