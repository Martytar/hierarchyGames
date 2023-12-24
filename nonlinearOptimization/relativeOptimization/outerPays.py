from nonlinearOptimization.absoluteOptimization.highDimOptimization import highDimOptimizaCor
from nonlinearOptimization.absoluteOptimization.highDimOptimization import norm2


def outerPays(f, h, r, x, e):

    cR = r
    cX = x
    pX = x

    def cF(x, r=cR):
        return f.f(x) + cR * h(x)

    iters = 1

    #безусловная оптимизация с учетом штрафной функции
    cX = highDimOptimizaCor(cF, x, [1.0 for i in range(0, len(x))], e)
    cR *= 10

    #повторная безусловная оптимизация с условием остановки
    #алгоритма и преобразованием коэффициента штрафной функции
    while (abs(h(cX)) > e or norm2(cX, pX) > e) and iters <= 100:
        pX = cX
        cX = highDimOptimizaCor(cF, cX, [1.0 for i in range(0, len(x))], e)
        cR *= 10
        iters+=1

    return cX


