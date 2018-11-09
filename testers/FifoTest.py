##Testing Fifo class
import sys
sys.path.append('..')
import Fifo

fifo = Fifo.Fifo()

fifo.addList([1,2,3])
print(fifo.getList())

fifo.removeFirstIn()
print(fifo.getList())

fifo.addElement(4)
print(fifo.getList())

while not(fifo.isFifoEmpty()):
    x = fifo.removeFirstIn()
    if x == 4:
        fifo.addElement(5)
    print(x)

#return:
# [1, 2, 3]
# [2, 3]
# [2, 3, 4]
# 2
# 3
# 4
# 5
