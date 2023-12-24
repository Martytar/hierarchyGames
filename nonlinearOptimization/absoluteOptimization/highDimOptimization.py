import math

def norm2(arr1, arr2):
    s = 0.0
    for i in range(len(arr1)):
        s += (arr1[i] - arr2[i]) ** 2
    return math.sqrt(s)

def hex(v):
    h = hex(v)
    splitH = h.split('.')
    if len(h) > 9:
        return splitH[0] + "." + splitH[1][:4] + 'p' + h.split('p')[-1]
    return h

def format(v):
    s = str(v)
    if len(s) <= 10:
        sl = len(s)
        for i in range(10-sl):
            s += " "
    else:
        s = s[:10]
    return s


def highDimOptimizaCor(f, gSpot, gDisplacement, epsilon):
    spot = gSpot[:]
    displacement = gDisplacement[:]
    newSpot = spot[:]

    cf = f(spot)

    def isAwesomeDisplacement():
        for i in displacement:
            if abs(i) >= epsilon:
                return False
        return True

    while not isAwesomeDisplacement():
        i = 0
        dim = 0
        iters = 0
        while i < len(spot) and iters < 5000: #тут добавлен итератор для ограничения времени работы алгоритма
            iters += 1
            cSpot = newSpot[:]
            if dim != -1:
                cSpot[i] += displacement[i]
                rf = f(cSpot)
                if rf <= cf:
                    newSpot = cSpot
                    cf = rf
                    spot[i] = newSpot[i]
                    dim = 1
                    continue
                cSpot[i] -= displacement[i]
            if dim != 1:
                cSpot[i] -= displacement[i]
                lf = f(cSpot)
                if lf <= cf:
                    cf = lf
                    newSpot = cSpot
                    spot[i] = newSpot[i]
                    dim = -1
                    continue
            if abs(displacement[i]) >= epsilon:
                displacement[i] = displacement[i] / 2.0
            i += 1
            dim = 0
    i = 0
    dim = 0
    iters = 0
    while i < len(spot) and iters <= 5000: #аналогично вводим итератор для огриничания времени работы алгоритма
        iters += 1
        cSpot = newSpot[:]
        if dim != -1:
            cSpot[i] += displacement[i]
            rf = f(cSpot)
            if rf <= cf:
                newSpot = cSpot
                cf = rf
                dim = 1
                spot[i] = newSpot[i]
                continue
            cSpot[i] -= displacement[i]
        if dim != 1:
            cSpot[i] -= displacement[i]
            lf = f(cSpot)
            if lf <= cf:
                cf = lf
                newSpot = cSpot
                spot[i] = newSpot[i]
                dim = -1
                continue
        if abs(displacement[i]) >= epsilon:
            displacement[i] = displacement[i] / 2.0
        i += 1
        dim = 0
    return newSpot


