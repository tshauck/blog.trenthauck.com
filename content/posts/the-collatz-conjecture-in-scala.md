title: The Collatz Conjecture in Scala
tags: Scala
summary: Fun little problem in Scala.
slug: the-collatz-conjecture-in-scala
category: Code
date: 2013-06-15

[The Collatz Conjecture][wiki] is a simple recursive relationship that is pretty
easy to state but hard to prove.  The conjecture states that for any number,
n, if it's odd I take 3n + 1 and if it's even I take n/2... and
if I continue to do that I eventually get to one.  It's pretty intuitive to see
that this thing should go to one... if once you get an even number it's easy to
go down hill very fast (though clearly you can still hit odds).

So while the proof is beyond me, and apparently everyone else, it is interesting
to have a look at how fast a given starting point will go to 1.  As an aside,
this is a Project Euler problem, which I like to do when learning new languages
since the problems typically require the basics in any language.

##Euler Problem

The Project Euler problem is to find the number less than 1,000,000 that has
the longest path to 1.  And I'll do this in Scala since it's a language I'm
trying to get strong with.

To solve this we really need to do two things.

1.  Write a function that determines the path length to 1.
2.  Find the maximum number.

###Dat Function

This is pretty easy, we know from above that the Collatz Conjecture is recursive
so we want a recursive function and we know our requirement is to count the
number of recursions.

     def collatz(n: Long, c: Int = 0): Int = {
       if(n == 1) {
         return c + 1
       } else {
         if(n % 2 == 0) collatz(n / 2, c + 1)
         else collatz(3*n + 1, c + 1)
       }
     }

`n` is the number we've passed and `c` is the count of times we've run
one of the operations.  Basically if we're at one we return the count, if not we
cycle through again and iterate the count once.

###Dat `maxBy`

The next thing we need to do is take iterate through the list of numbers and
associate the numbers with their Collatz path length.

    val max_val = (1 until 1000000)
        .map(x => (x, collatz(x)))
        .maxBy(x => x._2)._1

It's shit like this that makes me realize why there's all the buzz around Scala.
It's got some of the ruby playfulness without being too long winded (although
that whole `_1` is lame, but w/e).  In these three lines I'm going from
1 through 1 less than 1,000,000, mapping each value to a tuple containing the
value and its path length, then getting the max tuple by path length, then
producing the value.  And it's done.

[wiki]: https://en.wikipedia.org/wiki/Collatz_conjecture
