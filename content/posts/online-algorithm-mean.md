title: Online Algorithm Mean and Variance
slug: online-algorithm-mean-and-variance
summary: A smarter way to find summary stats of large datasets.
date: 2013-07-12
category: Data Science
tags: Python, AWS, Data


This is a combination of two curiosities of mine for the last week or so.  I'm thinking about using a message queue for a project... so that's one have.  The other half, is that online algorithms seem like something I should know, or at least be comfortable with.  The most basic of which are for calculating the mean and variance of a list of numbers.  
 
The advantage of an online algorithm for these calculations are two fold (or maybe more, I'm clearly just playing with these).  First, you only need to do one pass of the data.  This saves batch processing of the data as new data comes in.  If we save our state, we can this update the calculations per the new data.  The other advantage is we're not doing math operations on huge sets of numbers.  This is good because we won't lose precision... or at least the opportunity for a lossy operation goes down.
 
The message queue side of the story is really simple.  To simulate a list of numbers coming in I can use a message queue, having one system generate numbers and pass them to the queue, I can then have another system poll the queue and act accordingly in updating the numbers.  I'll use Amazon SQS since it's what we'd probably use in the project.

##Writing the Numbers

This part has to come first, since if we don't have numbers we can't calculate moments.  Anyways it's the simpler of the two parts as well.

    import boto
    import random
    import time
    from boto.sqs.message import Message
     
    sqs = boto.connect_sqs()
    queue = sqs.get_queue('StreamingPlay')
     
    rands = (random.gauss(0, 1) for _ in range(1000))
     
    for rand in rands:
        m = Message()
        m.set_body(str(rand))
        status = queue.write(m)
        print "wrote:{}".format(m.get_body())
        time.sleep(.1)
     
    m = Message()
    m.set_body('Done')
    status = queue.write(m)

Hopefully this is simple to follow.  First I create a generate for 1000 random variables that follow a normal distribution.  Then for each number I write it to the queue.  Finally, once that's all done, I write 'Done' - easy-peasy.

##Reading the Numbers 

This section is slightly more complicated so we'll talk about it in a few sections.  The repo is available [here][github] if you want the full code.

    def new_mean(old_mean, new_number, n):
        return old_mean + (new_number - old_mean)/n

This is were the magic happens.  The function should be straight forward.  We simply take the old mean and update it with the delta between the old mean and the new mean by a an amount proportional to the number of numbers we've seen.  Think about it for a second... it feels right.

    from functools import partial
 
    def new_M2(old_mean, current_mean, M2, num):
        return M2 + (num-old_mean)*(num-current_mean)

    #this sits in a loop that polls for new numbers
    #some code has been omitted
    m2_calc = partial(new_m2, old_mean=mean)
    mean = new_mean(mean, new_number, n)
    M2 = m2_calc(current_mean=mean, M2=M2, num=num)

M2 is the kinda like a sum of squares, except it's off a number (the mean).  Once we have M2 we can then calculate the variance or the standard deviation without much work since n is the number of numbers we've seen, it's straight algebra at this point.
 
Again, full code is available [here][github].

[github]: https://github.com/tshauck/OnlineAlgo
