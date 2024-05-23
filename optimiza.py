import numpy as np
import sympy as sp
import nonlinearOptimization.functions.functions as funcs

#тут методы для решения задачи параметрического симплекса, т. е. нахождение оптимальных переменных векторов в зависимости от параметра
def findOptimalFunction(c, A, u):

    rest = np.array([])
    tab = makeTable(c, A, u)
    n = len(A[0])
    m = len(A)
    basis = [n+i for i in range(1, m+1)]

    return solveTable(tab, rest, basis)



#симплекс-метод
def solveTable(table, restricts, basis, pair = []): #параметры: 1)текущая симплексная таблица, 2)текущие ограничения, 3)индексы базисных переменных

    tab = np.copy(table)
    rest = np.copy(restricts)
    base = np.copy(basis)

    if pair == []:
        #выбираем ведущий столбец
        c = 1
        for i in range(1, len(tab[0])):
            if tab[-1, i] < tab[-1, c]:
                c = i
        if tab[-1, c] >= 0:
            return np.array([makeFunPart(tab, rest, basis)]) #если таблица оптимальна, то сразу создаем функцию и возвращаем

        #находим множество строк, подозрительных на ведущую строку
        potentRow = np.array([])
        for i in range(0, len(tab)):
            if tab[i, c] > 0:
                potentRow = np.append(potentRow, i)

        foundFuns = np.array([])
        for i in potentRow:
            addictRest = np.array([])
            for j in potentRow:
                if(i != j):
                    addictRest = np.append(addictRest, tab[int(i), 0]/tab[int(i), c] - tab[int(j), 0]/tab[int(j), c])
            foundFuns = np.append(foundFuns, solveTable(tab, np.append(restricts, addictRest), base, [i, c]))

        return foundFuns

    else:
        #если заданы ведущие строка и столбец, преобразуем таблицу и заново запустим метод рекурсивно
        tab[int(pair[0]), :] /= tab[int(pair[0]), int(pair[1])]
        for i in range(0, len(tab)):
            if i != pair[0]:
                tab[i, :] -= tab[int(pair[0]), :]*tab[i, int(pair[1])]

        base[int(pair[0])] = pair[1]
        return solveTable(tab, restricts, base)

def makeFunPart(tab, rest, basis): #задание 1 функции управления производителя на некоторой области. tab - симплекс-таблица, rest - текущее ограничение(ия), basis
    # - индексы базисных переменных в симплекс-таблице

    n = len(tab[0, :]) - len(tab)
    f = sp.Matrix(np.zeros(n))
    for i in range(0, len(basis)):
        if basis[i] <= n:
            f[basis[i]-1] = tab[i, 0]

    return funcs.funPart(f, rest)

def makeTable(c, A, u): #задание симплексной таблицы

    c = np.array(c)

    zer = np.diag(np.diag(np.ones((len(A), len(A)))))

    z = np.append(np.append([0], [-1*c]), np.zeros(len(A)))

    tab = np.row_stack((np.column_stack((u, A, zer)), z))

    return tab
