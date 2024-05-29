# Information polluants

INFOPOLS = {
    "24": {
        "nom": "PM10",
        "lim1": 50,
        "lim2": 80,
        "lim3": 400,
        "max": 100,
        "ann": "mean",
    },
    "39": {
        "nom": "PM2.5",
        "lim1": 15,
        "lim2": None,
        "lim3": None,
        "max": 60,
        "ann": "mean",
    },
    "68": {
        "nom": "PM1",
        "lim1": 12,
        "lim2": None,
        "lim3": None,
        "max": 50,
        "ann": "mean",
    },
    "08": {
        "nom": "O3",
        "lim1": 180,
        "lim2": 240,
        "lim3": None,
        "max": None,  # val_O3_max', '10
        "ann": "max",
    },
    "03": {
        "nom": "NO2",
        "lim1": 200,
        "lim2": 400,
        "lim3": None,
        "max": None,  # val_NO2_max', '10
        "ann": "max",
    },
    "01": {
        "nom": "SO2",
        "lim1": 125,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_SO2_max', '10
        "ann": "max",
    },
    "V4": {
        "nom": "Benzene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_BENZENE_max', '10
        "ann": "mean",
    },
    "VQ": {
        "nom": "Toluene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_TOLUENE_max', '10
        "ann": "mean",
    },
    "VU": {
        "nom": "M+P-Xylene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_MPXYLENE_max', '10
        "ann": "mean",
    },
    "VV": {
        "nom": "O-Xylene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_OXYLENE_max', '10
        "ann": "mean",
    },
    "V6": {
        "nom": "n-Butane",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_NBUTANE_max', '10
        "ann": "mean",
    },
    "V9": {
        "nom": "Ethylene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": 10,  # val_ETHYLENE_max', '10
        "ann": "mean",
    },
    "VB": {
        "nom": "Formaldehyde",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_FORMAL_max', '10
        "ann": "mean",
    },
    "OA": {
        "nom": "Cyclohexane",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_CYCLO_max', '10
        "ann": "mean",
    },
    "V0": {
        "nom": "1,3-Butadiene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_BUTADIENE_max', '10
        "ann": "mean",
    },
    "T3": {
        "nom": "NbParticule",
        "lim1": 10000,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_NbP_max', '10
        "ann": "mean",
    },
    "VA": {
        "nom": "Ethylbenzene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_ETHYLBENZ_max', '10
        "ann": "mean",
    },
    "0N": {
        "nom": "ChlorureDeVinyle",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_CVM_max', '10
        "ann": "mean",
    },
    "H9": {
        "nom": "1,2-Dichloroethane",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,  # val_DCE_max', '10
        "ann": "mean",
    },
    "05": {
        "nom": "H2S",
        "lim1": 150,
        "lim2": None,
        # seuil nuissance olfactive (7 µg/m3) sur une demi-heure
        # (nuisance olfactive) OMS(2000))
        "lim3": 7,
        "max": None,  # val_H2S', '10
        "ann": "max",
    },
    'ML': {
        "nom": "Métaux Lourds",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    },
    'BTEX': {
        "nom": "BTEX",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    },
    'COVle': {
        "nom": "COV Légères",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    },
    'COVlo': {
        "nom": "COV Lourds",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    },
}

METAUX_LOURDS = ['9G', '9I', '9P', '9Q', '9R', '9S', '9T', '9U', '9V',
                 '9W', '9X', '9Y', '9a', '9c', '9d', '9e', '9g', '3Z',
                 '9h', '9i', '9p', '9q', '9s', '9u', '9v',]

BTEX = ['V4', 'VQ', 'VA', 'VU',  'VV',]

COV_LEGERES = ['V6', 'VD', 'V0', '0N', 'V9', 'V8', 'VP',
               'VN', 'V3', 'V2', 'V1', 'V7', 'Ut', 'WH',
               'VI', 'VK', 'VF', 'W7', 'VL', 'O3', 'O7',
               'OC', 'WD', 'V5', 'WI',]

COV_LOURDS = ['V4', 'VQ', 'VA', 'VU', 'VV', 'H9', 'OA',
              'H3', 'H4', 'R2', 'QA', 'WB', 'WD', 'VE',
              'R4', 'VR', 'VS', 'VT', 'VG', 'W6', 'VX',
              'VH', 'Vd', 'VC',]

POLL_AGG_LIST = {
    'V_MART': {
        'ML': {'sites': ['FSCB'],
               'iso_list': METAUX_LOURDS},
    },
    'V_MARS': {
        'ML': {'sites': ['CINQAV'],
               'iso_list': METAUX_LOURDS},
        },
    'V_COV': {
        'BTEX': {
            'sites': ['FSCB', 'BETG', 'MLVR',
                      'MOBILE_14', 'PDBL', 'PENHUV',
                      'RBRT'],
            'iso_list': BTEX
        },
        'COVle': {
            'sites': ['BETG', 'MLVR', 'PDBL'],
            'iso_list': COV_LEGERES
        },
        'COVlo': {
            'sites': ['BETG', 'MLVR', 'PDBL'],
            'iso_list': COV_LOURDS
        }
    },
}


JSON_PATH_LISTS = {
    'sites': {
        'record_path': None,
        'meta': [
            'labelSite',
            ['address', ['department', 'id']],
        ]
    },
    'measures': {
        'record_path': None,
        'meta': [
            'id',
            ['site', 'id'],
            ['physical', 'tagPhy'],
            ['physical', 'id'],
            ['unit', 'id'],
        ],
    },
    'data': {
        'record_path': ['hourly', 'data',],
        'meta': [
            'id',
            ['hourly', 'unit', 'id'],
        ],
    },
    'physicals': {
        'record_path': None,
        'meta': None,
    },
}


HEADER_RENAME_LISTS = {
    'sites': {
        'id': 'labelSite',
        'address.department.id': 'dept_code',
    },
    'measures': {
        'id': 'id',
        'site.id': 'id_site',
        'physical.tagPhy': 'phy_name',
        'physical.id': 'id_phy',
        'unit.id': 'unit',
    },
    'data': {
        'id': 'id',
        'hourly.unit.id': 'unit',
        'value': 'value',
        'date': 'date',
        'state': 'state',
    },
    'physicals': {
        'id': 'id',
        'chemicalSymbol': 'chemicalSymbol',
        'label': 'long_name',
    },
}


MATPLOT_PARAMS = {
    "axes.labelsize": 9,
    "font.size": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 9,
}

URL_DICT = {
    "data": "https://172.16.13.224:8443/dms-api/public/v2/data?",
    "sites": "https://172.16.13.224:8443/dms-api/public/v2/sites?",
    "physicals": "https://172.16.13.224:8443/dms-api/public/v1/physicals?",
    "measures": "https://172.16.13.224:8443/dms-api/public/v2/measures?",
}

DATA_KEYS = {
    "data": "data",
    "sites": "sites",
    "physicals": "physicals",
    "measures": "measures",
}

GROUP_LIST = ["DIDON", "V_NICE", "V_MARS", "V_MART"]
