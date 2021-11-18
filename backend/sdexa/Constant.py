class Constant:
    def __init__(self, value, unit=None, info=None):
        self.__value = value
        self.__unit = unit
        self.__info = info

    @property
    def value(self):
        return self.__value

    @property
    def unit(self):
        return self.__unit

    @property
    def info(self):
        return self.__info

    def __str__(self):
        return f"CONSTANT value: {self.value}, unit: {self.unit}, note: {self.info}"
