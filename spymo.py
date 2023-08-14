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

# PARAMETERS
NPOP = 40
NGEN = 120
SEED = 1

# DEFINITIONS
# PROBLEM

problem = trgepProblem.TrgepProblem()
crossovert = {
                Real: PointCrossover(n_points=5),
                Integer: PointCrossover(n_points=5),
            }
mutationt = {
                Real: PolynomialMutation(prob=0.02,eta=9999),
                Integer: PolynomialMutation(prob=0.02,eta=0.1,vtype=float, repair=RoundingRepair()),
            }


# INITIALIZE POPULATION
def init_population():
    pop = Population.new("X", trgeptb.read_population())
    Evaluator().eval(problem, pop)
    return pop


# ALGORITHM
algorithm = NSGA2(pop_size=NPOP,
                  sampling=init_population() , # init_population(), MixedVariableSampling()
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination(),
                                             repair=trgeptb.repair(),
                                             crossover=crossovert,
                                             mutation=mutationt
                                             ),
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

# RUN
res = minimize(problem, #AdaptiveConstraintHandling(problem)
               algorithm,
               ('n_gen', NGEN),
               seed = SEED,
               verbose=True)


trgeptb.show_result(problem,res)