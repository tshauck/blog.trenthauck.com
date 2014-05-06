import toolz
from toolz.functoolz import curry

import random

@curry
def exp_weighting(x_t_1, s_t_1, alpha=0.5):
    return alpha * x_t_1 + (1 - alpha) * s_t_1

ts = (random.randint(5, 10) for _ in range(20))
