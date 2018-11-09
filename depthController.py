class DepthController:

    def __init__(self, stop):
        self.__table = [1] + [0 for i in range(stop - 1)]
        self.__cursor = 0

    def addElementsToTreat(self, list):
        self.__table[self.__cursor] += len(list)

    def cursorUpdate(self):
        if self.__table[self.__cursor] == 0:
            self.__cursor += 1

    def elementsTreated(self):
        self.__table[self.__cursor] -= 1

    def depthControl(self):
        if len(self.__table) == self.__cursor:
            return False
        else:
            return True
