# hashing table to know if an elmt has already been treated

from BitVector import BitVector
import mmh3


class UrlDistinctTester:
    def __init__(self):
        self.__bitvector = BitVector(size=2 ** 32)

    def add(self, elmt):
        """Add an elmt in self if not in and return True, else does nothing
        and return false"""
        hash_elmt = mmh3.hash(elmt, 1)
        if self.__bitvector[hash_elmt]:
            initially_in = False
        else:
            self.__bitvector[hash_elmt] = 1
            initially_in = True

        return initially_in

    def getBitvector(self):
        return self.__bitvector
