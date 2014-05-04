title: Daddy's First Decorator, or I finally Found a Use Case
slug: daddys-first-decorator
date: 2013-12-27
Summary: Using decorators and exponential backoff to avoid rate limits.
Category: Code
Tags: Python

I've known about decorators for a while - they show up pretty quick in many of
the most used python libraries.  For instance, in `flask` decorators are
extremely common.  They're used as the mechanism that associates a function with
a route.

```{python}
@app.route("/the_route")
def index():
    print "hi"
```
    
When you go to "example.com__/the_route__" the function `index` will be
called.  From a usability standpoint it seems perfect for its use case.

They show up many other places.  For example, in the test suite of `pandas`
there is an [`@network`][1] decorator.  I wish I would've explored this
earlier, because it's not to different from the code I'll be writing.
`@network` labels a test, and if that test is labeled it will skip the test
if a network connection cannot be established.  Very simple and very clean.
Staying in pydata land, Numpy has an entire [file][4] dedicated to
decorators.

##My Need
Before the solution, I should first explain the need.  I deal _a lot_ with APIs.
I work at a Marketing Analytics agency ([Alight Analytics][2]), we take our
clients data from standard sources (Twitter, Google Analytics, Facebook, etc),
mash it together, and try to derive some insights and recommendations.  As
a data scientist, I need to get that data out so I can use it and store it.  

When you're dealing with a lot of data for a lot of clients rate limits come
into the picture very quickly.  I need my code to run as fast as I can, while
still being observant of limitations.  A naive solution, would be to sleep some
amount of time.  For example, if you can't make more then 10 calls a second
(Google Analytics rate limit) you could sleep for .1 seconds after every call if
your code takes some epsilon to run you'd be fine.

The better solution solution is [exponential backoff][3] - it's an alogrithm that
asks for forgiveness rather than permission.  The idea is to make calls as fast
as you can, when you get an error pause for _2^n_ seconds where _n_ is the
attempt.  Very simply it might look like:

```{python}
def make_call():
    n = 0
    while True:
        try:
            return api.data()
        except:
            time.sleep(2**n)
            n += 1
```

This isn't the best solution. For example, if there is something wrong with your api call other than you're making them too fast it'll keep looping, but it illustrates the solution.
                                                                
##My Solution
                                                                
I could start with the whole garb about python's functions being first class, but you can get that elsewhere (you probably should get it elsewhere, it's useful to know). Therefore, I'll start with the code.
                                                                
```{python}
import time

def exp_backoff(tries=2, passable_exceptions=Exception):

    def exp_backoff_outer(function):

        def exp_backoff_inner(*args, **kwargs):
            for x in range(tries):
                try:
                    return function(*args, **kwargs)
                except passable_exceptions:
                    if x == tries - 1:
                        raise
                    time.sleep(2**x)
                else: 
                    raise 
        return exp_backoff_inner 

    return exp_backoff_outer
```

Sadly the syntax for a decorator with arguments is really silly. Wrapping a function twice is smelly. If I didn't want to have a configurable number of tries and didn't want to choose the `passable_exceptions` then I could remove he `exp_backoff_outer`. Besides the whole wrapping madness it's not much different than the above. The only difference is the use of `else` in the try-except block. If the `passable_exceptions` isn't modified from the default it'll never see the light of day, if it is set to something like `ValueError` then it will if a non-`ValueError` exception occurs. The other difference from the first example is exiting after the code has been tried `tries` times.

The decorator would be used like...

```{python}
@exp_backoff
def add(*args):
    sum(args)
```

So if I called add with something like `add(1, 1)` there would be no problem, but if I did `add(1, "hi")` you'd get a pass for 3 seconds (2^0 + 2^1) before seeing a `ValueError` exception.

Anyways, this is probably one of the posts that'll be more useful for me later, much like my post on `numpy` dates and times (fuck those), but hopefully it's useful for others.

[1]: https://github.com/pydata/pandas/blob/master/pandas/util/testing.py#L969-L1065
[2]: www.alightanalytics.com
[3]: http://en.wikipedia.org/wiki/Exponential_backoff
[4]: https://github.com/numpy/numpy/blob/master/numpy/testing/decorators.py
