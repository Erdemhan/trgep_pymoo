import trgepProblem
from pymoo.algorithms.moo.nsga2 import NSGA2 
from pymoo.core.mixed import MixedVariableMating,MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
import trgep_toolbox as trgeptb
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
import numpy as np
from pymoo.visualization.scatter import Scatter
import pandas as pd
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.core.variable import Real, Integer
from pymoo.operators.crossover.expx import ExponentialCrossover
from pymoo.operators.crossover.sbx import SimulatedBinaryCrossover
from pymoo.operators.crossover.pntx import PointCrossover
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.constraints.adaptive import AdaptiveConstraintHandling
import pandas as pd

# PARAMETERS
NPOP = 80
NGEN = 220
SEED = 1

# DEFINITIONS
# PROBLEM

problem = trgepProblem.TrgepProblem()
crossovert = {
                Real: PointCrossover(n_points=2),
                Integer: SimulatedBinaryCrossover(vtype=float,repair=RoundingRepair()),
            }
mutationt = {
                Real: PolynomialMutation(prob=0.02,eta=9999),
                Integer: PolynomialMutation(prob=0.02,eta=0.1,vtype=float, repair=RoundingRepair()),
            }


# INITIALIZE POPULATION
#in_pop_cost_20
#in_pop_em_20
#initial_pop_40
#best80_2f
def init_population():
    pop = Population.new("X", trgeptb.read_population('initial_pop_40.xlsx'))
    Evaluator().eval(problem, pop)
    return pop


# ALGORITHM
algorithm = NSGA2(pop_size=NPOP,
                  sampling=init_population(), # init_population(), MixedVariableSampling()
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination(),
                                             repair=trgeptb.repair()
                                             ),
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

# RUN
res = minimize(problem, #AdaptiveConstraintHandling(problem)
               algorithm,
               ('n_gen', NGEN),
               seed = SEED,
               verbose=True)

print(SEED)
#trgeptb.pop_to_excel(res.pop)
trgeptb.show_result(problem,res)
