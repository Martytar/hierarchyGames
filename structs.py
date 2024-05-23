class funPart(): # "часть функции" т. е. функция в ограниченной условиями области (для оптимальных управлений таких функций много непересекающихся областях)
    def __init__(self, expression, restricts):
        self.exp = expression
        self.rest = restricts