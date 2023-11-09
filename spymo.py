import trgepProblem
from pymoo.algorithms.moo.nsga2 import NSGA2 
from pymoo.core.mixed import MixedVariableMating,MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
import trgep_toolbox as trgeptb
import matplotlib.pyplot as plt
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
import numpy as np
from pymoo.visualization.scatter import Scatter
import pandas as pd
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.core.variable import Real, Integer
from pymoo.operators.crossover.expx import ExponentialCrossover
from pymoo.operators.crossover.sbx import SimulatedBinaryCrossover
from pymoo.operators.crossover.pntx import PointCrossover
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.constraints.adaptive import AdaptiveConstraintHandling
import pandas as pd
from pymoo.algorithms.moo.nsga2 import binary_tournament
from pymoo.problems import get_problem
from pymoo.core.callback import Callback
from pymoo.core.mixed import MixedVariableGA
import random as rand

# PARAMETERS
NPOP = 250 #200-300, 300-500, 500-1500  200(pop)-150(offs)
NGEN = 500

# 500 - 250
SEED = 1

# DEFINITIONS
# PROBLEM

problem = trgepProblem.TrgepProblem(NPOP=NPOP)
#problem = get_problem("carside")
'''
ZDT4 	10 2 0
ZDT5 	80 2 0
MW5 	15 2 3
Carside 7 3 10
'''

crossovert = {
                Real: PointCrossover(n_points=5),
                Integer: SimulatedBinaryCrossover(vtype=float,repair=RoundingRepair()),
            }
mutationt = {
                Real: PolynomialMutation(prob=0.15,eta=9999),
                Integer: PolynomialMutation(prob=0.15,eta=0.1,vtype=float, repair=RoundingRepair()),
            }


# INITIALIZE POPULATION
#in_pop_cost_20
#in_pop_em_20
#initial_pop_40
#best80_2f
def init_population():
    pop = Population.new("X", trgeptb.read_population('initpop_2020 - original.xlsx'))  
    # 10 em-opt best.xlsx 
    # 10 em-opt 10 cost-opt initpop_2020.xlsx
    Evaluator().eval(problem, pop)
    return pop


# ALGORITHM
algorithm_old = NSGA2(
                  pop_size=NPOP,
                  n_offsprings=200,
                  sampling=init_population(), # init_population(), MixedVariableSampling()
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination(),
                                             repair=trgeptb.repair()
                                             ),
                  #survival=binary_tournament(),                           
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

algorithmMixed = MixedVariableGA(
    pop_size=NPOP,
    #n_offsprings=100,
    sampling=MixedVariableSampling(), #MixedVariableSampling(), init_population()
    mating=MixedVariableMating( eliminate_duplicates=MixedVariableDuplicateElimination(),
                                repair=trgeptb.repair(),
                                #crossover=crossovert,
                                #mutation=mutationt,
                                #selection=selectiont,
                              ),
    #sampling= init_population(),
                                )


class MyCallback(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.genC = trgepProblem.TrgepProblem.genCtr 

    def notify(self, algorithm):
        #self.data["best"].append(algorithm.pop.get("F").min())
        trgepProblem.TrgepProblem.genCtr += 1

class convergenceCallback(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.data["best"] = []

    def notify(self, algorithm):
        self.data["best"].append(algorithm.pop.get("F").min())

#algorithm = NSGA2()

# RUN
""" 
res = minimize(problem,
               #algorithm_old,
               algorithmMixed,
               ('n_gen', NGEN),
               callback = convergenceCallback(),
               seed = SEED,
               verbose=True)
 """
#print(SEED)
#trgeptb.pop_to_excel(res.pop)

seedList = []
for m in range(5):
    SEED = rand.randint(0, 200)
    SEED = 54
    # 135
    seedList.append(SEED)
    #print(SEED)

    res = minimize(problem,
               algorithm_old,
               #algorithmMixed,
               ('n_gen', NGEN),
               callback = convergenceCallback(),
               seed = SEED,
               verbose=True)
    trgeptb.show_result(problem,res)

with open('seed_list.txt', 'a') as f:
    for line in seedList:
        f.write(f"{line}\n")

