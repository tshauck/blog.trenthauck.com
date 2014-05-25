#Single Parameter Models

Presents four widely used one-dimensional models:

1. binomial
2. normal
3. Posson
4. exponential

Binomial model is good for data that arise from a sequence of n exchangable trials, where each trial has 2 outcomes.

Definitions from Bayes in 1763, example uses a probability space as a table.

* Prior Distribution: A ball $W$ is randomly thrown on the table, the horizontal position $\theta$ is expressed as a fraction of the table width.
* A ball $O$ is randomly thrown $n$ times.  The value of $y$ is the number of time $O$ lands to the right of $W$.

Problems:

1. Q: Prior is Beta(4, 4).  A coin is head less than three times, find the posterior.

The liklihood is the sum of cases when heads is 0, 1, or 2.  The liklihood times the prior is then the posterior to a constant.

