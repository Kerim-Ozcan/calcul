# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import math

# 1. Fonction
def f(x):
    return math.log(x) - 1
# 2. Tracé de la courbe avec pas 0.05
X = np.arange(1, 6, 0.05)
Y = [f(x) for x in X]

plt.figure()
plt.plot(X, Y, label="f(x) = ln(x) - 1")
plt.axhline(0, color='black')
plt.axvline(math.e, color='red', linestyle='--', label="x = e")
plt.legend()
plt.title("Courbe de f(x) = ln(x) - 1")
plt.grid()
plt.show()

# 3. Méthode de dichotomie pour approximer e
a = 1.0
b = 6.0
eps = 1e-6

while b - a > eps:
    c = (a + b) / 2.0
    if f(a) * f(c) <= 0:
        b = c
    else:
        a = c

print("Approximation de e par dichotomie :", (a+b)/2)
