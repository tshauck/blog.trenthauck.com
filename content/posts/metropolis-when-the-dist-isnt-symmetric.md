title: Metropolis: When the Proposal Distribution isn't Symmetric
slug: metropolis-when-the-dist-isnt-symmetric
date: 2014-05-18
Summary: Using decorators and exponential backoff to avoid rate limits.
Category: Data Science
Tags: Python, Statistics

<div class="alert alert-warning">
This is a draft.
</div>

#The Setup First

There are several types of MCMC algorithms for approximating distributions, which is central in Bayesian statistics. The Metropolis-Hastings sampler is very commonly used, and it has several special cases which are well know (each of with have several special cases themself, isn't math fun!). For example, the Gibbs sampler is a special case of Metropolis-Hastings (TODO: Exaplain Why).  But it is not what the subject of this post.

The subject of this post is to compare the Metropolis-Hastings sampler, with its special case, the Metropolis sampler.  The Metropolis sampler is a special case when the proposal distribution is symmetric, that is, $Q(x|y) = Q(y|x)$.

To see the difference between the two, consider the acceptance ratio section of the algorithms.  In the Metroplis case,

$$\alpha = {P(x^{'})\over P(x_{t})}$$

Where $x^{'}$ is the proposed move in the parameter space, and $x_t$ is the current location.  The move between the two locations happens with probability $\alpha$.  (Make a foot note about 1).  The intuition is that if alpha is high (or even 1) then that value is more likely to be the parameter in question, and we should move there.

So that's great, but what happens when, as the post suggests, the proposal distribution isn't symmetric.  First our formula changes, but really that's the result of a fundemental change in how the ratios work.  The new fomula, then the discussion:

$$ \alpha = \frac{P(x^')}{P(x_{t})} \frac{Q(x^{'})}{Q(x_{t})} $$

It's clear something has changed, the second fraction.  $Q(\cdot)$ is the proposal distribution; it's the distribution that generates the proposed moves, $x^{'}$.  It's also worth noting here that when the 

Instead of a single ratio, there are now two.  The first was already described, but the second is the ratio of probabilties between our current x and our new x from the probability distribution that generate those values in the first place.

#Why Symmetry Matters

Taking a step back, it's not technically $P(\cdot)$ that matters, but $ P(\dot^' \rightarrow \dot) $, however the ratio of $\frac{P(\cdot^{'} \rightarrow \cdot)}{P(\cdot^{'} \rightarrow \cdot)}$ is equivilent to the probability ratio already present when the proposal distribution is symmetric, due to the characteristics of Markov Chains (covered elsewhere).  But, when the proposal distribution isn't symmetric. (\cdot prime is stupid, use $T$.)


[gibbs]: http://en.wikipedia.org/wiki/Gibbs_sampling
