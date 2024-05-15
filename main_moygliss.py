from datetime import datetime
import pandas as pd

from src.dictionaries import  (
    INFOPOLS,
    MATPLOT_PARAMS,
    URL_DICT,
    DATA_KEYS,
    GROUP_LIST
    )


from src.fonctions import (
    mask_aorp,
    request_xr,
    build_dataframe,
    test_path,
    float_none,
    test_valid,
    list_of_days,
    day_of_month,
    date_last_weekday,
    time_window,
    get_rolling_data
    )


if __name__ == "__main__":
    for group in GROUP_LIST:
        poll_site_info = pd.DataFrame(
            request_xr(
                folder="measure",
                groups="DIDON"
            ),
            columns=[
                'id',
                'id_site',
                'phy_name',
                'id_phy',
                'unit',
                ]
            )

    data = request_xr(
        fromtime="2024-01-01T00:00:00Z",
        totime="2024-01-05T00:00:15Z",
        folder="data",
        measures=",".join(poll_site_info['id'].to_list()),
        datatype="hourly",
        header_for_df=['id', 'date', 'value', 'state']
        )

    data = mask_aorp(data.set_index('date'))
    data['moygliss24'] = data['value'].rolling(window=24).mean()

    moymax_data = pd.DataFrame()
    for measure_id in poll_site_info['id'].to_list():
        pollsite = data[data['id'] == measure_id]
        moymax_data = pd.concat(
            [
                get_rolling_data(
                    data=data[data['id'] == id],
                    measure_id=measure_id,
                    poll_site_info=poll_site_info,
                    threshold=0.75
                    ).reset_index(),
                moymax_data
            ],
        )
