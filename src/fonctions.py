import os
import warnings
import requests
import datetime as dt
import pandas as pd
from src.dictionaries import (
    DATA_KEYS,
    URL_DICT,
)


def request_xr(
    fromtime: str = "",
    totime: str = "",
    folder: str = "",
    datatypes: str = "base",
    groups: str = "",
    sites: str = "",
    measures: str = ""
):
    """
    Get json objects from XR rest api

    input :
    -------
        fromtime : str
            Start time  in YYYY-MM-DDThh:mm:ssZ format
        totime : str
            End time  in YYYY-MM-DDThh:mm:ssZ format
        folder : str
            Url string to request XR rest api
            Default = "data"
        dataTypes : str,
            Time mean in base(15min), hour, day, month
            Default = "base"
        groups : str
            Site groupes
            Default = "DIDON"
        sites : str
            site or list of sites to retrive
            Default = "" (all sistes)
        measures : str
            list of measure ids
            Default : str
    return :
    --------
        csv : csv file
            File in ../data directory
    """
    url = (
        f"{URL_DICT[folder]}&"
        f"from={fromtime}&"
        f"to={totime}&"
        f"sites={sites}&"
        f"dataTypes={datatypes}&"
        f"groups={groups}&"
        f"measures={measures}"
    )

    # AVOID WARNING MESSAGE FOR CERTIFICATE SSL VERIFICATION
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        data = requests.get(url, verify=False).json()
    return data[DATA_KEYS[folder]]


def build_dataframe(data: dict, header: list):
    out_df = pd.DataFrame(columns=header)
    for i in range(len(data[:])):
        df = pd.DataFrame(data[i]['base'])

        df["id"] = data[i]["id"]

        for col in header:
            if col not in df.columns:
                df.insert(2, col, None)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            out_df = pd.concat([out_df, df],
                               join="inner",
                               ignore_index=True,
                               sort=False)

        out_df['date'] = pd.to_datetime(
            out_df['date'],
            format="%Y-%m-%dT%H:%M:%SZ"
            )

    return (out_df)


def get_pollsite_stats(data):
    moyenne_gliss = (
        data.dropna().groupby('id')
        .resample(
            'd',
            on='date',
            )
        .mean()
    )
    max_jour = (
        data.dropna().groupby('id')
        .resample(
            'd',
            on='date',
            )
        .max()
    )
    return (moyenne_gliss, max_jour)


def test_path(path: str, mode: str):

    if mode == "mkdir":
        if os.path.exists(path) is False:
            os.mkdir(path)
    if mode == "makedirs":
        if os.path.exists(path) is False:
            os.makedirs(path)
    if mode == "remove_file":
        if os.path.exists(path):
            os.remove(path)


def time_window(days=5):
    time_now = dt.datetime.now()
    time_delta = dt.timedelta(days)

    end_time = time_now.strftime(format="%Y-%mm-%ddT%HH:%MM:%SSZ")
    start_time = (time_now-time_delta).strftime(
        format="%Y-%mm-%ddT%HH:%MM:%SSZ"
    )
    return (start_time, end_time)


def float_none(v):
    """Convert into float or None."""
    if v is None:
        return None
    else:
        return float(v)


def test_valid(n):
    """ Return n of -999 if None. """
    if n is None:
        return -999
    else:
        return n


def list_of_days(start_date, end_date):
    """ List of days between two dates. """
    dates = []
    d = start_date
    while d < end_date:
        dates.append(d)
        d += dt.timedelta(days=1)
        return dates


def day_of_month(year, month):
    """ List of days in a month. """
    di = dt.date(year, month, 1)
    if month == 12:
        de = dt.date(year + 1, 1, 1)
    else:
        de = dt.date(year, month + 1, 1)
    return list_of_days(di, de)


def date_last_weekday(year, month, weekday):
    """ Date of the last weekday in a month. """
    dm = day_of_month(year, month)
    wd = [e.isoweekday() for e in dm]
    for i, e in enumerate(wd[::-1]):
        if e == weekday:
            return dm[::-1][i]
    return None
