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
    moyenne_gliss
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

    data = mask_aorp(data.set_index('date'))

    data_gliss = pd.DataFrame()
    for measure_id in poll_site_info['id'].to_list():
        pollsite = data[data['id'] == measure_id]
        data_gliss = pd.concat(
            [
                moyenne_gliss(
                    data=data[data['id'] == id],
                    measure_id=measure_id,
                    threshold=0.75
                    ).reset_index(),
                data_gliss
            ],
        )
        
