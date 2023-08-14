from pymoo.core.repair import Repair
import trgep_toolbox as trgeptb
import numpy as np

class TrgepRepair(Repair): # capacity repair
    def _do(self, problem, X, **kwargs):
        key = 0
        for dictItems in X:
            dictValues = np.array(list(dictItems.values()))
            consts = trgeptb.const_check(dictValues, trgeptb.data)
            capConstaintDict,nuclearInd = consts[5],consts[6] 

            for vio in capConstaintDict.keys():
                dictItems[f'{vio}'] = dictItems[f'{vio}'] - capConstaintDict[f'{vio}']
            for vio in nuclearInd.keys():
                dictItems[f'{vio}'] = 0
                

            X[key] = dictItems
            key += 1

        return X
