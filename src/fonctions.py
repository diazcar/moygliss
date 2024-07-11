import math
import os
import warnings
from matplotlib import dates, pyplot as plt, ticker
import requests
import datetime as dt
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "../")


from src.dictionaries import (
    COV_FAMILIES,
    DATA_KEYS,
    FAMILY_LIST,
    INFOPOLS,
    JSON_PATH_LISTS,
    PCOP_DATA,
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

        data = pd.json_normalize(
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
        ] = np.nan

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
                group: str,
                poll_iso: str,
                measure_id: str,
                site_name: str,
                dept_code: str,
                units: str,
                hourly_data: pd.DataFrame,
                day_data: pd.DataFrame,
                y_ticks: list,
                max_y_lim: int,
                agg_data_dir: str,
                background_color: str = 'white',
                timeseries_color: str = 'blue',
                weight_data=None,
                ) -> plt:

    measure_id_data = hourly_data[hourly_data['id'] == measure_id]
    moygliss = measure_id_data['moygliss24'][24:]
    max_jour_j = measure_id_data['value'][-24:].max()
    data_hour = measure_id_data['value'][24:]
    time = data_hour.reset_index()['date']

    x_fig_size = 4
    y_fig_size = 3
    if poll_iso in FAMILY_LIST or poll_iso in COV_FAMILIES:
        x_fig_size = 13

    fig = plt.figure(figsize=(x_fig_size, y_fig_size))

    ax = fig.add_axes(
            [0.13, 0.12, 0.8, 0.8],
            facecolor=background_color
            )

    ax.plot(data_hour, timeseries_color, alpha=.35)
    last_valid_time = data_hour.last_valid_index()
    ax.plot(moygliss[:last_valid_time], timeseries_color, lw=2)

    window_gliss_data = moygliss[:last_valid_time]
    max_gliss = window_gliss_data[-24:].dropna().max()

    add_color_use_cases(
        max_gliss=max_gliss,
        max_jour_j=max_jour_j,
        poll_iso=poll_iso,
        ax=ax,
        y_ax=time,
        x_ax_len=len(moygliss),
    )

    ax.xaxis.set_major_locator(dates.HourLocator(byhour=0))
    ax.xaxis.set_minor_locator(dates.HourLocator(byhour=12))
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%d %b'))
    ax.set_yticks(y_ticks)
    ax.set_ylim(0, max_y_lim)
    ax.set_xlim(
            data_hour.index[0],
            dt.datetime.combine(
                    data_hour.index[-1], dt.datetime.max.time()
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
            group=group,
            measure_id=measure_id,
            poll_iso=poll_iso,
            day_data=day_data,
            time_vector=time,
            ax=ax,
            max_y_lim=max_y_lim,
            mode=INFOPOLS[poll_iso]["ann"],
            agg_data_dir=agg_data_dir
            )
    if poll_iso in COV_FAMILIES:
        update_COV_plot(
            poll_iso=poll_iso,
            weight_data=weight_data,
            measure_id=measure_id,
            start_end_dates=[
                data_hour.index[0],
                data_hour.index[-1]
                ],
            time=time,
            ax=ax,
            max_y_lim=max_y_lim,
            y_ticks=y_ticks,
        )

    if poll_iso in FAMILY_LIST:
        add_weight_annotations(
            weight_data=weight_data,
            time_vector=time,
            measure_id=measure_id,
            ax=ax,
            max_y_lim=max_y_lim,
            poll_iso=poll_iso,
        )

    return (fig)


def update_COV_plot(
        poll_iso: str,
        weight_data: pd.DataFrame,
        measure_id: str,
        start_end_dates: list,
        time: np.array,
        ax: plt.axes,
        max_y_lim: float,
        y_ticks: np.array,
):

    if poll_iso == 'COVpcop':
        pcop_annotations(
            weight_data=weight_data,
            time_vector=time,
            measure_id=measure_id,
            ax=ax,
            max_y_lim=max_y_lim,
            poll_iso=poll_iso,
        )
        ax.get_lines()[1].remove()

        reactive_data = weight_data[
            weight_data['id'] == measure_id
            ]['reactive_value']

        ax.plot(
            time,
            reactive_data[time[0]:],
            color='darkorange',
            )

        ax.set_ylabel("Conc. Potentiellement Réactive")
        ax.yaxis.label.set_color('darkorange')
        ax.get_lines()[0].remove()
        ax.get_lines()[1].remove()

    else:
        add_weight_annotations(
            weight_data=weight_data,
            time_vector=time,
            measure_id=measure_id,
            ax=ax,
            max_y_lim=max_y_lim,
            poll_iso=poll_iso,
        )

        ax2 = ax.twinx()

        reactive_data = weight_data[
            weight_data['id'] == measure_id
            ]['reactive_value']

        ax2.plot(
            time,
            reactive_data[time[0]:],
            color='darkorange',
            )
        ax2.set_ylim(0, max_y_lim)
        ax2.set_xlim(
            start_end_dates[0],
            dt.datetime.combine(
                    start_end_dates[1],
                    dt.datetime.max.time()
                    )
        )
        ax2.set_yticks(y_ticks)
        ax2.set_ylabel("Conc. Potentiellement Réactive")
        ax2.yaxis.label.set_color('darkorange')
        ax.yaxis.label.set_color('blue')
        ax.get_lines()[0].set_color('blue')
        ax.get_lines()[1].remove()


def add_annotations(
        group: str,
        measure_id: str,
        poll_iso: str,
        day_data: str,
        time_vector: pd.DatetimeIndex,
        max_y_lim: int,
        ax: plt.axes,
        mode: str,
        agg_data_dir: str,
        ):

    if poll_iso in FAMILY_LIST or poll_iso in COV_FAMILIES:

        value_day_list = get_family_day_max(
            poll_iso,
            group, measure_id,
            agg_data_dir
            )

        x = time_vector[0]

    else:

        df_values = day_data[
            day_data['id'] == measure_id
            ][mode]

        value_day_list = df_values.to_list()[1:]

        x = time_vector[0]

    y = max_y_lim - max_y_lim*0.06

    add_ann_mode(
        poll_iso=poll_iso,
        mode=mode,
        ax=ax
    )

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


def add_ann_mode(
        poll_iso: str,
        mode: str,
        ax: plt.axes,
):

    x = -1.3
    y = 189

    if poll_iso in FAMILY_LIST or poll_iso in COV_FAMILIES:
        x = 85

    ax.annotate(
        f"{mode}->",
        xy=(x, y),
        xycoords='figure points',
        fontsize=7,
        color='grey',
        )


def add_weight_annotations(
        weight_data: pd.DataFrame,
        time_vector: pd.DatetimeIndex,
        measure_id: str,
        ax: plt.axes,
        max_y_lim: int,
        poll_iso: str,
        ):

    id_data = weight_data[weight_data['id'] == measure_id][time_vector[0]:]
    dtindex = id_data.resample('d')['value'].idxmax()
    if poll_iso in COV_FAMILIES:
        drop_col_list = [
            'id', 'id_site', 'phy_name',
            'id_phy', 'value', 'reactive_value',
            'unit',
            ]
    else:
        drop_col_list = [
            'id', 'id_site', 'phy_name',
            'id_phy', 'value', 'unit'
            ]

    x_delta = dt.timedelta(hours=24)
    x = time_vector[0]
    x_delta_porcentage = dt.timedelta(hours=5)

    for date_index in dtindex:
        if pd.isnull(date_index):
            x = x + x_delta
        else:
            filtered_max_w8 = id_data.loc[date_index].drop(drop_col_list)

            highest_five = filtered_max_w8.reset_index()
            highest_five.index.name = "index"
            highest_five.rename(
                columns={
                    highest_five.columns[0]: "iso_name",
                    highest_five.columns[1]: "weight"
                },
                inplace=True
            )

            if poll_iso in COV_FAMILIES:
                highest_five = highest_five[
                    ~highest_five['iso_name'].str.contains("pcop_")
                    ].sort_values(
                    by=['weight'],
                    ascending=False
                    ).reset_index(drop=True).head(5)

                highest_five['pcop'] = highest_five['iso_name'].apply(
                    lambda iso_name:
                        PCOP_DATA[
                            PCOP_DATA["label"] == iso_name
                            ]['PCOP'].values,
                    )
            else:
                highest_five = highest_five.sort_values(
                    by=['weight'],
                    ascending=False
                    ).reset_index(drop=True).head(5)

            y_delta = max_y_lim*.09
            y = max_y_lim - y_delta

            if len(highest_five.index) > 2:
                n = 5
            else:
                n = 2
            for i in range(n):
                iso = highest_five.iloc[i]['iso_name']
                weight = highest_five.iloc[i]['weight']

                if poll_iso in ['BTEX', 'COVle', 'COVlo']:
                    pcop_index = highest_five.iloc[i]['pcop']
                    color = get_pcop_index_color(pcop_index)

                else:
                    color = "silver"

                y = y - y_delta

                ax.annotate(
                    f"{weight*100: .0f}%-",
                    xy=(x, y),
                    xycoords='data',
                    fontsize=8,
                    color="silver",
                    weight='bold',
                )

                ax.annotate(
                    f"{iso}",
                    xy=(x+x_delta_porcentage, y),
                    xycoords='data',
                    fontsize=8,
                    color=color,
                    weight='bold',
                )
            x = x + x_delta
    return ()


def pcop_annotations(
        weight_data: pd.DataFrame,
        time_vector: pd.DatetimeIndex,
        measure_id: str,
        ax: plt.axes,
        max_y_lim: int,
        poll_iso: str,
        ):

    id_data = weight_data[weight_data['id'] == measure_id][time_vector[0]:]
    dtindex = id_data.resample('d')['value'].idxmax()
    if poll_iso in COV_FAMILIES:
        drop_col_list = [
            'id', 'id_site', 'phy_name',
            'id_phy', 'value', 'reactive_value',
            'unit',
            ]
    else:
        drop_col_list = [
            'id', 'id_site', 'phy_name',
            'id_phy', 'value', 'unit'
            ]

    x_delta = dt.timedelta(hours=24)
    x = time_vector[0]
    x_delta_porcentage = dt.timedelta(hours=5)

    for date_index in dtindex:
        if pd.isnull(date_index):
            x = x + x_delta
        else:
            filtered_max_w8 = id_data.loc[date_index].drop(drop_col_list)

            highest_five = filtered_max_w8.reset_index()
            highest_five.index.name = "index"
            highest_five.rename(
                columns={
                    highest_five.columns[0]: "iso_name",
                    highest_five.columns[1]: "weight"
                },
                inplace=True
            )

            highest_five = highest_five[
                highest_five['iso_name'].str.contains("pcop_")
                ].sort_values(
                by=['weight'],
                ascending=False
                ).reset_index(drop=True).head(5)

            highest_five['iso_name'] = (
                highest_five['iso_name'].str.replace('pcop_', '')
                )

            highest_five['pcop'] = highest_five['iso_name'].apply(
                lambda iso_name:
                    PCOP_DATA[
                        PCOP_DATA["label"] == iso_name
                        ]['PCOP'].values,
                    )

            y_delta = max_y_lim*.09
            y = max_y_lim - y_delta
            if len(highest_five.index) > 2:
                n = 5
            else:
                n = 2
            for i in range(n):
                iso = highest_five.iloc[i]['iso_name']
                weight = highest_five.iloc[i]['weight']

                pcop_index = highest_five.iloc[i]['pcop']
                color = get_pcop_index_color(pcop_index)

                y = y - y_delta

                ax.annotate(
                    f"{weight*100: .0f}%-",
                    xy=(x, y),
                    xycoords='data',
                    fontsize=8,
                    color="silver",
                    weight='bold',
                )

                ax.annotate(
                    f"{iso}",
                    xy=(x+x_delta_porcentage, y),
                    xycoords='data',
                    fontsize=8,
                    color=color,
                    weight='bold',
                )
            x = x + x_delta
    return ()


def get_pcop_index_color(value):
    if value <= 25:
        color = "green"
    if 25 <= value <= 75:
        color = "orange"
    if 75 <= value <= 125:
        color = "red"
    if 125 <= value <= 175:
        color = "purple"

    return (color)


def compute_aggregations(
        data: pd.DataFrame,
        reseaux: str,
        physicals: dict,
):
    iso_family = list(POLL_AGG_LIST[reseaux].keys())
    cov_family = list(POLL_AGG_LIST['V_COV'].keys())
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
            if family in cov_family:
                add_pcop_weight(
                    data=filtered_data
                    )

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
                agg_data = head_data.groupby(head_data.index).sum()
                w8 = agg_data['value']/weights['value']
                weights[physicals[head]['label']] = w8.values

            if family in cov_family:
                weights["reactive_value"] = (
                    filtered_data['value_w8_pcop']
                    .groupby(filtered_data.index)
                    .sum()
                    .replace(0, np.nan)
                    .to_frame()
                )
                for head in list(filtered_data['id_phy'].unique()):
                    head_data = filtered_data[filtered_data['id_phy'] == head]
                    agg_data = head_data.groupby(head_data.index).sum()
                    w8 = agg_data['value_w8_pcop']/weights['reactive_value']
                    weights[f"pcop_{physicals[head]['label']}"] = w8.values

            add_poll_info(
                data=weights,
                site_info=filtered_data,
                columns=['unit', 'id_site'],
                new_col={
                    'id_phy': family,
                    'id': f"{family}{site}",
                    'phy_name': INFOPOLS[family]['nom'],
                    }
                )
            weight_data = pd.concat([weight_data, weights], sort=False)

    data = pd.concat([data, weight_data], join='inner')
    data = data[~data.id_phy.isin(iso_list_family)]

    return (data, weight_data)


def add_pcop_weight(
        data: pd.DataFrame,
):
    data['value_w8_pcop'] = data.apply(
        lambda row: (
            row['value']*(
                PCOP_DATA[PCOP_DATA['id'] == row['id_phy']]['PCOP'].values
                )/100
            )[0],
        axis=1,
        )
    data['pcop'] = data.apply(
        lambda row: (
            PCOP_DATA[PCOP_DATA['id'] == row['id_phy']]['PCOP'].values/100)[0],
        axis=1
        )
    return (data)


def wrap_agg_to_data(
        data: pd.DataFrame,
        agg_data: pd.DataFrame,
        unit: str,
        site_name: str,
        physical_id: str,
        ):
    """_summary_

    Parameters
    ----------
    data : pd.DataFrame
        _description_
    agg_data : pd.DataFrame
        _description_
    unit : str
        _description_
    site_name : str
        _description_
    physical_id : str
        _description_

    Returns
    -------
    _type_
        _description_
    """
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


def pas_du_range(val_end, nbr_ysticks, offset=0):
    """_summary_

    Parameters
    ----------
    val_end : _type_
        _description_
    offset : _type_
        _description_
    nbr_ysticks : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    if val_end < 5:
        pas = val_end/nbr_ysticks
    else:
        step_by_tick = math.ceil((val_end+offset)/nbr_ysticks)
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

    Returns
    -------
    _type_
        _description_
    """
    if "MOBILE" in id.upper():
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


def get_family_day_max(
        poll_iso: str,
        group: str,
        measure_id: str,
        agg_data_dir: str,
) -> pd.DataFrame:
    """_summary_

    Parameters
    ----------
    measure_id : str
        _description_
    poll_iso : str
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """

    agg_data = pd.read_csv(
        f"{agg_data_dir}/data/{group}_agg_weights.csv",
        parse_dates=['date'],
    )

    data_measure_id = agg_data[agg_data['id'] == measure_id]
    # Corriger la transition des mois
    if poll_iso == 'COVpcop':
        day_maxes = (
            data_measure_id['reactive_value']
            .groupby(data_measure_id.date.dt.date)
            .max()
            )
    else:
        day_maxes = (
            data_measure_id['value']
            .groupby(data_measure_id.date.dt.date)
            .max()
            )

    return (day_maxes.values[1:])


def get_iso_max_val(
        poll_iso: str,
        measure_id: str,
        group_data: pd.DataFrame,
        ) -> int:
    """_summary_

    Parameters
    ----------
    measure_id : str
        _description_
    group_data : pd.DataFrame
        _description_

    Returns
    -------
    int
        _description_
    """

    if len(measure_id) > 0:
        values = group_data[
            group_data['id'].isin(measure_id)
            ]
        graph_time_x1 = str(
            values.reset_index()['date'].unique()[24:][0]
            )
        values = values[graph_time_x1:]['value']
    else:
        values = [np.nan,]

    if pd.isnull(values).all():
        max_val = 10
    else:
        if INFOPOLS[poll_iso]['max'] is not None:
            max_val = INFOPOLS[poll_iso]['max']
        else:
            max_val = math.ceil(
                values.dropna().values.max())
        if max_val == 0:
            max_val = 10

    return (max_val)


def add_color_use_cases(
        max_gliss: float,
        max_jour_j: float,
        poll_iso: str,
        ax: plt.axes,
        y_ax,
        x_ax_len: int,
):
    if poll_iso in ["08", "03"]:
        for lim in ['lim1', 'lim2', 'lim3']:
            if lim in list(INFOPOLS[poll_iso].keys()):
                ax.plot(
                        y_ax,
                        [INFOPOLS[poll_iso][lim],] * (x_ax_len),
                        'red',
                        ls='--'
                )

                if (
                    INFOPOLS[poll_iso]['lim1'] is not None
                    and
                    max_jour_j > INFOPOLS[poll_iso]['lim1']
                ):
                    ax.update({'facecolor': (1, 0, 0, 0.05)})

                if (
                    INFOPOLS[poll_iso]['lim1'] is not None
                    and
                   (
                       INFOPOLS[poll_iso]['lim1']*0.95
                       ) <= max_jour_j < INFOPOLS[poll_iso]['lim1']
                ):
                    ax.update({'facecolor': (1, .6, 0, 0.05)})

                if (
                    INFOPOLS[poll_iso]['lim2'] is not None
                    and
                    max_jour_j >= INFOPOLS[poll_iso]['lim2']
                ):
                    ax.get_lines()[0].set_color('red')
                    ax.update({'facecolor': (1, 0, 0, 0.05)})

    else:
        for lim in ['lim1', 'lim2', 'lim3']:
            if lim in list(INFOPOLS[poll_iso].keys()):
                ax.plot(
                        y_ax,
                        [INFOPOLS[poll_iso][lim],] * (x_ax_len),
                        'red',
                        ls='--'
                )
                if (
                    INFOPOLS[poll_iso]['lim1'] is not None
                    and
                    max_gliss >= INFOPOLS[poll_iso]['lim1']
                ):
                    ax.get_lines()[1].set_color('red')
                    ax.update({'facecolor': (1, 0, 0, 0.05)})

                if (
                    INFOPOLS[poll_iso]['lim1'] is not None
                    and
                    max_jour_j >= INFOPOLS[poll_iso]['lim1']
                ):
                    ax.get_lines()[0].set_color('red')

                if (
                    INFOPOLS[poll_iso]['lim2'] is not None
                    and
                    max_jour_j >= INFOPOLS[poll_iso]['lim2']
                ):
                    ax.get_lines()[0].set_color('red')
                    ax.update({'facecolor': (1, 0, 0, 0.05)})

                if (
                    INFOPOLS[poll_iso]['lim3'] is not None
                    and
                    max_jour_j >= INFOPOLS[poll_iso]['lim3']
                ):
                    ax.get_lines()[0].set_color('green')
