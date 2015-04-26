title: Fun on PuzzleOR
slug: puzzleor-geom
category: Code
tags: Python
date: 2015-03-16
summary: Fun on PuzzleOr

I discovered an interesting site recently: puzzlor.com.  It's a site that every few months will pose an applied math problem.  Given the name "PuzzleOR" (and having perused the site) the math in puzzle is normally an operations researched focused.

The current puzzle is described here: http://puzzlor.com/2014-02_Coins.html.  The premise is that you're given three nickles, 3 dimes, and 3 pennies with the goal to arrange them in a 3x3 grid such that the rows and columns sum to a the given amount.

It's pretty interesting, if a bit simple... it's pretty easy to find a solution just by elimiating impossible solutions.  For example, given the first row sums to a number that ends with a one, therefore, that row must contain a penny.

But I'm not going to talk about the solution anymore.  I don't want to be a spoiler.  Instead I'll talk about a method of solving the problem, and more specifically, I'll discuss the some properties of that solution.  The solution is the most naive solution of this problem: random guessing.

### Guessing Quickly

Using numpy, I've written a simple implementation.  There are two function, one that produces assesses the solution and the other produces random matrices with according to the rules of the puzzle.

    import numpy as np
    
    def is_solution(arr):
        """ Take a 3x3 array and determine if it is a solution according to the rules defined
        here: http://puzzlor.com/2014-02_Coins.html
    
        Args:
            arr: 3x3 numpy array
    
        Using an "artisan :/" solution
        >>> is_solution([[1, 5, 5], [10, 1, 1], [10, 10, 5]])
        True
        """
    
        columns_are_correct = np.all(np.sum(arr, 0) == [21, 16, 11])
        rows_are_correct = np.all(np.sum(arr, 1) == [11, 12, 25])
    
        return rows_are_correct and columns_are_correct
    
    def random_choices():
        """ Yields random coin configurations. """
    
        coins = [1, 1, 1, 5, 5, 5, 10, 10, 10]
    
        while True:
            random_coins = np.random.permutation(coins)
            reshaped = random_coins.reshape(3, 3)
    
            yield reshaped

Then in this while loop masquerating as a for loop the code'll test solutions until one is found.

    %%time 
    
    for i, choice in enumerate(random_choices(), start=1):
        if is_solution(choice):
            print "Found the solution after {} guesses".format(i)
            break

    Found the solution after 696 guesses
    CPU times: user 37.7 ms, sys: 5.73 ms, total: 43.4 ms
    Wall time: 40.2 ms


### P(Solution)

Running this several times I got a range of solutions.  So my next quesion was how likely is a solution? Well, thinking about how guesses are generated and how to determine if to stop guessing is basically analagous to flipping a coin, if it's tails, reflip (guess again), and if it's heads stop.  This process can be modeled using a geometetric distribution.

The expected number of guesses is 1 over the probability of a solution.  Since it's possible to generate the number of guesses, but there's no knowledge of the underlying probability, it's possible to flip that equation and the probability of a solution is 1 over the number of guesses.

To see this in action, I'll wrap the code above in another loop just to get 500 samples of guesses.


    n = 500
    tries = []
    
    for k in range(n):
            
        for i, choice in enumerate(random_choices(), start=1):
            if is_solution(choice):
                tries.append(i)
                break

Below is a histogram of the number of attempts, along with the estimate of the probability of a solution.


    f, ax = plt.subplots(figsize=(10, 4), ncols=2)
    
    ax[0].hist(tries)
    ax[0].set_title("Number of attempts")
    
    ax[1].hist(1. / np.array(tries))
    ax[1].set_title(r"Estimate of $p$")

    <matplotlib.text.Text at 0x10aaee8d0>

![png](/assets/puzzlor-geom.png)

Using all the trials, the best estimate of $p$.

    p = 1. / np.mean(tries)
    print p
    0.00059330068597425304

There's probably an exact solution available via combinatorics, but uggg... it's just so much easier to simulate.

And that's it.  Just a little fun.
