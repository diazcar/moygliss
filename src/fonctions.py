import os
import warnings
import requests
import datetime as dt
import pandas as pd
import numpy as np
from src.dictionaries import (
    DATA_KEYS,
    URL_DICT,
)


def request_xr(
    fromtime: str = "",
    totime: str = "",
    folder: str = "",
    datatype: str = "base",
    groups: str = "",
    sites: str = "",
    measures: str = "",
    header_for_df: list = None
) -> pd.DataFrame:
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
        f"dataTypes={datatype}&"
        f"groups={groups}&"
        f"measures={measures}"
    )

    # AVOID WARNING MESSAGE FOR CERTIFICATE SSL VERIFICATION
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        data = requests.get(url, verify=False).json()[DATA_KEYS[folder]]

    if header_for_df:
        data = build_dataframe(
            data=data,
            header=header_for_df,
            datatype=datatype
            )

    return (data)


def build_dataframe(data: dict, header: list, datatype: str) -> pd.DataFrame:
    out_df = pd.DataFrame(columns=header)
    for i in range(len(data[:])):
        df = pd.DataFrame(data[i][datatype]['data'])

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


def time_window(days: int = 4):
    time_now = dt.datetime.now()
    time_delta = dt.timedelta(days)

    end_time = time_now.strftime(format="%Y-%m-%dT%H:%M:%SZ")
    start_time = dt.datetime.combine(
        time_now-time_delta,
        dt.datetime.min.time()
        ).strftime(
            format="%Y-%m-%dT%H:%M:%SZ"
            )
    
    return (start_time, end_time)


def float_none(v: float) -> float:
    """Convert into float or None."""
    if v is None:
        return None
    else:
        return float(v)


def test_valid(n: int) -> int:
    """ Return n of -999 if None. """
    if n is None:
        return -999
    else:
        return n


def list_of_days(start_date: str, end_date: str):
    """ List of days between two dates. """
    dates = []
    d = start_date
    while d < end_date:
        dates.append(d)
        d += dt.timedelta(days=1)
        return dates


def day_of_month(year: int, month: int):
    """ List of days in a month. """
    di = dt.date(year, month, 1)
    if month == 12:
        de = dt.date(year + 1, 1, 1)
    else:
        de = dt.date(year, month + 1, 1)
    return list_of_days(di, de)


def date_last_weekday(year: int, month: int, weekday: int):
    """ Date of the last weekday in a month. """
    dm = day_of_month(year, month)
    wd = [e.isoweekday() for e in dm]
    for i, e in enumerate(wd[::-1]):
        if e == weekday:
            return dm[::-1][i]
    return None


def pas_du_range(val_end, offset, nbr_ysticks):
    """ define step for range. """
    space_between_ticks = int(
        np.round((val_end+offset)/nbr_ysticks,
                 -(len(str(int(np.round((val_end+offset)/nbr_ysticks))))-1))
            )
    return space_between_ticks


def get_rolling_data(
        data: pd.DataFrame,
        measure_id: str,
        poll_site_info: pd.DataFrame,
        threshold: int = 0.75
        ) -> pd.DataFrame:

    pd.options.mode.chained_assignment = None

    data.drop('id', axis=1, inplace=True)
    data['data_coverage'] = (~np.isnan(data['value'])).astype(int)

    moymax_jour = data.resample('d').mean().rename(columns={'value': 'mean'})
    moymax_jour['max'] = data['value'].resample('d').max()
    moymax_jour.loc[
        moymax_jour['data_coverage'] < threshold, ['mean', 'max']
        ] = np.NaN

    site_info = poll_site_info[
        poll_site_info['id'] == measure_id
        ].iloc[:, 1:]

    add_poll_info(
        moymax_jour,
        site_info,
        site_info.columns.to_list()
        )
    return (moymax_jour)


def add_poll_info(
        data: pd.DataFrame,
        site_info: pd.DataFrame,
        columns: list,
        ) -> pd.DataFrame:
    for head in columns:
        data[head] = site_info[head].iloc[0]


def mask_aorp(data: pd.DataFrame) -> pd.DataFrame:
    data['value'] = data.apply(
        lambda row:
        np.nan
        if row['state'] not in ['A', 'O', 'R', 'P']
        else row['value'],
        axis=1
    )
    return (data[['id', 'value']])
