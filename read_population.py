import pandas as pd
import numpy as np
import trgep_toolbox as trgeptb
# EXCELI OKUYOR
def pop_as_list(path):
    df = pd.read_excel(path,engine='openpyxl', sheet_name=None)
    return df['pop'].values.tolist()
#in_pop_cost_20
#in_pop_em_20
#initial_pop_40

# LİSTEYİ DİCTRİONARY E ÇEVİRİYOR
def list_to_dict(list):
    vars = dict()
    k = 0
    for item in list:
            vars[f"x{k:02}"] = item
            k += 1
    return vars

# VEKTÖRE ÇEVİRİYOR
def flatten(list):
    return [item for sublist in list for item in sublist]

# VEKTÖRÜ 352 Lİ OLARAK BÖLÜYOR
def divide(list,step=352):
    arr_of_arrs = []
    for i in range(0, len(list), step):
        x = i
        arr_of_arrs.append(list[x:x+step])
    return arr_of_arrs

# ARRAYLERİ DICTIONARY E CEVIRIYOR
def arr_to_nparr_dict(arr_of_arrs):
    arr_of_dict = []
    for arr in arr_of_arrs:
        arr_of_dict.append(list_to_dict(arr)) 
    return np.array(arr_of_dict)   

# İLK ÇALIŞAN FONKSİYON
def read(path):
     pop = pop_as_list(path)
     pop = flatten(pop)
     pop = divide(pop)
     pop = arr_to_nparr_dict(pop)
     return pop


def pop_to_excel(pop):
    gene_list = []
    for ind in pop:
        if len(gene_list) == 0:
            gene_list = trgeptb.reshape_to_matrix([ind.X[f"x{k:02}"] for k in range(0, 352)],is_full=True)
        else:
            temp = trgeptb.reshape_to_matrix([ind.X[f"x{k:02}"] for k in range(0, 352)],is_full=True)
            gene_list = np.vstack((gene_list,temp))
    df = pd.DataFrame(gene_list)
    df.to_excel(f'best{len(pop)}_2f.xlsx', index=False, header=False)