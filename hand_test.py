from dss import dex
from dss import esco_utils
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
import bisect
import networkx as nx

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

# FIX THIS
dexmodel = dex.DEXModel('./data/SKP Evaluation version 3.xml')
esco = esco_utils.ESCOUtil()
occupations = pd.read_excel('./data/SKP_ESCO.xlsx')
napoved_year = 2018
napoved_period = 'I'

skp_skills = pd.read_pickle('./data/skp_skills_%d-%s.pcl' % (napoved_year,napoved_period) )
res = pd.read_pickle('./data/res_merged_2018.pcl')
id_distance_time = pickle.load( open('./data/id_dist_time.pcl','rb') )
job_contract_mer = pd.read_pickle('./data/elise/job_contract_type.pcl')
job_working_hours_mer = pd.read_pickle('./data/elise/job_job_working_hours.pcl')
DG = nx.read_gpickle('./data/elise/career_graph.pcl')
# FIX END

data = dict()
data['Languages'] = 'yes'
data['Driving licence'] = 'yes'
data['Age appropriateness'] = 'yes'
data['Disability appropriateness'] = 'yes'

#SKP Wish
#SKPvsESCO
# data['BO wishes for contract type'] = 0
#Job contract type

# data['BO career wishes'] = 0
#Job career advancement

# data['BO working hours wishes'] = 0
#Job working hours
#MSO Location
# data['BO wish location'] = 'yes'





default = dexmodel.get_intput_attributes()


skp_code = 3434.01 # Input
up_enota = 50 # Sk.Loka
data['BO wishes for contract type'] = 'full time'
# Career
data['BO career wishes'] = '*'
data['BO working hours wishes'] = 'daily shift'

wishes = [5120,5151,3322]
wishes_location = [59,60,61]

# There is a case when SKP4 is listed. SKP-6 has two 'decimal' digits. This line checks whether the code is SKP4 or SKP6
col_name = 'SKP koda-4' if int(skp_code) == skp_code else 'SKP koda-6'
bo_skills, bo_skill_opt = esco.get_all_skills_SKP2ESCO(occupations,  skp_code, col_name)
dif_skills = skp_skills.apply(lambda x: len(np.setdiff1d(x.skills, bo_skills)), axis=1)
resSKPs = select_positions(res, up_enota, id_distance_time)
dif_df = pd.DataFrame({'SKP-4':skp_skills['SKP-4'],'diff':dif_skills})
dex_df = pd.merge(resSKPs, dif_df, on='SKP-4')

pbar = tqdm()
pbar.reset(total=len(dex_df))
for r in dex_df.iterrows():
    vals = r[1]
    if '*' in wishes:
        data['SKP Wish'] = '*'
    else:
        data['SKP Wish'] = 'yes' if vals['SKP-4'] in wishes else 'no'
    ind = bisect.bisect_left([5,10], vals['diff'])
    data['SKPvsESCO'] = np.flipud(default['SKPvsESCO'])[ind]

    ind = bisect.bisect_left([10,50], vals['diff'])
    data['Available positions'] = default['Available positions'][ind]

    ind = bisect.bisect_left([10,20], vals['diff'])
    data['MSO'] = np.flipud(default['MSO'])[ind]

    # Job contract type
    wh = job_contract_mer['SFpoklicaSKP'].astype(int) == vals['SKP-4']
    if np.any(wh):
        contract_type = job_contract_mer[wh].sort_values(by='dosežene točke (0-100)').iloc[0]['delovni čas']
        if 'Kraj' in contract_type:
            data['Job contract type'] = 'part time'
        else:
            data['Job contract type'] = 'full time'
    else:
        data['Job contract type'] = '*'

    # Job career advancement
    try:
        adv = len(list(nx.all_simple_paths(DG, source=skp_code, target=int(vals['SKP-4']), cutoff=3)))
    except:
        adv = -1

    try:
        degrade = len(list(nx.all_simple_paths(DG, target=skp_code, source=int(vals['SKP-4']), cutoff=3)))
    except:
        degrade = -1

    if adv > degrade:
        data['Job career advancement'] = 'up'
    elif adv < degrade:
        data['Job career advancement'] = 'down'
    elif adv == -1 and degrade == -1:
        data['Job career advancement'] = '*'
    else:
        data['Job career advancement'] = 'same'


    # Job working hours
    wh = job_working_hours_mer['SFpoklicaSKP'].astype(int) == vals['SKP-4']
    if np.any(wh):
        working_hours = job_working_hours_mer[wh].sort_values(by='dosežene točke (0-100)').iloc[0]#['delovni čas']
        if working_hours['koda Urnik dela'] == 5:
            data['Job working hours'] = 'daily shift'
        else:
            data['Job working hours'] = 'daily/night shift'
    else:
        data['Job working hours'] = '*'

    #BO Wish location
    data['BO wish location'] = 'yes' if vals['IDupEnote'].astype(int) in wishes_location else 'no'

    eval_res, qq_res = dexmodel.evaluate_model(data)
    pbar.update()
