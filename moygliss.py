import sys
import matplotlib
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import math
import argparse
sys.path.insert(0, "./")

from src.dictionaries import (
    INFOPOLS,
    MATPLOT_PARAMS,
    GROUP_LIST,
    POLL_AGG_LIST
    )

from src.fonctions import (
    add_poll_info,
    build_mpl_graph,
    compute_aggregations,
    get_figure_title,
    get_iso_max_val,
    get_moymax_data,
    mask_aorp,
    pas_du_range,
    request_xr,
    test_path,
    time_window,
    list_of_strings
    )

register_matplotlib_converters()
pd.options.mode.chained_assignment = None
matplotlib.rcParams.update(MATPLOT_PARAMS)

if __name__ == "__main__":

    ###########################################################################
    # ARGUMENTS
    ###########################################################################
    parser = argparse.ArgumentParser(
        description="""
    Thise Script compute the hourly rolling mean for the last 5.
    Then Generate a list of figures for every Group-site-pollutant.
        """,
        formatter_class=argparse.RawTextHelpFormatter,
        )
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
    parser.add_argument(
        '-d', '--date',
        type=str,
        help=' End rolling mean date',
        default=None,
        metavar="\b",
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='path/to/output/figures.png',
        default='.',
        metavar='\b',
    )
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # Create path/folder if not exist
    test_path(f'{args.output}/data', 'mkdir')
    test_path(f'{args.output}/output', 'mkdir')

    # Define list of files to append: for the html site mesmod
    list_of_files = []

    # -------------------------------------------------------------------------

    # LOOP GROUPS
    for group in args.group:
        #######################################################################
        # GET DATA AND PUT IN TABLE FORMAT WITH POLLUTANT AND SITE INFO ->CSV #
        #######################################################################
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
            fromtime=time_window(args.date)[0],
            totime=time_window(args.date)[1],
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

        # ---------------------------------------------------------------------
        # Add pollutant and site info to measurements in group data
        group_data = pd.DataFrame()
        for id in group_raw_data.id.unique():
            data_chunk = add_poll_info(
                data=group_raw_data[group_raw_data['id'] == id],
                site_info=group_poll_site_info[
                    group_poll_site_info['id'] == id
                    ],
                columns=['id_site', 'id_phy', 'phy_name'],
            )
            group_data = pd.concat([group_data, data_chunk])

        # ---------------------------------------------------------------------
        # Add iso familly aggregations and build table wiht iso's weights
        weight_data = None
        if group in list(POLL_AGG_LIST.keys()):
            group_data, weight_data = compute_aggregations(group_data, group)

            # Add family info to iso's info list
            cols = ['id', 'id_site', 'phy_name', 'id_phy', 'unit']
            families = list(POLL_AGG_LIST[group].keys())
            family_info = group_data[group_data['id_phy'].isin(families)][cols]
            family_info.reset_index(drop=True, inplace=True)

            group_poll_site_info = pd.concat(
                [group_poll_site_info, family_info]
                )

            # Save Family members weights
            weight_data.to_csv(f"{args.output}/data/{group}_agg_weights.csv")

        # ---------------------------------------------------------------------
        # Compute daily means and max and build table with poll-site-info
        group_moymax_data = pd.DataFrame()
        for id in group_data['id'].unique():
            measure_id_gliss = get_moymax_data(
                data=group_data[group_data['id'] == id][['id', 'value']],
                measure_id=id,
                poll_site_info=group_poll_site_info,
                threshold=0.75
            )
            group_moymax_data = pd.concat(
                [group_moymax_data, measure_id_gliss]
                )
        # ---------------------------------------------------------
        # Compute rolling mean and create "moygliss24" col. in data
        group_data['moygliss24'] = (
            group_data['value']
            .rolling(window=24, min_periods=12)
            .mean()
            )

        # ---------------------------------------------------------------------
        # Save data files to debug and exlore data used
        group_poll_site_info.to_csv(
            f"{args.output}/data/{group}_pollsites_info.csv"
            )
        group_data.to_csv(f"{args.output}/data/{group}_data.csv")
        group_moymax_data.to_csv(f"{args.output}/data/{group}_moymax.csv")
        group_sites.to_csv(f"{args.output}/data/{group}_sites.csv")

        # ---------------------------------------------------------------------
        # Loop of iso pollutant in dictionary $poll_agg_list
        for poll_iso in args.pollutant_iso:

            for_poll_list = group_data[
                group_data['id_phy'] == poll_iso
                ]

            measure_id = for_poll_list['id'].unique()

            # ---------------------------------------------------------
            # Get overall measurement max to set graph limits

            max_val = get_iso_max_val(
                poll_iso=poll_iso,
                measure_id=measure_id,
                group_data=group_data
                )
            max_y_lim = max_val + max_val*0.15
            step = pas_du_range(max_val, 0, 10)
            y_ticks = np.arange(
                0, max_val, step
                )
            # -------------------------------------------------------------
            # Loop of measurements(by site) of the iso in the group
            if len(measure_id) > 0:
                for id in measure_id:

                    test_values = group_data[group_data['id'] == id]['value']
                    units = group_data[group_data['id'] == id]['unit'].unique()
                    if ~pd.isnull(test_values).all():
                        desc = "".join(
                            [
                                f"Processing {poll_iso} ",
                                "for sites ",
                                f"in group {group} ..."
                            ]
                            )
                        print(desc, end='\r')

                        site_name, dept_code = get_figure_title(
                            group_data,
                            group_sites,
                            id
                        )

                        # ---------------------------------------------------------
                        # Build graph for measurement
                        plot = build_mpl_graph(
                                group=group,
                                poll_iso=poll_iso,
                                measure_id=id,
                                site_name=site_name,
                                dept_code=dept_code,
                                units=units,
                                hourly_data=group_data,
                                day_data=group_moymax_data,
                                weight_data=weight_data,
                                max_y_lim=max_y_lim,
                                y_ticks=y_ticks,
                        )

                        # ---------------------------------------------------------
                        # Save figure
                        file_name = ".".join(
                            [
                                "moygliss24h",
                                group,
                                f"{dept_code} {site_name}",
                                poll_iso,
                                "png"
                                ]
                        )

                        file_out = f"{args.output}/output/{file_name}"
                        list_of_files.append(file_name)
                        plot.savefig(file_out)
                        matplotlib.pyplot.close()

    with open(f"{args.output}/output/list", 'w') as f:
        for file in list_of_files:
            f.write(f"{file}\n")

sys.exit(0)
