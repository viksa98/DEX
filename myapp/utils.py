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
    xx =  mer.loc[:,['SKP-4','weight_num','IDupEnote','number of BO']]
    dist = mer.apply(lambda x: id_distance_time[x.IDupEnote][bo_id_upravne_enote]['lengthInMeters']/1000.,axis=1)
    travel_time = mer.apply(lambda x: id_distance_time[x.IDupEnote][bo_id_upravne_enote]['travelTimeInSeconds']/60.,axis=1)
    xx['distance_km'] = dist
    xx['travel_min'] = travel_time

    return xx

def get_occupation():
    occupations = cache.get("occ")
    if occupations is None:
        logger.info("Loading occupations")
        occupations = pd.read_excel(os.path.join(settings.DATA_ROOT, "SKP_ESCO.xlsx"))
        cache.add("occ", occupations, timeout=None)

    return occupations

def get_jobs():
    sif_skp = cache.get("sif_skp")
    skp_code = float(skp_code)
    if sif_skp is None:
        logger.info("Loading sif_skp")
        sif_skp = pd.read_csv(os.path.join(settings.DATA_ROOT, "dimSKP08.csv"))
        cache.set("sif_skp", sif_skp, timeout=None)
