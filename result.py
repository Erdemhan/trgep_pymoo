import trgep_toolbox as trgeptb
import numpy as np
from pymoo.visualization.scatter import Scatter
import pandas as pd


# PRINT RESULT
def print_result(problem,res):
    print('Time: ', res.exec_time)
    if not problem.n_obj == 1:
        #print_multi(res)
        draw(problem,res)
    else:
        print_one(res)
    
def print_one(res):
    print("Best solution found ever : \nF = %s " % (res.F))
    x = np.array([res.X[f"x{k:02}"] for k in range(0, 352)])
    print(trgeptb.const_check_debug(x,trgeptb.data))
    x = trgeptb.reshape_to_matrix(x,is_generation=False)
    df = pd.DataFrame(x)
    df.to_excel('best.xlsx', index=False, header=False)

def print_multi(res):
    for t in range(len(res.F)):
        print(str(res.F[t][0])[:3] , "e" , len(str(int(res.F[t][0])))-3 , "          " , str(res.F[t][1])[:3] , "e" , len(str(int(res.F[t][1])))-3)
        x = np.array([res.X[t][f"x{k:02}"] for k in range(0, 352)])
        trgeptb.const_check_debug(x,trgeptb.data)

def divide_feasible(res):   
    f_pop_res = []
    if_pop_res = []
    for ind in res.pop:
        nucp,capp,demp,pdemp,climp,capConstraintDict,nuclearInd = trgeptb.const_check(np.array(list(ind.X.values())),trgeptb.data)
        total = nucp+capp+demp+pdemp+climp
        if total == 0:
            f_pop_res.append(ind.F)
        else:
            if_pop_res.append(ind.F)
    return np.array(f_pop_res),np.array(if_pop_res)

def draw(problem,res):
    f_pop_res,if_pop_res = divide_feasible(res)
    plot = Scatter()
    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    if len(f_pop_res) > 0:
        plot.add(f_pop_res, facecolor="none", edgecolor="blue")
    if len(if_pop_res) > 0:
        plot.add(if_pop_res, facecolor="none", edgecolor="red")
    plot.show()

