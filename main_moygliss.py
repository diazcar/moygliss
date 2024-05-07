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
    request_xr,
    build_dataframe,
    test_path,
    float_none,
    test_valid,
    list_of_days,
    day_of_month,
    date_last_weekday,
    time_window
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

    data = build_dataframe(
        data=request_xr(
            fromtime=time_window[0],
            totime=time_window[1],
            folder="data",
            poll_site_info=",".join(poll_site_info['id'].to_list())
            ),
        header=['id', 'date', 'value', 'state']

        )

    
    for measure in poll_site_info['id'].to_list():
        pollsite = data[data['id'] == measure]

        (
            moyenne_gliss,
            max_jour,


        )
