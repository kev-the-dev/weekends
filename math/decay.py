#!/usr/bin/env python3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def exponential(x, start, halflife):
    return np.where(x < start, 0., np.power(0.5, np.divide(x - start, halflife)))

HOURS = 48
t = np.arange(0.0, HOURS, 1)

ys = np.zeros(len(t))
for offset in np.arange(0, HOURS, 8):
    print(offset)
    ys = ys + expoential(offset

#for xt in t:
#    y = exponential(xt, 0, 8)
#    ys.append(y)

fig, ax = plt.subplots()
ax.plot(t, ys)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

plt.show()


