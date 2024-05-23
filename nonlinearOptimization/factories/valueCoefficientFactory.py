import numpy.random as random


class valueCoefficientFactory():
    # число видов продукции (в рамках иерархической игры) по умолчанию
    k = 1
    # максимальное значение цены
    limit = 1

    def getLimitedValues(self):
        vals = [random.random() * self.limit for i in range(0, self.k)]
        return vals

    def getSpecifiedValues(self, limits):
        vals = [random.random() * limits[i] for i in range(0, len(limits))]
        return vals

    def setParams(self, k, limit):
        self.k = k
        self.limit = limit


