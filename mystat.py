import numpy as np
import pandas as pd
import math

def get_topk_factors(data_list, k):
    df_data = {'mood1':[], 'mood2':[], 'alcohol':[], 'caffeine':[], 'sugar':[], 'water':[], 'sleep':[], 'social':[], 'eat':[], 'exercise':[]};
    farr = ['alcohol', 'caffeine', 'sugar', 'water', 'sleep', 'social', 'eat', 'exercise']
    marr = ['mood1', 'mood2']
    for item in data_list:
        print(item)
        for m in marr:
            if m in item['moods']:
                df_data[m].append(item['moods'][m])
            else:
                df_data[m].append(-1)
        for f in farr:
            if f in item['factors']:
                df_data[f].append(item['factors'][f])
            else:
                df_data[f].append(-1)
    df = pd.DataFrame(data=df_data)
    print(df)
    corr = df.corr()
    print('corr')
    print(corr)

    arr = np.array(corr['mood1'])
    indices = np.argsort(arr)

    ret1 = []
    ret2 = []
    cols = df.columns.values;
    cols = list(cols)
    #cols.reverse()
    print('cols:')
    print(cols)
    print('indices:')
    print(indices)
    print('arr:')
    print(arr)

    indices = indices.tolist()
    reversed_indices = indices[:]
    reversed_indices.reverse()
    cnt = 0
    for index, index_val in enumerate(reversed_indices):
        if math.isnan(arr[index_val]) or cols[index_val] == 'mood1' or cols[index_val] == 'mood2':
            continue
        if cnt >= k or arr[index_val] <= 0:
            break
        cnt += 1
        ret1.append({'name':cols[index_val], 'score': arr[index_val]})
    cnt = 0
    for index, index_val in enumerate(indices):
        if math.isnan(arr[index_val]) or cols[index_val] == 'mood1' or cols[index_val] == 'mood2':
            continue
        if cnt >= k or arr[index_val] >= 0:
            break
        cnt += 1
        ret2.append({'name':cols[index_val], 'score': arr[index_val]})

    ret = {'positive':ret1, 'negative':ret2}
    return ret

def get_all_factors_score(data_list):
    df_data = {'mood1':[], 'mood2':[], 'alcohol':[], 'caffeine':[], 'sugar':[], 'water':[], 'sleep':[], 'social':[], 'eat':[], 'exercise':[]};
    farr = ['alcohol', 'caffeine', 'sugar', 'water', 'sleep', 'social', 'eat', 'exercise']
    marr = ['mood1', 'mood2']
    for item in data_list:
        print(item)
        for m in marr:
            if m in item['moods']:
                df_data[m].append(item['moods'][m])
            else:
                df_data[m].append(-1)
        for f in farr:
            if f in item['factors']:
                df_data[f].append(item['factors'][f])
            else:
                df_data[f].append(-1)
    df = pd.DataFrame(data=df_data)
    corr = df.corr()
    print('corr')
    print(corr)

    arr = np.array(corr['mood1'])
    indices = np.argsort(arr)

    ret = []
    cols = df.columns.values;
    cols = list(cols)

    indices = indices.tolist()
    reversed_indices = indices[:]
    reversed_indices.reverse()

    for index, index_val in enumerate(indices):
        if cols[index_val] == 'mood1' or cols[index_val] == 'mood2':
            continue
        ret.append({'name':cols[index_val], 'score': arr[index_val]})
    return ret
