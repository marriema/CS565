import numpy as np
import pandas as pd

def get_topk_factors(data_list):
    df_data = {'mood1':[], 'mood2':[], 'alcohol':[], 'caffeine':[], 'sugar':[], 'water':[], 'sleep':[], 'social':[], 'eat':[], 'exercise':[]};
    for item in data_list:
        print(item)
        if 'mood1' in items['moods']:
            df_data['mood1'].append(item['moods']['mood1'])
        else:
            df_data['mood1'].append(-1)
        df_data['mood2'].append(item['moods']['mood2'])
        df_data['alcohol'].append(item['factors']['alcohol'])
        df_data['caffeine'].append(item['caffeine'])
        df_data['sugar'].append(item['sugar'])
        df_data['water'].append(item['water'])
        df_data['sleep'].append(item['sleep'])
        df_data['social'].append(item['social'])
        df_data['eat'].append(item['eat'])
        df_data['exercise'].append(item['exercise'])
    return df_data
