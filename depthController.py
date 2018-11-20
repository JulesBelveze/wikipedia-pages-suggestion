class DepthController:

    def __init__(self, stop):
        """The DepthController object allow us to follow the depth during the computation on the fifo
        We have a table for saying how many elmts do we need to treat in a given depth
        We have a cursor allowing us to know the current depth
        the argument stop is the maximum depth we want
        we can use the method depthControl to know when the wanted depth is obtained"""
        self.__table = [1] + [0 for i in range(stop)]  # length = stop + 1 in order to go through the last layer pages
        self.__cursor = 1
        self.__stop = stop

    def addElementsToTreat(self, list):
        """Since we added an elmt in the fifo we want to know how many we have to treat before the next depth step"""
        self.__table[self.__cursor] += len(list)

    def cursorUpdate(self):
        """Allow to update the cursor in order to know the depth"""
        if self.__table[self.__cursor - 1] == 0:
            self.__cursor += 1

    def elementsTreated(self):
        """we have treated an elmt in the given depth"""
        self.__table[self.__cursor - 1] -= 1

    def depthControl(self):
        """return True if we acan continue going in further depth
        return False if we are currently at the stop point"""
        if self.__cursor <= self.__stop:
            return 1
        elif self.__cursor == self.__stop + 1:
            return 2
        elif self.__cursor > self.__stop + 1:
            return 3

    def getTable(self):
        return self.__table

    def getCursor(self):
        return self.__cursor
