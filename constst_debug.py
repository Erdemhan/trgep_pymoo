import copy 
import numpy as np
from deap import  creator

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



def check_constraints(individual,data):
    global datas
    datas = data
    individual = np.array(individual).reshape(32,11)
    demands = data['demand']
    peakDemand = data['peaks']
    constructionLimit = data['climit']
    genAmount = individual[0:16, :]
    investedNum = individual[16:32, :]
    capacities = kapasite_hesapla_cumulative(individual[16:32, :])

    totalFark = 0.0

    totalFark += positive_variables_constraint(genAmount, investedNum)  
    totalFark += nuclear_constraint(investedNum) 

    totalFark += demand_constraint(genAmount, demands)
    totalFark += capacity_constraint(genAmount, capacities)
    totalFark += peak_demand_constraint(peakDemand, capacities)
    totalFark += construction_limit_constraint(investedNum, constructionLimit)
    
    print("p_n_v = " , positive_variables_constraint(genAmount, investedNum))
    print("nuclear_constraint = " , nuclear_constraint(investedNum) )
    print("demand_constraint = " , demand_constraint(genAmount, demands))
    print("capacity_constraint = " , capacity_constraint(genAmount, capacities))
    print("peak_demand_constraint = " , peak_demand_constraint(peakDemand, capacities))
    print("construction_limit_constraint = " , construction_limit_constraint(investedNum, constructionLimit))

# mwh dogru
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
def capacity_constraint(birey, capacities):  # whatsapp
    fark = 0.0
    for year in range(16):
        for unitType in range(11):
            if birey[year][unitType] > capacities[year][unitType]:
                    fark = birey[year][unitType] - capacities[year][unitType]

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



def nuclear_constraint(investedNum):
    fark = 0.0

    for year in range(11):
        if investedNum[year][5] != 0:  # 5 for nuclear
            fark = investedNum[year][5]
    
    return fark


def positive_variables_constraint(genAmount, investedNum):
    fark = 0.0

    for year in range(16):
        for unitType in range(11):
            if genAmount[year][unitType] < 0 or investedNum[year][unitType] < 0:
                fark += 1

    return fark

