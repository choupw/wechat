import numpy as np;
import symbol

#sigmoid function
def nonlin(x, deriv = False):
    if(deriv == True):
        return x*(1-x)
    return 1/(1+np.exp(-x))


# input dataset
x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

# output dataset
y = np.array([[0, 0, 1, 1]]).T

np.random.seed(1)

#init weight value
syn0 = 2*np.random.random((3,1))-1

print(syn0)

# for iter  in range(1):
#
#     l0 = x  # the first layer,and the input layer
#     l1 = nonlin(np.dot(l0, syn0))  # the second layer,and the output layer
#     print('l1')
#     print(l1)
#     l1_error = y - l1
#     print('l1_error')
#     print(l1_error)
#     l1_delta = l1_error * nonlin(l1, True)
#     print('l1_delta')
#     print(l1_delta)
#     syn0 += np.dot(l0.T, l1_delta)
# print("outout after Training:")
# print(l1)


# p = np.poly1d(1/(1+np.exp(-x)))
p = 1/(1+np.exp(-x))
print(p)
# d = p.deriv()
# print(d)