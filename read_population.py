import pandas as pd
import numpy as np

def pop_as_list():
    df = pd.read_excel('initial_pop_40.xlsx',engine='openpyxl', sheet_name=None)
    return df['pop'].values.tolist()

def list_to_dict(list):
    vars = dict()
    k = 0
    for item in list:
            vars[f"x{k:02}"] = item
            k += 1
    return vars

def flatten(list):
    return [item for sublist in list for item in sublist]

def divide(list,step=352):
    arr_of_arrs = []
    for i in range(0, len(list), step):
        x = i
        arr_of_arrs.append(list[x:x+step])
    return arr_of_arrs

def arr_to_nparr_dict(arr_of_arrs):
    arr_of_dict = []
    for arr in arr_of_arrs:
        arr_of_dict.append(list_to_dict(arr)) 
    return np.array(arr_of_dict)   

def read():
     pop = pop_as_list()
     pop = flatten(pop)
     pop = divide(pop)
     pop = arr_to_nparr_dict(pop)
     return pop
