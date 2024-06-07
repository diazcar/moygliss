import os
import warnings
from matplotlib import dates, pyplot as plt, ticker
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import requests
import datetime as dt
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "../")

from src.dictionaries import (
    DATA_KEYS,
    FAMILY_LIST,
    INFOPOLS,
    JSON_PATH_LISTS,
    PHYSICALS,
    POLL_AGG_LIST,
    URL_DICT,
    HEADER_RENAME_LISTS,
)
TIME_NOW = dt.datetime.now()

def list_of_strings(arg):
    return arg.split(',')


def time_window(date: str = None):
    days = 5
    time_delta = dt.timedelta(days)

    if date:
        time_now = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    else:
        time_now = dt.datetime.now()

    end_time = dt.datetime.combine(
        time_now,
        dt.datetime.max.time()
        ).strftime(format="%Y-%m-%dT%H:%M:%SZ")

    start_time = dt.datetime.combine(
        time_now-time_delta,
        dt.datetime.min.time()
        ).strftime(format="%Y-%m-%dT%H:%M:%SZ")

    return (start_time, end_time)


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
 
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        request_data = requests.get(
            url, verify=False
            ).json()[DATA_KEYS[folder]]

        data = pd.io.json.json_normalize(
            data=request_data,
            record_path=JSON_PATH_LISTS[folder]['record_path'],
            meta=JSON_PATH_LISTS[folder]['meta'],
        )[list(HEADER_RENAME_LISTS[folder].keys())]
    return (data.rename(columns=HEADER_RENAME_LISTS[folder]))


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


def get_moymax_data(data, measure_id, poll_site_info, threshold=0.75):

    pd.options.mode.chained_assignment = None

    data.drop(['id'], axis=1, inplace=True)
    data['data_coverage'] = (~np.isnan(data['value'])).astype(int)

    moymax_jour = (
        data.resample('d')
        .mean()
        .rename(columns={'value': 'mean'})
        )
    moymax_jour['max'] = data['value'].resample('d').max()
    moymax_jour.loc[
        moymax_jour['data_coverage'] < threshold, ['mean', 'max']
        ] = np.NaN

    site_info = poll_site_info[
        poll_site_info['id'] == measure_id
        ]

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
        new_col: dict = None,
        ) -> pd.DataFrame:
    for head in columns:
        data.insert(
            0,
            head, site_info[head].iloc[0]
            )
    if new_col:
        for head in new_col:
            data.insert(
                0,
                head, new_col[head]
                )
    return (data)


def mask_aorp(data):
    data['value'] = data.apply(
        lambda row:
            np.nan
            if row['state'] not in ['A', 'O', 'R', 'P']
            else row['value'],
            axis=1
    )
    return (data[['id', 'value', 'unit']])


def build_mpl_graph(
                poll_iso: str,
                measure_id: str,
                site_name: str,
                dept_code: str,
                units: str,
                hourly_data: pd.DataFrame,
                day_data: pd.DataFrame,
                y_ticks: list,
                max_y_lim: int,
                background_color: str = 'white',
                timeseries_color: str = 'blue',
                weight_data=None,
                ) -> plt:

    measure_id_data = hourly_data[hourly_data['id'] == measure_id]
    moygliss = measure_id_data['moygliss24']
    max_gliss = moygliss.dropna()[-24:].max()
    data_hour = measure_id_data['value']
    time = data_hour.reset_index()['date']

    x_fig_size = 3
    y_fig_size = 3
    if poll_iso in FAMILY_LIST:
        x_fig_size = 12

    fig = plt.figure(figsize=(x_fig_size, y_fig_size))

    ax = fig.add_axes(
            [0.18, 0.1, 0.8, 0.8],
            facecolor=background_color
            )
    ax.plot(data_hour, timeseries_color, alpha=.25)

    last_date_to_plot = time.searchsorted(data_hour.last_valid_index())
    ax.plot(moygliss.iloc[:last_date_to_plot], timeseries_color, lw=2)

    for lim in ['lim1', 'lim2', 'lim3']:
        if lim in list(INFOPOLS[poll_iso].keys()):
            ax.plot(
                    time,
                    [INFOPOLS[poll_iso][lim],] * (len(moygliss)),
                    'red',
                    ls='--'
            )
            if (
                INFOPOLS[poll_iso]['lim1'] is not None
                and
                max_gliss > INFOPOLS[poll_iso]['lim1']
            ):
                ax.update({'facecolor': (1, 0, 0, 0.07)})

            if (
                INFOPOLS[poll_iso]['lim2'] is not None
                and
                max_gliss > INFOPOLS[poll_iso]['lim2']
            ):
                ax.get_lines()[0].set_color('red')

            if (
                INFOPOLS[poll_iso]['lim3'] is not None
                and
                max_gliss > INFOPOLS[poll_iso]['lim3']
            ):
                ax.get_lines()[0].set_color('purple')

    ax.xaxis.set_major_locator(dates.HourLocator(byhour=0))
    ax.xaxis.set_minor_locator(dates.HourLocator(byhour=12))
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d %b'))
    ax.set_yticks(y_ticks)
    ax.set_ylim(0, max_y_lim)
    ax.set_xlim(
            hourly_data.index[0],
            dt.datetime.combine(
                    hourly_data.index[-1], dt.datetime.max.time()
                    )
            )
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    ax.set_title(f"{dept_code} {site_name}")
    ax.set_ylabel(
        f"{INFOPOLS[poll_iso]['nom']} [{units[0]}]",
        labelpad=2,
        )
    ax.grid(True, linestyle='--')

    add_annotations(
            measure_id=measure_id,
            day_data=day_data,
            time_vector=time,
            ax=ax,
            max_y_lim=max_y_lim,
            mode=INFOPOLS[poll_iso]["ann"],
            )

    if poll_iso in FAMILY_LIST:
        add_weight_annotations(
            weight_data=weight_data,
            time_vector=time,
            measure_id=measure_id,
            ax=ax,
            max_y_lim=max_y_lim,
            mode=INFOPOLS[poll_iso]["ann"],
        )
    return (fig)


def add_annotations(
                measure_id: str,
                day_data: str,
                time_vector: pd.DatetimeIndex,
                max_y_lim: int,
                ax: plt.axes,
                mode: str,
                ):

    value_day_list = day_data[
        day_data['id'] == measure_id
        ][mode].to_list()[1:-1]

    x = time_vector[0] + dt.timedelta(hours=25)
    y = max_y_lim - max_y_lim*0.06

    for max in value_day_list:

        if ~np.isnan(max):
            if max > 10:
                string = f"{max: .0f}"
            else:
                string = f"{max: .2f}"
            ax.annotate(
                    string,
                    xy=(x, y),
                    xycoords='data',
                    fontsize=8,
                    color='grey',
            )
            x = x + dt.timedelta(hours=24)
        else:
            x = x + dt.timedelta(hours=24)


def add_weight_annotations(
        weight_data: pd.DataFrame,
        time_vector: pd.DatetimeIndex,
        measure_id: str,
        ax: plt.axes,
        max_y_lim: int,
        mode: str,
        ):
    id_data = weight_data[weight_data['id'] == measure_id]
    dtindex = id_data.resample('d')['value'].idxmax()
    drop_col_list = ['id', 'id_site', 'phy_name', 'id_phy', 'value', 'unit']

    x_delta = dt.timedelta(hours=24)
    x = time_vector[0] + dt.timedelta(hours=25)

    for date_index in dtindex[:-1]:
        if pd.isnull(date_index):
            x = x + x_delta
        else:
            filtered_max_w8 = id_data.loc[date_index].drop(drop_col_list)

            highest_five = filtered_max_w8.reset_index()
            highest_five.index.name = "index"
            highest_five.rename(
                columns={
                    highest_five.columns[0]: "iso",
                    highest_five.columns[1]: "weight"
                },
                inplace=True
            )
            highest_five = highest_five.sort_values(
                by=['weight'],
                ascending=False
                ).reset_index(drop=True).head(5)

            y_delta = max_y_lim*.09
            y = max_y_lim - y_delta

            for i in range(5):
                iso = highest_five.iloc[i]['iso']
                weight = highest_five.iloc[i]['weight']

                y = y - y_delta

                ax.annotate(
                    f"{iso} : {weight*100: .0f}%",
                    xy=(x, y),
                    xycoords='data',
                    fontsize=8,
                    color='#aaaaaa',
                    weight='bold',
                )

            x = x + x_delta

    return ()


def compute_aggregations(
        data: pd.DataFrame,
        reseaux: str,
):
    iso_family = list(POLL_AGG_LIST[reseaux].keys())
    weight_data = pd.DataFrame()

    for family in iso_family:

        iso_list_family = POLL_AGG_LIST[reseaux][family]['iso_list']
        sites = POLL_AGG_LIST[reseaux][family]['sites']

        for site in sites:
            filtered_data = data[
                (data['id_site'] == site)
                &
                (data['id_phy'].isin(iso_list_family))
                ]

            if family == 'ML':
                filtered_data['value'] = filtered_data['value']/1000
                filtered_data['unit'] = 'μg/m3'
            weights = (
                filtered_data['value']
                .groupby(filtered_data.index)
                .sum()
                .replace(0, np.nan)
                .to_frame()
            )

            for head in list(filtered_data['id_phy'].unique()):
                head_data = filtered_data[filtered_data['id_phy'] == head]
                head_data = head_data.groupby(head_data.index).sum()
                w8 = head_data['value']/weights['value']
                weights[PHYSICALS[head]['label']] = w8.values

            add_poll_info(
                data=weights,
                site_info=filtered_data,
                columns=['unit', 'id_site'],
                new_col={
                    'id_phy': family,
                    'id': f"{family}{site}",
                    'phy_name': INFOPOLS[family]['nom']
                    }
                )
            weight_data = pd.concat([weight_data, weights], sort=False)

    data = pd.concat([data, weight_data], join='inner')
    data = data[~data.id_phy.isin(iso_list_family)]

    return (data, weight_data)


def wrap_agg_to_data(
        data: pd.DataFrame,
        agg_data: pd.DataFrame,
        unit: str,
        site_name: str,
        physical_id: str,
        ):
    n_data = len(agg_data.values)
    for site in site_name:
        agg_df = pd.DataFrame(
                data={
                    'id': [f"{physical_id}{site}"]*n_data,
                    'value': agg_data,
                    'unit': unit[:n_data],
                    'id_site': [site]*n_data,
                    'id_phy': [physical_id]*n_data,
                    'phy_name': INFOPOLS[physical_id]['nom']
                },
            )

        data = pd.concat([data, agg_df])

    return (data)


def pas_du_range(val_end, offset, nbr_ysticks):
    """ define step for range. """
    step_by_tick = (val_end+offset)/nbr_ysticks
    nb_digits = len(str(int(np.round(step_by_tick))))-1
    if nb_digits == 0:
        nb_digits = 1
    roundup = np.round(step_by_tick, -nb_digits)
    pas = int(roundup)
    if pas == 0:
        pas = step_by_tick
    return (pas)


def get_figure_title(
    group_data: pd.DataFrame,
    group_sites: pd.DataFrame,
    id: str,
):
    """_summary_

    Parameters
    ----------
    group_data : pd.DataFrame
        _description_
    group_sites : pd.DataFrame
        _description_
    id : str
        _description_
    """
    if "MOBILE" in id:
        name = group_data[
            group_data['id'] == id
            ]['id_site'].values[0]
        site_name = group_sites[
            group_sites['id'] == name
            ]['labelSite'].values[0]
        dept_code = group_sites[
            group_sites['labelSite'] == site_name
            ]['dept_code'].values[0]

    else:
        site_name = group_data[
            group_data['id'] == id
            ]['id_site'].values[0]
        dept_code = group_sites[
            group_sites['id'] == site_name
            ]['dept_code'].values[0]

    return (site_name, dept_code)
