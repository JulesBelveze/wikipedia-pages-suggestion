class Fifo:
    def __init__(self):
        self.__list = []

    def removeFirstIn(self):
        try:
            self.__list.pop(0)
        except IndexError:
            pass

    def addList(self, listToAdd):
        self.__list.extend(listToAdd)

    def addElement(self, elementToAdd):
        self.__list.append(elementToAdd)
