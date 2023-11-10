import copy 
import numpy as np
from deap import  creator

capConstaintDict = dict()
nucConstraintInd = dict()
datas = []
# Kaynakların her yıl için kapasitesini üretir 16x11 matris dönderiyor
def kapasite_hesapla_cumulative(inv_genes):
    genes = copy.deepcopy(inv_genes)
    exist = copy.deepcopy(datas['exists'])
    kapasiteler = []

    for i in range(11):
        exist[i] = exist[i]*datas['hours'][i]

    for i in range(16):
        kapasiteler.append(kapasite_hesapla_yil_mwh(genes[0:i+1],exist))

    return kapasiteler

def kapasite_hesapla_yil_mwh(inv_genes_v,exist):
    kapasiteler = np.empty(11)
    temp = []
    units = inv_genes_v.sum(axis=0)
    for i in range(11):
        kapasiteler[i] = units[i]*datas['initial_cap'][i]*datas['hours'][i]

    temp.append(kapasiteler)
    temp.append(exist)
    temp = [sum(x) for x in zip(*temp)]
    return temp


# ILK ÇALIŞAN FONKSİYON
def check_constraints(individual,data):
    global datas
    datas = data
    temp = individual
    individual = np.array(individual).reshape(32,11)
    demands = data['demand']
    peakDemand = data['peaks']
    constructionLimit = data['climit']
    genAmount = individual[0:16, :]
    investedNum = individual[16:32, :]
    capacities = kapasite_hesapla_cumulative(individual[16:32, :])

    return nuclear_constraint(investedNum),capacity_constraint(genAmount, capacities),demand_constraint(genAmount, demands),peak_demand_constraint(peakDemand, capacities),construction_limit_constraint(investedNum, constructionLimit),capConstaintDict,nucConstraintInd


# mwh dogru
# DEMAND VIOILATION HESAPLIYOR
def demand_constraint(genAmount, demands):
    annualProd = 0.0
    fark = 0.0

    for year in range(16):
        annualProd = 0.0
        for unitType in range(11):
            annualProd += genAmount[year][unitType]
        if annualProd < demands[year]:
            fark += demands[year] - annualProd

    return fark


#mwh olacak dogru
# KAPASITE VIOLATION
def capacity_constraint(birey, capacities):  # whatsapp
    capConstaintDict.clear()
    fark = 0.0
    key = 0
    for year in range(16):
        for unitType in range(11):
            if birey[year][unitType] > capacities[year][unitType]:
                    fark = birey[year][unitType] - capacities[year][unitType]
                    capConstaintDict[f'x{key:02}'] = fark
                    fark += fark
            key += 1
    return fark


# mw dogru
def peak_demand_constraint(peakDemand, capacities):  # whatsapp
    annualCap = 0.0
    fark = 0.0

    for year in range(16):
        annualCap = 0.0
        for unitType in range(11):
            annualCap += (capacities[year][unitType] / datas['hours'][unitType])
        if annualCap < peakDemand[year]:
            fark += peakDemand[year] - annualCap

    # 6240 ortalama çalışma saati farkı mw den mwh ye çevirdi
    return fark*6240


def construction_limit_constraint(investedNum, constructionLimit):
    fark = 0.0

    for i in range(16):
        for unitType in range(11):
            if investedNum[i][unitType] > constructionLimit[unitType]:
                fark = investedNum[i][unitType] - constructionLimit[unitType]

    return fark


# NUKLEER VIOLATION
def nuclear_constraint(investedNum): 
    '''
    0    1   2   3   4   5   6   7   8   9  10   ... 175
    176 177 178 179 180 181 182 183 184 185 186  ... 351
    '''
    fark = 0.0
    key = 181
    for year in range(11): # ilk 11 yıl nuc 0, toplam 16 yıl
        #if investedNum[year][5] != 0:  # 5 for nuclear
        fark = investedNum[year][5]
        nucConstraintInd[f'x{key-176:02}'] = 0 #debugging takip için
        nucConstraintInd[f'x{key:02}'] = fark
        key += 11
    return fark


def positive_variables_constraint(genAmount, investedNum):
    fark = 0.0

    for year in range(16):
        for unitType in range(11):
            if genAmount[year][unitType] < 0 or investedNum[year][unitType] < 0:
                fark += 1

    return fark

