import trgepProblem
from pymoo.algorithms.moo.nsga2 import NSGA2 
from pymoo.core.mixed import MixedVariableMating,MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
import trgep_toolbox as trgeptb
import timeit
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
import numpy as np
from pymoo.visualization.scatter import Scatter
import pandas as pd

# PARAMETERS
NPOP = 80
NGEN = 220
SEED = 1


# DEFINITIONS
# PROBLEM
problem = trgepProblem.TrgepProblem()

# INITIALIZE POPULATION
pop = Population.new("X", trgeptb.read_population())
Evaluator().eval(problem, pop)

# ALGORITHM
algorithm = NSGA2(pop_size=NPOP,
                  sampling=pop,
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                  eliminate_duplicates=MixedVariableDuplicateElimination()
                  )


# RUN

start = timeit.default_timer()
res = minimize(problem,
               algorithm,
               ('n_gen', NGEN),
               seed = SEED,
               verbose=True)
stop = timeit.default_timer()


'''
# PRINT RESULT
print('Time: ', stop - start)
print("Best solution found ever : \nF = %s " % (res.F))
x = np.array([res.X[f"x{k:02}"] for k in range(0, 352)])
print(trgeptb.const_check_debug(x,trgeptb.data))
'''

for t in range(len(res.F)):
    print(str(res.F[t][0])[:3] , "e" , len(str(int(res.F[t][0])))-3 , "          " , str(res.F[t][1])[:3] , "e" , len(str(int(res.F[t][1])))-3)
    x = np.array([res.X[t][f"x{k:02}"] for k in range(0, 352)])
    trgeptb.const_check_debug(x,trgeptb.data)


plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()
