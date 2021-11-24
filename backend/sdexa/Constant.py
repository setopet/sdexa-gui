"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""


class Constant:
    def __init__(self, name, value, unit=None, description=None):
        self.__name = name
        self.__value = value
        self.__unit = unit
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def unit(self):
        return self.__unit

    @property
    def description(self):
        return self.__description

    def __str__(self):
        return f"CONSTANT value: {self.value}, unit: {self.unit}, description: {self.description}"
