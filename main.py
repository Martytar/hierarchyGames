import sympy as sp
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

import optimiza
from nonlinearOptimization.Function.function import f_v, f_f
from nonlinearOptimization.relativeOptimization.outerPays import outerPays
import structs
import optimiza

matplotlib.use('TKAgg')

a1 = -1*np.array([10, 20, 5])  # ценовые ко-ты завода-распределителя для 1 завода
c1 = np.array([4.0, 3.0, 5.0])  # ценовые к-ты целевой ф-и
A1 = np.array(
    [[5.0, 6.0, 2.0]])  # производственная матрица (пусть домножение будет слева, это удобнее)
rest1 = np.array([])  # базовые ограничения (их нет)

u1 = np.array([])  # переменные, которые мы будем варьировать для первого завода
for i in range(1, 2):
    u1 = np.append(u1, [sp.Symbol(f'u_{i}')])

funs1 = optimiza.findOptimalFunction(c1, A1, u1)  # оптимальные управления 1 завода-производителя

f1 = f_v(funs1, u1)  # функция-оптимальное управление завода-производителя

a2 = -1*np.array([10, 15])  # ценовые ко-ты завода-распределителя для 2 завода
c2 = np.array([3.0, 70.0])  # ценовые к-ты целевой ф-и
A2 = np.array(
    [[6.0, 1.0]])  # производственная матрица (пусть домножение будет слева, это удобнее)
rest2 = np.array([])  # базовые ограничения (их нет)

u2 = np.array([])  # переменные, которые мы будем варьировать для второго завода
for i in range(2, 3):
    u2 = np.append(u2, [sp.Symbol(f'u_{i}')])

funs2 = optimiza.findOptimalFunction(c2, A2, u2)  # оптимальные управления 2 завода-производителя

f2 = f_v(funs2, u2)  # функция-оптимальное управление завода-производителя

f = f_f([f1, f2], [a1, a2], np.append(u1, u2)) #функция прибыли координирующего центра

def h(x):  # функция штрафов
    res = 0.0
    for i in x:
        res += math.pow(max(0.0, -1 * i), 2)
    res += math.pow(max(0.0, x[0] - 50), 2)
    res += math.pow(max(0.0, x[1] - 50), 2)

    res += math.pow(x[0] + x[1] - 50, 2)

    return res

#maxSpot = outerPays(f, h, 1.0, [0, 0], 10**(-2))

#print(maxSpot)
#print(-1*f.f(maxSpot))

#////////////////////////////////////////////////Строим график для простейшего случая
fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.linspace(0, 50, 100)
xv, yv = np.meshgrid(x, x, indexing='ij')

z = np.zeros((100, 100))
for i in range(0, 100):
    for j in range(0, 100):
        cx = xv[i, j]
        cy = yv[i, j]
        z[i, j] = -1*f.f([cx, cy])


ax.plot_surface(xv, yv, z, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)

ax.legend()
ax.set_xlabel("u1")
ax.set_ylabel("u2")
ax.set_zlabel("f")


plt.show()