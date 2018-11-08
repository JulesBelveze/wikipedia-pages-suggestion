#hashing table to know if an elmt has already been treated

from BitVector import BitVector
import mmh3

class url_distinct_tester:
        def __init__(self):
                self.__bitvector = BitVector(size = 2**32)

        def add(self, elmt):
                """Add an elmt in self if not in and return True, else does nothing
                and return false"""
                hash_elmt = mmh3.hash(elmt, seed)
                if self.__bitvector[j]:
                        initially_in = False
                else:
                        self.__bitvector[j] = 1
                        initially_in = True
                
                return initially_in

        def get_bitvector(self):
                return self.__bitvector
