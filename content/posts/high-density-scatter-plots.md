title: High Density Scatter Plots
date: 2013-05-01
summary: Various ways to represent lots of points in a scatter plot.
tags: R, Code, Data
category: Data Science

I gave a [talk](http://blog.trenthauck.com/2013/05/04/analytics-for-developers.html) 
this weekend where a small portion of it was devoted to
visualization.  In it, I mentioned that charting distributions is important, but
that there are situations where a basic scatter plot won't work very well.  I
didn't do a very good job explaining situation where it isn't the best and possible solutions.

##The Why
Let's consider a situation where we have a lot of overlapping points and how that
looks with a basic scatter plot.  All examples in this post will use R and its
fantastic plotting library ggplot2.

First we need a sample of points that will have high density.

    df <- data.frame(x=rnorm(1000, 0, 1), y=rnorm(1000, 0, 1))

A basic plot looks like the following:

    library(ggplot2)
    ggplot(df, aes(x=x, y=y)) + geom_point()

![Basic Scatter Plot](/img/basic_scatter.png "Basic Scatter Plot")

It's fairly clear that there are a lot of points around `(0,0)`... but it's also
clear that there's just a black blob around `(0, 0)`.  So what if we wanted to
make that a bit more clear.

##Jitter
On easy option is to use jittering.  This is done (in ggplot2) by adding the
jitter argument to the `geom_point` function.

    ggplot(df, aes(x=x, y=y)) + geom_point(position = 'jitter')

![Basic Jitter Plot](/img/basic_jitter.png "Basic Jitter Plot")

Cool story, bro... so what's the difference.  Well here it's not really obvious
due the extra high density, which immediately gets to why jitter isn't always a
good option. That's because it attempts to slightly alter the position of the
points to make it more spread out, but if there's too many points it doesn't do
much.  Jittering is probably best when you don't have a huge number of points
and the exact location of those points isn't important.

##Adding Alpha
Another option is to use alpha on the points... effectively making the points
slightly transparent.  This create a situation where higher density areas will
appear darker.

    ggplot(df, aes(x=x, y=y)) + geom_point(alpha = 0.4)

![Basic Alpha Plot](/img/basic_alpha.png "Basic Alpha Plot")

This is certainly nicer than the jitter when a lot of points are present.

##Contour Lines
Here's another option that doesn't mess with the display of the points
themselves, but adds contour lines (like a map) that spells out the areas of high
density.

    ggplot(df, aes(x=x, y=y)) + geom_point() + geom_density2d()

![Basic Contour Plot](/img/basic_density.png "Basic Contour Plot")

It's pretty easy hear to figure out which area of the plot are of higher
density via the contour lines.  But there is one other option... and my personal
favorite.

##HexBins
We can draw a whole bunch of hexagons on our plot that will then be colored
dependent on the density. This is particularly good for lots of data.  The reason
for this is that with a huge number of points... the individual importance of a
single point goes down, but understanding the distribution is more important.

    ggplot(df, aes(x=x, y=y)) + stat_binhex()

![Basic HexBin Plot](/img/basic_hex.png "Basic Hex Plot")

##Conclusion
There's clearly several ways to do this, and this list isn't exhaustive, it's
more important to be able to justify the decision to use a particular plotting
technique than a broad statement about which of the preceding methods is best.
