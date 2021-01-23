#!/usr/bin/python3
#Coupon Collector Problem in Python
#x coupon population
#y number of tries
import numpy as np
import matplotlib.pyplot as plt
values=[]
index=[]
upto=1000
start=100
step=10
def couponCollector(n):
    return sum(np.random.geometric(float(n-k)/n) for k in range(n))
for iter in range(start,upto,step):
    print (str(iter))
    index.append(iter)
    values.append(couponCollector(iter))
plt.plot(index,values, linewidth=.1)
plt.savefig("coupon.png",dpi=400)
