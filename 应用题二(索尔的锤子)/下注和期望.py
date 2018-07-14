import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import math

#参考https://en.wikipedia.org/wiki/Kelly_criterion
#资金的期望 E=plog(1+f*b)+((1-p)log(1-f)

#在0到0.99间生成1000个值
f = np.linspace(0,0.99,1000)

#对上述生成的1000个数循环用sigmoid公式求对应的y
y = [(0.6*math.log(1+i)+0.4*math.log(1-i)) for i in f]
subplot(1,2,2)
minorticks_on()
tick_params(which='minor',length=10)

plt.xlabel("f")
plt.ylabel("E")
plt.plot(f,y)
plt.show()