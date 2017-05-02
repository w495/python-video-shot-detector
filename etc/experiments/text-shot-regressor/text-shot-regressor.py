# -*- coding: utf8 -*-
from __future__ import absolute_import, division, print_function

from builtins import range

# Import the necessary modules and libraries
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeRegressor

print(__doc__)

filename = "bitva_za_sewastopl.luma.txt"

# filename = "drone-survol-paris.luma.txt"
# filename = "djadja-stepa-milicioner.luma.txt"

data = np.loadtxt('./dummy_shot/' + filename)
data = data[0:2000]

X = np.arange(0, data.shape[0], dtype=np.int).reshape(data.shape[0], 1)

print (data.shape)
print (X)
print (data)

# Fit regression model
clf_1 = DecisionTreeRegressor(max_depth=5)
clf_1.fit(X, data)

# Predict

X = np.arange(0, data.shape[0], dtype=np.int).reshape(data.shape[0], 1)
Y = clf_1.predict(X)
print ('Y = ', Y)

f = open("./result/" + filename, "w")

for i in range(data.shape[0]):
    print ("\t".join(map(str, [data[i], Y[i]])))

# Plot the results
plt.figure()
plt.scatter(X, data, c="r", label="data")
plt.plot(X, Y, c="g", label="max_depth=2", linewidth=2)

plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()

f.close()
