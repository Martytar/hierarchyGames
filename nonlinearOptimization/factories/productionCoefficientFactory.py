import numpy.random as random


class productionCoefficientFactory():
    # число видов продукции (в рамках иерархической игры) по умолчанию
    k = 1

    #число видов ресурсов
    n = 1

    # максимальное значение производственного коэффициента
    limit = 1

    def getLimitedValues(self):
        vals = [[random.random() * self.limit for i in range(0, self.k)] for j in range(0, self.n)]
        return vals

    def getSpecifiedValues(self, limits):
        vals = [[random.random() * limits[j][i] for i in range(0, len(limits[0]))] for j in range(0, len(limits))]
        return vals

    def setParams(self, k, n, limit):
        self.k = k
        self.n = n
        self.limit = limit
