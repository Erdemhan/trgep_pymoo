import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer
import trgep_toolbox as trgeptb
import copy



class TrgepProblem(ElementwiseProblem):
    # Penalty Factor
    PF =5.0
    # Penalty Generation Exponent
    PGE = 1.4
    capPGE = PGE
    pdemPGE = PGE
    
    genCtr = 0 

    def __init__(self, **kwargs):

        data = trgeptb.data

        variables = dict()

        for k in range(0, 176):
            variables[f"x{k:02}"] = Real(bounds=(0.0, 146458237*2.2))

        for k in range(176, 352):
            variables[f"x{k:02}"] = Integer(bounds=(0, data['climit'][k%11]))

        super().__init__(vars=variables, n_obj=2 ,n_ieq_constr=5 , **kwargs)


    def _penalty(self,x):
        nucp,capp,demp,pdemp,climp,capConstraintDict,nuclearInd = trgeptb.const_check(x,trgeptb.data)

        return nucp,capp,demp,pdemp,climp
    
    def _penalty_manuel(self,x,f1,f2=0):
        nucp,capp,demp,pdemp,climp,capConstraintDict,nuclearInd = trgeptb.const_check(x,trgeptb.data)
        o1 = copy.deepcopy(f1)
        o2 = copy.deepcopy(f2)
        if nucp>0:
            o1 += ((self.PF*nucp))*(((self.genCtr)+1)**self.PGE)
            o2 += ((self.PF*nucp))*(((self.genCtr)+1)**self.PGE)
        if capp>0:
            o1 += (self.PF*capp)*(((self.genCtr)+1)**self.capPGE)
            o2 += (self.PF*capp)*(((self.genCtr)+1)**self.capPGE)
        if demp>0:
            o1 += ((self.PF*demp))*(((self.genCtr)+1)**self.PGE)
            o2 += ((self.PF*demp))*(((self.genCtr)+1)**self.PGE)  
        if pdemp>0:
            o1 += ((self.PF*pdemp))*(((self.genCtr)+1)**self.pdemPGE)
            o2 += ((self.PF*pdemp))*(((self.genCtr)+1)**self.pdemPGE)
        if nucp>0:
            o1 += ((self.PF*climp))*(((self.genCtr)+1)**self.PGE)
            o2 += ((self.PF*climp))*(((self.genCtr)+1)**self.PGE)
        
        self.genCtr += 1

        return o1,o2,nucp,capp,demp,pdemp,climp

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

        nucp,capp,demp,pdemp,climp = self._penalty(x)
        #nucp,capp,demp,pdemp,climp,capConstraintDict,nuclearInd = trgeptb.const_check(x,trgeptb.data)
        out["F"] = np.column_stack([f1,f2])
        out["G"] = np.column_stack([nucp,capp,demp,pdemp,climp])
        # out["F"] = f1

