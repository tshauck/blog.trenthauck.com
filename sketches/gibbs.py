"""

#Introduction

Gibbs sampling is aplicable when the joint distribution is difficult to sample
from, but the marginal distributions are known or easier to sample from.  Therefore
gibbs sampling is well suited for Bayesian Networks because these networks are
often represented by marginal distributions.

"""

import numpy as np

xs = []

for _ in range(3000):
    mu = np.random.normal(10, 1)

    s_1 = np.random.gamma(1, 1)
    s_2 = np.random.gamma(1, 10)
    s_3 = np.random.gamma(1, 20)
    s_4 = np.random.gamma(1, 50)

    x_1 = np.random.normal(mu, s_1)
    x_2 = np.random.normal(mu, s_2)
    x_3 = np.random.normal(mu, s_3)
    x_4 = np.random.normal(mu, s_3)

    xs.append([x_2, x_3, x_4])

xs = np.array(xs)

import matplotlib.pyplot as plt
plt.close()

_, n = xs.shape
for x in range(n):
    min_x = int(min(xs[:, x]))
    max_x = int(max(xs[:, x]))

    bin_width = 2

    plt.hist(xs[:, x], bins=np.arange(min_x, max_x + bin_width, bin_width),
             alpha=.5, label="s_{}".format(x))

plt.legend()
plt.savefig('gibbs.png')
