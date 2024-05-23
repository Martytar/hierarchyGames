import sympy as sp
import numpy as np


class f_v: #функция - оптимальное управление завода-производителя

    def __init__(self, funs, u):
        self.funs = funs
        self.u = u

    def f(self, spot):
        u = self.u

        res = sp.Matrix(np.zeros(len(u)))
        for i in self.funs:
            isSuitable = True
            for j in i.rest:
                cRectVal = j
                for k in range(0, len(u)):
                     cRectVal = cRectVal.subs(u[k], spot[k])
                if cRectVal > 0.0:
                    isSuitable = False
                    break
            if isSuitable:
                res = i.exp
                for k in range(0, len(u)):
                    res = res.subs(u[k], spot[k])
                break

        return res

class f_f: #функция прибыли распределителя при оптимальности производственных центров

    def __init__(self, funcSet, coefSet, u):
        self.funkSet = funcSet
        self.coefSet = coefSet
        self.u = u

    def f(self, spot):
        res = 0.0
        displace = 0
        for i in range(0, len(self.funkSet)):
            res += np.matmul(self.coefSet[i], self.funkSet[i].f(spot[displace:]))
            displace += len(self.funkSet[i].u)
        return res