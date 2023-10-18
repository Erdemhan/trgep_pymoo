import pandas as pd
import openpyxl


df = pd.read_excel('investment_gen_data.xlsx',engine='openpyxl', sheet_name=None)
df_pareto = pd.read_excel('pareto.xlsx',engine='openpyxl', sheet_name=None)

def read_gencost():
    return df['gencost'].values.tolist()

def read_invcost():
    return df['invcost'].values.tolist()

def read_omcost():
    return df['omcost'].values.tolist()

def read_emission():
    return df['emission'].values.tolist()


def read_capfactor():
    return df['capfactor'].values.tolist()[0]

def read_demand():
    return df['demand'].values.tolist()[0]

def read_gencap():
    return df['xmax'].values.tolist()[0]

def read_climit():
    return df['climit'].values.tolist()[0]

def read_exists():
    return df['exists'].values.tolist()[0]

def read_hours():
    return df['hours'].values.tolist()[0]

def read_peaks():
    return df['peak'].values.tolist()[0]


def initial_cap():
    capacities = read_gencap()[:11]
    capfactors = read_capfactor()
    initial_cap = []

    for i in range(len(capacities)):
        initial_cap.append(capacities[i] * capfactors[i])
    
    return initial_cap



def read():
    return {'gencap':read_gencap(),'initial_cap':initial_cap(),'gencost':read_gencost(),'invcost':read_invcost(),'omcost':read_omcost(),'demand':read_demand(),'climit':read_climit(),'exists':read_exists(),'peaks':read_peaks(),'hours':read_hours(),'emission':read_emission()}


def read_pareto():
    return df_pareto['Sayfa1'].values.tolist()