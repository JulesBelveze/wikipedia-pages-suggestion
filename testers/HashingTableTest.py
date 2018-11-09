#Testing the UrlDistinctTester class
import sys
sys.path.append('..')
import hashingTable
import time

top = time.time()


udt = hashingTable.UrlDistinctTester()
print(time.time()-top)

top2 = time.time()

res1 = udt.add("Hello")
res2 = udt.add("hgf")
print(res1, res2)
print(udt.add("Hello"))

print(time.time()-top2)


# return:
# 9.512563705444336
# True True
# False
# 9.393692016601562e-05

#10 seconds to create the object but it seems that just adding is quite fast