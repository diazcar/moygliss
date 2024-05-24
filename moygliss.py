import sys
import matplotlib
import pandas as pd
import math
import argparse
from tqdm import tqdm

from src.dictionaries import (
    INFOPOLS,
    MATPLOT_PARAMS,
    POLL_BY_SITE_LIST,
    GROUP_LIST
    )

from src.fonctions import (
    add_poll_info,
    build_mpl_graph,
    get_moymax_data,
    mask_aorp,
    request_xr,
    test_path,
    time_window,
    list_of_strings
    )

pd.options.mode.chained_assignment = None
matplotlib.rcParams.update(MATPLOT_PARAMS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
Thise Script compute the hourly rolling mean for the last 5.
Then Generate a list of figures for every Group-site-pollutant.
        """,
        formatter_class=argparse.RawTextHelpFormatter,)

    parser.add_argument(
        "-g", "--group",
        type=list_of_strings,
        help="Stations group",
        default=GROUP_LIST,
        metavar="\b"
        )

    parser.add_argument(
        "-iso", "--pollutant_iso",
        type=list_of_strings,
        help="ISO identifiant for a pollutant",
        default=list(INFOPOLS.keys()),
        metavar="\b"
        )

    args = parser.parse_args()

    test_path('./data', 'mkdir')
    test_path('./output', 'mkdir')

    list_of_files = []

    for group in args.group:
        group_sites = request_xr(
            folder='sites',
            groups=group,
        )

        group_poll_site_info = request_xr(
            folder="measures",
            groups=group,
            datatype='sta'
        )

        group_raw_data = request_xr(
            fromtime=time_window()[0],
            totime=time_window()[1],
            folder="data",
            measures=",".join(group_poll_site_info['id'].to_list()),
            datatype="hourly",
        )

        group_raw_data['date'] = pd.to_datetime(
            group_raw_data['date'],
            format="%Y-%m-%dT%H:%M:%SZ"
            )
        group_raw_data.set_index('date', inplace=True)
        group_raw_data = mask_aorp(group_raw_data)

        group_data = pd.DataFrame()
        for id in group_raw_data.id.unique():
            data_chunk = add_poll_info(
                data=group_raw_data[group_raw_data['id'] == id],
                site_info=group_poll_site_info[
                    group_poll_site_info['id'] == id
                    ],
                columns=['id_site', 'id_phy'],
            )
            group_data = pd.concat([group_data, data_chunk])

        if group in ['V_MARS', 'V_MART']:
            compute_metaux_lourds(group_data)

        group_moymax_data = pd.DataFrame()
        for id in group_poll_site_info['id'].to_list():
            measure_id_gliss = get_moymax_data(
                data=group_data[group_data['id'] == id][['id', 'value']],
                measure_id=id,
                poll_site_info=group_poll_site_info,
                threshold=0.75
            )
            group_moymax_data = pd.concat(
                [group_moymax_data, measure_id_gliss]
                )

        group_poll_site_info.to_csv(f"./data/{group}_pollsites_info.csv")
        group_data.to_csv(f"./data/{group}_data.csv")
        group_moymax_data.to_csv(f"./data/{group}_moymax.csv")
        group_sites.to_csv(f"./data/{group}_sites.csv")

        for poll_iso in args.pollutant_iso:
            if poll_iso not in POLL_BY_SITE_LIST:
                for_poll_list = group_poll_site_info[
                    group_poll_site_info['id_phy'] == poll_iso
                    ]
                measure_id = for_poll_list['id'].to_list()

                for id in tqdm(
                    measure_id, desc="".join(
                        [
                            f"Processing {poll_iso} ",
                            "for sites ",
                            f"in group {group}"
                        ]
                    )
                ):

                    site_name = group_poll_site_info[
                        group_poll_site_info['id'] == id
                        ]['id_site'].values[0]

                    dept_code = group_sites[
                        group_sites['labelSite'] == site_name
                        ]['dept_code'].values[0]

                    figure_title = f"{dept_code} {site_name}"

                    group_data['moygliss24'] = (
                        group_data['value']
                        .rolling(window=24, min_periods=1).mean()
                        )

                    if INFOPOLS[poll_iso]['max'] is not None:
                        max_val = INFOPOLS[poll_iso]['max']
                    else:
                        max_val = int(
                            group_data[
                                group_data['id'].isin(measure_id)
                                ]['value'].dropna().values.max()
                        )
                    if max_val == 0:
                        max_val = 10
                    max_y_lim = max_val + math.ceil(max_val*0.1)
                    y_ticks = range(0, max_val, math.ceil(max_val*0.1))

                    plot = build_mpl_graph(
                            poll_iso=poll_iso,
                            measure_id=id,
                            site_name=site_name,
                            dept_code=dept_code,
                            hourly_data=group_data.iloc[24:],
                            day_data=group_moymax_data,
                            max_y_lim=max_y_lim,
                            y_ticks=y_ticks,
                    )
                    file_name = ".".join(
                        [
                            "moygliss24h",
                            group,
                            f"{dept_code}_{site_name}",
                            poll_iso,
                            "png"
                            ]
                    )
                    file_out = f"./output/{file_name}"
                    list_of_files.append(file_name)
                    plot.savefig(file_out)
                    matplotlib.pyplot.close()

    with open("./output/list", 'w') as f:
        for file in list_of_files:
            f.write(f"{file}\n")

sys.exit(0)
