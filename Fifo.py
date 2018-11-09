class Fifo:
    def __init__(self):
        self.__list = []

    def removeFirstIn(self):
        try:
            return self.__list.pop(0)
        except IndexError:
            pass

    def addList(self, listToAdd):
        self.__list.extend(listToAdd)

    def addElement(self, elementToAdd):
        self.__list.append(elementToAdd)

    def isFifoEmpty(self):
        return self.__list == []

    def getList(self):
        return self.__list
