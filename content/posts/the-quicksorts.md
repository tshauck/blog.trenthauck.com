title: The Quicksorts
slug: the-quicksorts
summary: Another little Scala problem.
date: 2013-07-20
category: Code
tags: Scala

I've been spending some time trying to learn Scala and functional programming
lately.  To do so, I've been following Erik Meijer's [lecture series][fpseries] 
on the subject.  It uses Haskell as the example, which makes sense, but
I thought it would be a good opportunity to translate the ideas into Scala.

#Quicksorts

In the first lecture Erik mentions [quicksort][qwiki] in order to convey a few
ideas in functional programming.  So I translated it into Scala.

<!--<script src="https://gist.github.com/tshauck/6045393.js"></script>-->
<pre>
def quicksort(my_list: Iterable[Int]): Iterable[Int] = my_list match {
    case Nil => Nil
    case x :: xs => {
        quicksort(my_list.filter(_ < x)) ++ Iterable(x) ++
        quicksort(my_list.filter(_ > x))
    }
}
 
val r = quicksort(List(10, 100, 1000, 9, 99, 999))
val t = quicksort(Seq(10, 100, 1000, 9, 99, 999))

println(r)
println(t)
</pre>



A few points (and since I'm still learning, these may not be best practices):

  1. Erik mentions pattern matching as an important tool in functional
     programming.  Here `case` acts as pattern matching, with two outcomes.
     Either A) the incoming variable is `Nil`, therefore we should return
     `Nil`... this covers the empty list case, or B) we have a list and we need
     to sort it.  In this case, `x::xs` acts as a sort of unpacking (I work a lot
     in python) to give the `head` of the list and the `tail` of the list.
  2. The `.filter` operates on a Traversable (I used Iterable, but I think
     I could have used Traversable) in order to filter out any elements of the
     list that return false.
  3. The line `quicksort(my_list.filter(_ < x)) ++ Iterable(x) ++ quck//omitted`
     recursively glues together the list from the pivot point `x`.  Where
     x becomes is the head of the list.

Anyways, it's a pretty simple implementation and may not be the best, but I think
it makes a log of sense... again showing why Scala is being adopted all over the
place.

[fpseries]: http://channel9.msdn.com/Series/C9-Lectures-Erik-Meijer-Functional-Programming-Fundamentals
[qwiki]: http://en.wikipedia.org/wiki/Quicksort
