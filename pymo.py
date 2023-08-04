import numpy as np
import trgepProblem



problem = trgepProblem.TrgepProblem()
from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2, RankAndCrowdingSurvival
from pymoo.core.mixed import MixedVariableMating, MixedVariableGA, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
from pymoo.constraints.as_penalty import ConstraintsAsPenalty
import trgep_toolbox as trgeptb
import timeit
import random

algorithm = NSGA2(pop_size=40,
                  sampling=MixedVariableSampling(),
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

start = timeit.default_timer()
best = 99999999999999999
bestSeed = 0
ctr = 0


while ctr < 300:
    seedR = random.randint(0,999)
    res = minimize(problem,
               algorithm,
               ('n_gen', 250),
               seed=seedR,
               verbose=False)
    print("Best solution found: \nF = %s , seed =  F = %s" % (res.F,seedR))
    if res.F < best:
        best = res.F
        bestSeed = seedR
    ctr +=1

stop = timeit.default_timer()
print('Time: ', stop - start)

x = np.array([res.X[f"x{k:02}"] for k in range(0, 352)])
print(trgeptb.const_check_debug(x,trgeptb.data))
print("Best solution found ever : \nF = %s  Seed = %s " % (best,bestSeed))


