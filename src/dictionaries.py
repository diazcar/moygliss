import pandas as pd


INFOPOLS = {
    "24": {
        "nom": "PM10",
        "lim1": 50,
        "lim2": 80,
        "lim3": 460,  # 400 ancienne?
        "max": 100,
        "ann": "mean",
    },
    "39": {
        "nom": "PM2.5",
        "lim1": 15,
        "lim2": 25,
        "lim3": 170,
        "max": 60,
        "ann": "mean",
    },
    "68": {
        "nom": "PM1",
        "lim1": 12,
        "lim2": None,
        "lim3": 130,
        "max": 60,
        "ann": "mean",
    },
    'GA': {
        "nom": "BC Wood Burnning",
        "lim1": None,
        "lim2": None,
        "lim3": 5,
        "max": None,
        "ann": "max",
    },
    'GB': {
        "nom": "BC Fuel Fossil",
        "lim1": None,
        "lim2": None,
        "lim3": 15,
        "max": None,
        "ann": "max",
    },
    "08": {
        "nom": "O3",
        "lim1": 180,
        "lim2": 240,  # 240?
        "lim3": 200,
        "max": None,
        "ann": "max",
    },
    "03": {
        "nom": "NO2",
        "lim1": 200,
        "lim2": 400,  # 400 ?
        "lim3": 170,
        "max": None,
        "ann": "max",
    },
    "01": {
        "nom": "SO2",
        "lim1": 125,
        "lim2": None,
        "lim3": 210,
        "max": None,
        "ann": "max",
    },
    "V4": {
        "nom": "Benzene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "VQ": {
        "nom": "Toluene",
        "lim1": 5,
        "lim2": None,
        "lim3": 140,
        "max": None,
        "ann": "mean",
    },
    "VU": {
        "nom": "M+P-Xylene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "VV": {
        "nom": "O-Xylene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    # "V6": {
    #     "nom": "n-Butane",
    #     "lim1": 5,
    #     "lim2": None,
    #     "lim3": None
    #     "max": None,
    #     "ann": "mean",
    # },
    # "V9": {
    #     "nom": "Ethylene",
    #     "lim1": 5,
    #     "lim2": None,
    #     "lim3": None
    #     "max": 10,  #
    #     "ann": "mean",
    # },
    "VB": {
        "nom": "Formaldehyde",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "OA": {
        "nom": "Cyclohexane",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "V0": {
        "nom": "1,3-Butadiene",
        "lim1": 5,
        "lim2": None,
        "lim3": 140,
        "max": None,
        "ann": "mean",
    },
    "T3": {
        "nom": "NbParticule",
        "lim1": 10000,
        "lim2": None,
        "lim3": 100000,
        "max": None,
        "ann": "mean",
    },
    "VA": {
        "nom": "Ethylbenzene",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "0N": {
        "nom": "ChlorureDeVinyle",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": 280,
        "ann": "mean",
    },
    "H9": {
        "nom": "1,2-Dichloroethane",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "H8": {
        "nom": "1,2-Dichloroethylène",
        "lim1": 5,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "mean",
    },
    "05": {
        "nom": "H2S",
        "lim1": 150,
        "lim2": None,
        # seuil nuissance olfactive (7 µg/m3) sur une demi-heure
        # (nuisance olfactive) OMS(2000))
        "lim3": 7,
        "max": None,
        "ann": "max",
    },
    'MLPM1': {
        "nom": "Métaux Lourds in PM1",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    },
    'MLPM10': {
        "nom": "Métaux Lourds in PM10",
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
        "nom": "COV Légers",
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
    "BC": {
        "nom": "Black Carbon",
        "lim1": None,
        "lim2": None,
        "lim3": 15,
        "max": None,
        "ann": "max",
    },
    "COVpcop": {
        "nom": "All COV",
        "lim1": None,
        "lim2": None,
        "lim3": None,
        "max": None,
        "ann": "max",
    }
}

METAUX_LOURDS_PM1 = ['9G', '9I', '9P', '9Q', '9R', '9S', '9T', '9U', '9V',
                     '9W', '9X', '9Y', '9a', '9c', '9d', '9e', '9g', '3Z',
                     '9h', '9i', '9p', '9q', '9s', '9u', '9v',]

METAUX_LOURDS_PM10 = ['14', '19', '2t', '2y', '3B', '3C', '3E', '3J', '3K',
                      '3O', '3T', '3U', '3W', '3Y', '3Z', '3a', '4D', '4J',
                      '4K', '4O', '4Q', '79', '80', '82', '83', '84', '85',
                      '86', '87', '88', '90', '91', '92', '93', '94', '96',
                      '9J', 'B2']
BTEX = ['V4', 'VQ', 'VA', 'VU',  'VV',]  # 5

COV_LEGERES = ['V6', 'VD', 'V0', '0N', 'V9', 'V8', 'VP',
               'VN', 'V3', 'V2', 'V1', 'V7', 'Ut', 'WH',
               'VI', 'VK', 'VF', 'W7', 'VL', 'O3', 'O7',
               'OC', 'WD', 'V5', 'WI',]  # 25

COV_LOURDS = ['V4', 'VQ', 'VA', 'VU', 'VV', 'H9', 'OA',
              'H3', 'H4', 'R2', 'QA', 'WB', 'WD', 'VE',
              'R4', 'VR', 'VS', 'VT', 'VG', 'W6', 'VX',
              'VH', 'Vd', 'VC',]  # 24

ALL_COV = [
    'V6', 'VD', 'V0', '0N', 'V9', 'V8', 'VP', 'VN', 'V3',
    'V2', 'V1', 'V7', 'Ut', 'WH', 'VI', 'VK', 'VF', 'W7',
    'VL', 'O3', 'O7', 'OC', 'WD', 'V5', 'WI', 'V4', 'VQ',
    'VA', 'VU', 'VV', 'H9', 'OA', 'H3', 'H4', 'R2', 'QA',
    'WB', 'WD', 'VE', 'R4', 'VR', 'VS', 'VT', 'VG', 'W6',
    'VX', 'VH', 'Vd', 'VC',
    ]  # 49

BLACK_CARBON = ['GA', 'GB']

FAMILY_LIST = ['MLPM1', 'MLPM10', 'BC']

COV_FAMILIES = ['BTEX', 'COVle', 'COVlo', 'COVpcop']

POLL_AGG_LIST = {
    'XLBC': {
        'BC': {
                'sites': ['GAPCOM', 'ARSON',
                          'CINQAV', 'MOBILE_12',
                          'RABATA', 'PLOMBIERES',
                          'MOBILE_13'
                ],
                'iso_list': BLACK_CARBON,
        }
    },
    'DIDON': {
        'BC': {
            'sites': ['GAPCOM', 'ARSON',
                      'CINQAV', 'MOBILE_12',
                      'RABATA', 'PLOMBIERES',
                      'MOBILE_13'
            ],
            'iso_list': BLACK_CARBON,
        }
    },
    'V_MART': {
        'MLPM1': {
            'sites': ['FSCB'],
            'iso_list': METAUX_LOURDS_PM1
        },
    },
    'V_MARS': {
        'MLPM10': {
            'sites': ['CINQAV'],
            'iso_list': METAUX_LOURDS_PM10
            },
        },
    'V_COV': {
        'BTEX': {
            'sites': ['FSCB', 'BETG', 'MLVR',
                      'MOBILE_14', 'PDBL', 'PENHUV',
                      'RBRT', 'MOBILE_15'],
            'iso_list': BTEX
        },
        'COVle': {
            'sites': ['BETG', 'MLVR', 'PDBL'],
            'iso_list': COV_LEGERES
        },
        'COVlo': {
            'sites': ['BETG', 'MLVR', 'PDBL'],
            'iso_list': COV_LOURDS
        },
        'COVpcop': {
            'sites': ['BETG', 'MLVR', 'PDBL'],
            'iso_list': ALL_COV
        },
    },
}


JSON_PATH_LISTS = {
    'sites': {
        'record_path': None,
        'meta': [
            'id',
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
        'id': 'id',
        'labelSite': 'labelSite',
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

GROUP_LIST = ["DIDON", "V_NICE", "V_MARS", "V_MART", "V_COV"]

PCOP_DATA = pd.read_csv("./data/cov_pcop.csv", delimiter=';')
