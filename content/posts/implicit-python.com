title: Implicit Python
slug: iumplicit-python
category: Opinion
tags: Code
date: 2015-03-24
summary: An opinion piece

Python is a great language.  I truely owe a lot to Python the language and the community.  But lately it's been bugging me more than usual.

I'm not sure why it started or when, but I think it's some combination of the influence of other languages I'm using and that I'm more time constrained.

This is the _Zen of Python_:


    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!

A lot of this is really good advice, for programming or otherwise.  There're are a few lines in particular that are relevant to my recent experiences.

    (12) In the face of ambiguity, refuse the temptation to guess.

In my day job, I'm make guesses all the time.  I try to make sure they're backed with facts and of sound methodology.  I don't want my programming language
to ever guess.  I want it to break if things are amiss, espicially the simple stuff.

Here's the example I just experienced:

    >>> float("INF")
    inf

This is a supidly simple line of code.  In and of itself, it's no problem.  But what if you have a bunch of strings, and you need to







    > Move type checking to the client level

Argument related to type checking


Forgivness
