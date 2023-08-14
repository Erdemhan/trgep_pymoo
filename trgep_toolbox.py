import read_excel as reader
import consts as const
import constst_debug as cdbg
import numpy as np
import copy 
import read_population as pop_reader
from trgepRepair import TrgepRepair
from result import print_result

data = reader.read()

# 16x11 Matris şeklinde kapasiteleri dönderiyor
def kapasite_hesapla_cumulative(genes):
    genes = copy.deepcopy(reshape_to_matrix(genes,is_full=False))
    exist = copy.deepcopy(data['exists'])
    kapasiteler = []

    for i in range(11):
        exist[i] = exist[i]*data['hours'][i]

    for i in range(16):
        kapasiteler.append(kapasite_hesapla_yil_mwh(genes[0:i+1],exist))

    return kapasiteler
# 1x11 Vektör şeklinde yıllık kapasiteleri dönderiyor
def kapasite_hesapla_yil_mwh(inv_genes_v,exist):
    kapasiteler = np.empty(11)
    temp = []
    units = inv_genes_v.sum(axis=0)
    for i in range(11):
        kapasiteler[i] = units[i]*data['initial_cap'][i]*data['hours'][i]

    temp.append(kapasiteler)
    temp.append(exist)
    temp = [sum(x) for x in zip(*temp)]
    return temp


# Vektörü 11*16  matris e çeviriyor , is generation True ise 0:176 (generation genleri) False ise 176:352 (investment genleri)
def reshape_to_matrix(vector,is_generation=True,is_full=True):
    if is_full:
        if is_generation:
            vector = vector[:176]
        else:
            vector = vector[176:]
    matrix = [ [ 0 for i in range(11) ] for j in range(16) ]
    ctr = 0

    for i in range(16):
        for j in range(11):
            matrix[i][j] = vector[ctr]
            ctr +=1

    return matrix


def const_check(individual,data):
    return const.check_constraints(individual,data)

def const_check_debug(individual,data):
    return cdbg.check_constraints(individual,data)

def read_population():
    return pop_reader.read()

def repair():
    return TrgepRepair()

def show_result(problem,res):
    print_result(problem,res)