from dss import dex
from dss import esco_utils
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
import bisect
import networkx as nx
from django.conf import settings
from django.core.cache import cache
import os

import logging

logger = logging.getLogger("root")

'''
The function generates a DataFrame that include SKP4, number of positions, number of matching BO in same Municipality, distance of BO, and travel for BO
'''
def select_positions(mer, bo_id_upravne_enote, id_distance_time):#, distance=10):

    '''
    key, values = zip(*id_distance_time[bo_id_upravne_enote].items())
    values = np.array(values)
    key = np.array(key)
    wh = mer.IDupEnote.isin(key[np.array(values) < distance])
    xx =  mer.loc[wh,['SKP-4','weight_num','IDupEnote','number of BO']]
    dist = mer[wh].apply(lambda x: id_distance[x.IDupEnote][64],axis=1)
    xx['distance'] = dist
    '''

    xx =  mer.loc[:,['SKP-6','weight_num','IDupEnote','number of BO']]
    dist = mer.apply(lambda x: id_distance_time[x.IDupEnote][bo_id_upravne_enote]['lengthInMeters']/1000.,axis=1)
    travel_time = mer.apply(lambda x: id_distance_time[x.IDupEnote][bo_id_upravne_enote]['travelTimeInSeconds']/60.,axis=1)
    xx['distance_km'] = dist
    xx['travel_min'] = travel_time

    return xx

def __load_df(path):
    if path.endswith('csv'):
        return pd.read_csv(path)
    elif path.endswith('pcl'):
        return pd.read_pickle(path)
    else:
        return pd.read_excel(path)

def __get_load(file_name, key):
    return __load_df(os.path.join(settings.DATA_ROOT, file_name))
    df = cache.get(key)
    if df is None:
        logger.info("Loading %s" % key)
        df = __load_df(os.path.join(settings.DATA_ROOT, "SKP_ESCO.xlsx"))
        cache.add(key, df, timeout=None)
    return df

def get_language():
    return __get_load("elise/language.pcl", "language")

def get_driver_lic():
    return __get_load("elise/driving_licence.pcl", "driving_licence")

def get_occupation():
    return __get_load("SKP_ESCO.xlsx", "occ")

def get_ue():
    ue = __get_load("sifUpravneEnote.csv","ue")
    ue = ue[ue.StatusSF == 'A']
    return ue

def get_jobs():
    return __get_load("dimSKP08.csv","sif_skp")
