import numpy as np;
x= np.poly1d([1,0]);
print(x)
p = 1/(1+np.exp(-x))


print(p.deriv())
print(x.deriv())
