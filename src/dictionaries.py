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
        "max": 60,
        "ann": "mean",
    },
    "68": {
        "nom": "PM1",
        "lim1": 12,
        "lim2": None,
        "max": 50,
        "ann": "mean",
    },
    "08": {
        "nom": "O3",
        "lim1": 180,
        "lim2": 240,
        "max": None,  # val_O3_max + 10
        "ann": "max",
    },
    "03": {
        "nom": "NO2",
        "lim1": 20,
        "lim2": 40,
        "max": None,  # val_NO2_max + 10
        "ann": "max",
    },
    "01": {
        "nom": "SO2",
        "lim1": 125,
        "lim2": None,
        "max": None,  # val_SO2_max + 10
        "ann": "max",
    },
    "V4": {
        "nom": "Benzene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_BENZENE_max + 10
        "ann": "mean",
    },
    "VQ": {
        "nom": "Toluene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_TOLUENE_max + 10
        "ann": "mean",
    },
    "VU": {
        "nom": "M+P-Xylene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_MPXYLENE_max + 10
        "ann": "mean",
    },
    "VV": {
        "nom": "O-Xylene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_OXYLENE_max + 10
        "ann": "mean",
    },
    "V6": {
        "nom": "n-Butane",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_NBUTANE_max + 10
        "ann": "mean",
    },
    "V9": {
        "nom": "Ethylene",
        "lim1": 5,
        "lim2": None,
        "max": 10,  # val_ETHYLENE_max + 10
        "ann": "mean",
    },
    "VB": {
        "nom": "Formaldehyde",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_FORMAL_max + 10
        "ann": "mean",
    },
    "OA": {
        "nom": "Cyclohexane",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_CYCLO_max + 10
        "ann": "mean",
    },
    "V0": {
        "nom": "1,3-Butadiene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_BUTADIENE_max + 10
        "ann": "mean",
    },
    "T3": {
        "nom": "NbParticule",
        "lim1": 10000,
        "lim2": None,
        "max": None,  # val_NbP_max + 10
        "ann": "mean",
    },
    "VA": {
        "nom": "Ethylbenzene",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_ETHYLBENZ_max + 10
        "ann": "mean",
    },
    "0N": {
        "nom": "ChlorureDeVinyle",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_CVM_max + 10
        "ann": "mean",
    },
    "H9": {
        "nom": "1,2-Dichloroethane",
        "lim1": 5,
        "lim2": None,
        "max": None,  # val_DCE_max + 10
        "ann": "mean",
    },
    "05": {
        "nom": "H2S",
        "lim1": 150,
        "lim2": None,
        # seuil nuissance olfactive (7 µg/m3) sur une demi-heure
        # (nuisance olfactive) OMS(2000))
        "lim3": 7,
        "max": None,  # val_H2S + 10
        "ann": "max",
    },
}

# Paramètres matplotlib
MATPLOT_PARAMS = {
    "axes.labelsize": 9,
    "font.size": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 9,
}

URL_DICT = {
    "data": "https://172.16.13.224:8443/dms-api/public/v2/data?",
    "sites": "https://172.16.13.224:8443/dms-api/public/v2/sites?",
    "physicals": "https://172.16.13.224:8443/dms-api/public/v2/physicals?",
    "measures": "https://172.16.13.224:8443/dms-api/public/v1/measures?",
}

DATA_KEYS = {
    "data": "data",
    "sites": "sites",
    "physicals": "physicals",
    "measures": "measures",
}

GROUP_LIST = ["DIDON", "V_NICE", "V_MARS", "V_MART"]
