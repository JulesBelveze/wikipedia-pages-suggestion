#Testing the Depth controller class
import sys
sys.path.append('..') # add parent folder
import depthController

dc = depthController.DepthController(2)

print(dc.getCursor(), dc.getTable())

dc.elementsTreated()
dc.cursorUpdate()
print(dc.getCursor(), dc.getTable())

if dc.depthControl():
    dc.addElementsToTreat([1,2,3,4,5,6])
print(dc.getCursor(), dc.getTable())

for i in range(6):
    dc.elementsTreated()
    dc.cursorUpdate()
    print(dc.getCursor(), dc.getTable())

print(dc.depthControl())




# return:
# 0 [1, 0]
# 1 [0, 0]
# 1 [0, 6]
# 1 [0, 5]
# 1 [0, 4]
# 1 [0, 3]
# 1 [0, 2]
# 1 [0, 1]
# 2 [0, 0]
# False

