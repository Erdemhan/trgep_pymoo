import numpy as np
import random
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer
import trgep_toolbox as trgeptb
import copy



class TrgepProblem(ElementwiseProblem):
    # Penalty Factor
    PF =100.0
    # Penalty Generation Exponent
    PGE = 1.1
    capPGE = PGE*1.2
    pdemPGE = PGE
    
    genCtr = 0 

    def __init__(self, **kwargs):

        data = trgeptb.data

        variables = dict()

        for k in range(0, 176):
            variables[f"x{k:02}"] = Real(bounds=(0.0, 146458237*2.2))

        for k in range(176, 352):
            variables[f"x{k:02}"] = Integer(bounds=(0, data['climit'][k%11]))

        super().__init__(vars=variables, n_obj=2 , **kwargs)




    def _evaluate(self, x, out, *args, **kwargs):
        x = np.array([x[f"x{k:02}"] for k in range(0, 352)])
        
        data = trgeptb.data
        #out["F"] = [f1, f2]
        costProd, costInvest, costMnt , emission = 0.0, 0.0, 0.0, 0.0
        genAmount = trgeptb.reshape_to_matrix(x,True)
        investResNumber = trgeptb.reshape_to_matrix(x,False)
        totalUnitsMW = copy.deepcopy(data['exists'])
        totalUnits =  [0.0 for element in range(11)]
        
        for year in range(16):  # 16
            for unitType in range(11):  # 11
                emission += genAmount[year][unitType] * data['emission'][year][unitType]
                costProd += genAmount[year][unitType] * data['gencost'][year][unitType]
                
                costInvest += investResNumber[year][unitType] *  data['invcost'][year][unitType]  *  data['gencap'][unitType]

                totalUnits[unitType] += investResNumber[year][unitType]
                totalUnitsMW[unitType] += totalUnits[unitType] * data['gencap'][unitType]
            
                #MW başına olacak şekilde değişecek
                costMnt += totalUnitsMW[unitType]  *  data['omcost'][year][unitType]
        
        f1 = costMnt + costInvest + costProd

        f2 = emission

        nucp,capp,demp,pdemp,climp = trgeptb.const_check(x,data)

        if nucp>0:
            f1 += ((self.PF*nucp))*(((self.genCtr//40)+1)**self.PGE)
            f2 += ((self.PF*nucp))*(((self.genCtr//40)+1)**self.PGE)
        if capp>0:
            f1 += (self.PF*capp)*(((self.genCtr//40)+1)**self.capPGE)
            f2 += (self.PF*capp)*(((self.genCtr//40)+1)**self.capPGE)
        if demp>0:
            f1 += ((self.PF*demp))*(((self.genCtr//40)+1)**self.PGE)
            f2 += ((self.PF*demp))*(((self.genCtr//40)+1)**self.PGE)  
        if pdemp>0:
            f1 += ((self.PF*pdemp))*(((self.genCtr//40)+1)**self.pdemPGE)
            f2 += ((self.PF*pdemp))*(((self.genCtr//40)+1)**self.pdemPGE)
        if nucp>0:
            f1 += ((self.PF*climp))*(((self.genCtr//40)+1)**self.PGE)
            f2 += ((self.PF*climp))*(((self.genCtr//40)+1)**self.PGE)

        self.genCtr += 1

        
        out["F"] = np.column_stack([f1,f2])