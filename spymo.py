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
from pymoo.algorithms.moo.nsga2 import binary_tournament
from pymoo.problems import get_problem
from pymoo.core.callback import Callback

# PARAMETERS
NPOP = 100
NGEN = 200
SEED = 1

# DEFINITIONS
# PROBLEM

problem = trgepProblem.TrgepProblem()
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
algorithm_old = NSGA2(pop_size=NPOP,
                  sampling=MixedVariableSampling(), # init_population(), MixedVariableSampling()
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination(),
                                             #repair=trgeptb.repair()
                                             ),
                  #survival=binary_tournament(),                           
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

class MyCallback(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.genC = trgepProblem.TrgepProblem.genCtr 

    def notify(self, algorithm):
        #self.data["best"].append(algorithm.pop.get("F").min())
        trgepProblem.TrgepProblem.genCtr += 1

#algorithm = NSGA2()

# RUN
res = minimize(problem,
               algorithm_old,
               ('n_gen', NGEN),
               callback = MyCallback(),
               seed = SEED,
               verbose=True)

print(SEED)
#trgeptb.pop_to_excel(res.pop)
trgeptb.show_result(problem,res)

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()
