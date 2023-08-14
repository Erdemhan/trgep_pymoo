import trgepProblem
from pymoo.algorithms.moo.nsga2 import NSGA2 
from pymoo.core.mixed import MixedVariableMating,MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.optimize import minimize
import trgep_toolbox as trgeptb
import timeit
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
import numpy as np
from pymoo.visualization.scatter import Scatter
import pandas as pd
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival
from pymoo.core.mixed import MixedVariableGA
from pymoo.core.problem import Problem
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.util import plotting

'''
def binary_tournament(pop, P, **kwargs):
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape

    # the result this function returns
    import numpy as np
    S = np.full(n_tournaments, -1, dtype=np.int)

    # now do all the tournaments
    for i in range(n_tournaments):
        best = 0
        for ind in P[i]:
            if pop[ind].F[0] < pop[best].F[0] :
                if pop[ind].F[1]  < pop[best].F[1]:
                    best = ind
                    break
                elif pop[best].F[0] - pop[ind].F[0]  > pop[ind].F[1]  - pop[best].F[1]:
                    best = ind
                    break
            elif pop[ind].F[1]  < pop[best].F[1]:
                if pop[ind].F[0]  < pop[best].F[0] :
                    best = ind
                    break
                elif pop[best].F[1] - pop[ind].F[1]  > pop[ind].F[0] - pop[best].F[0] :
                    best = ind
                    break
        S[i] = best
    return S

# PARAMETERS
NPOP = 120
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
                  survival=RankAndCrowdingSurvival(),
                  sampling=pop , # pop, MixedVariableSampling()
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination(),
                                             repair=trgeptb.repair()),
                  eliminate_duplicates=MixedVariableDuplicateElimination()
                  #output=CustomOutput(),
                  #callback=CustomCallback()
                  )

# RUN
start = timeit.default_timer()
res = minimize(problem,
               algorithm,
               ('n_gen', NGEN),
               seed = SEED,
               verbose=True)
stop = timeit.default_timer()

# PRINT RESULT
print('Time: ', stop - start)
print("Best solution found ever : \nF = %s " % (res.F))
x = np.array([res.X[f"x{k:02}"] for k in range(0, 352)])
print(trgeptb.const_check_debug(x,trgeptb.data))


for t in range(len(res.F)):
    print(str(res.F[t][0])[:3] , "e" , len(str(int(res.F[t][0])))-3 , "          " , str(res.F[t][1])[:3] , "e" , len(str(int(res.F[t][1])))-3)
    x = np.array([res.X[t][f"x{k:02}"] for k in range(0, 352)])
    trgeptb.const_check_debug(x,trgeptb.data)

print("Time: " , stop-start)

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()
'''
problem = trgepProblem.TrgepProblem()
sampling = FloatRandomSampling()
X = sampling(problem, 1).get("X")
plotting.plot(X[0], no_fill=True)