# Information polluants
INFOPOLS = {
    "24": {
        "nom": "PM10",
        "lim1": 50,
        "lim2": 80,
        "lim3": 400,
        "max": 100,
    },
    "39": {
        "nom": "PM2.5",
        "lim1": 15,
        "lim2": None,
        "max": 60,
    },
    "68": {
        "nom": "PM1",
        "lim1": 12,
        "lim2": None,
        "max": 50,
    },
    "08": {
        "nom": "O3",
        "lim1": 180,
        "lim2": 240,
        "max": 270,  # val_O3_max + 10
    },
    "03": {
        "nom": "NO2",
        "lim1": 200,
        "lim2": 400,
        "max": 70,  # val_NO2_max + 10
    },
    "01": {
        "nom": "SO2",
        "lim1": 125,
        "lim2": None,
        "max": 150,  # val_SO2_max + 10
    },
    "V4": {
        "nom": "Benzene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_BENZENE_max + 10
    },
    "VQ": {
        "nom": "Toluene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_TOLUENE_max + 10
    },
    "VU": {
        "nom": "M+P-Xylene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_MPXYLENE_max + 10
    },
    "VV": {
        "nom": "O-Xylene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_OXYLENE_max + 10
    },
    "V6": {
        "nom": "n-Butane",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_NBUTANE_max + 10
    },
    "V9": {
        "nom": "Ethylene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_ETHYLENE_max + 10
    },
    "VB": {
        "nom": "Formaldehyde",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_FORMAL_max + 10
    },
    "OA": {
        "nom": "Cyclohexane",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_CYCLO_max + 10
    },
    "V0": {
        "nom": "1,3-Butadiene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_BUTADIENE_max + 10
    },
    "T3": {
        "nom": "NbParticule",
        "lim1": 10000,
        "lim2": None,
        "max": 50000,  # val_NbP_max + 10
    },
    "VA": {
        "nom": "Ethylbenzene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_ETHYLBENZ_max + 10
    },
    "0N": {
        "nom": "ChlorureDeVinyle",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_CVM_max + 10
    },
    "H9": {
        "nom": "1,2-Dichloroethane",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_DCE_max + 10
    },
    "05": {
        "nom": "H2S",
        "lim1": 150,
        "lim2": None,
        # seuil nuissance olfactive (7 µg/m3) sur une demi-heure
        # (nuisance olfactive) OMS(2000))
        "lim3": 7,
        "max": 15,  # val_H2S + 10
    },
}

# Paramètres matplotlib
MATPLOT_PARAMS = {
    "axes.labelsize": 9,
    "font.size": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
}

URL_DICT = {
    "data": "https://172.16.13.224:8443/dms-api/public/v2/data?",
    "sites": "https://172.16.13.224:8443/dms-api/public/v2/sites?",
    "physicals": "https://172.16.13.224:8443/dms-api/public/v2/physicals?",
    "measures": "https://172.16.13.224:8443/dms-api/public/v2/measures?",
}

DATA_KEYS = {
    "data": "data",
    "sites": "sites",
    "physicals": "physicals",
    "measures": "measures",
}

GROUP_LIST = ["DIDON", "V_NICE", "V_MARS", "V_MART"]
