import sympy as sp
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

import optimiza
from nonlinearOptimization.functions.functions import f_v, f_f
from nonlinearOptimization.relativeOptimization.outerPays import outerPays
import optimiza
from nonlinearOptimization.factories.resourseValueFactory import resourseValueFactory
from nonlinearOptimization.factories.valueCoefficientFactory import valueCoefficientFactory
from nonlinearOptimization.factories.productionCoefficientFactory import productionCoefficientFactory
from nonlinearOptimization.absoluteOptimization.fire_optimization import fire_optimization

#matplotlib.use('TKAgg')

k = 10
n1 = 2
n2 = 2

rFact = resourseValueFactory()
rFact.setParams(k, 1000)

acFact = valueCoefficientFactory()

AFact = productionCoefficientFactory()

b = rFact.getLimitedValues() #максимальные поставки ресурсов от распределителя

acFact.setParams(n1, 500)
a1 = acFact.getLimitedValues()  # ценовые ко-ты завода-распределителя для 1 завода
c1 = acFact.getLimitedValues()  # ценовые к-ты целевой ф-и

AFact.setParams(n1, k, 50)
A1 = AFact.getLimitedValues()  # производственная матрица (пусть домножение будет слева, это удобнее)
rest1 = np.array([])  # базовые ограничения (их нет)

u1 = np.array([])  # переменные, которые мы будем варьировать для первого завода
for i in range(1, k+1):
    u1 = np.append(u1, [sp.Symbol(f'u_{i}')])

funs1 = optimiza.findOptimalFunction(c1, A1, u1)  # оптимальные управления 1 завода-производителя

f1 = f_v(funs1, u1)  # функция-оптимальное управление завода-производителя

acFact.setParams(n2, 500)
a2 = acFact.getLimitedValues() # ценовые ко-ты завода-распределителя для 2 завода
c2 = acFact.getLimitedValues() # ценовые к-ты целевой ф-и

AFact.setParams(n2, k, 50)
A2 = AFact.getLimitedValues() # производственная матрица (пусть домножение будет слева, это удобнее)
rest2 = np.array([])  # базовые ограничения (их нет)

u2 = np.array([])  # переменные, которые мы будем варьировать для второго завода
for i in range(k+1, 2*k+1):
    u2 = np.append(u2, [sp.Symbol(f'u_{i}')])

funs2 = optimiza.findOptimalFunction(c2, A2, u2)  # оптимальные управления 2 завода-производителя

f2 = f_v(funs2, u2)  # функция-оптимальное управление завода-производителя

f = f_f([f1, f2], [a1, a2], np.append(u1, u2)) #функция прибыли координирующего центра

resx = fire_optimization(f.f, b, 10000000, 1, [0 for i in range(0, 2*k)])

print(resx, f.f(resx))


#for i in funs2:
#    i.print()


#попытка во внешние штрафы( условная оптимизация с покоординатным спуском, так как оптимизируемая функция не является гладкой.
# def h(x):  # функция штрафов
#     res = 0.0
#     for i in x:
#         res += math.pow(max(0.0, -1 * i), 2)
#     res += math.pow(max(0.0, x[0] - 50), 2)
#     res += math.pow(max(0.0, x[1] - 50), 2)
#
#     res += math.pow(x[0] + x[1] - 50, 2)
#
#     return res
#
# maxSpot = outerPays(f, h, 1.0, [0, 50], 10**(-5)) #ищет минимум, а не максимум!!!!
#
# print(maxSpot)
# print(f.f(maxSpot))
# #////////////////////////////////////////////////Строим график для простейшего случая
# fig = plt.figure()
# ax = fig.gca(projection='3d')
#
# x = np.linspace(0, 50, 100)
# xv, yv = np.meshgrid(x, x, indexing='ij')
#
# z = np.zeros((100, 100))
# for i in range(0, 100):
#     for j in range(0, 100):
#         cx = xv[i, j]
#         cy = yv[i, j]
#         z[i, j] = f.f([cx, cy])
#
#
# ax.plot_surface(xv, yv, z, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)
#
# ax.legend()
# ax.set_xlabel("u1")
# ax.set_ylabel("u2")
# ax.set_zlabel("f")
#
#
# plt.show()