title: Pandas Group By Apply
slug: pandas-group-by-apply
date: 2013-09-20
summary: More apply, less typing.
tags: Python, PyData
category: Code

To calculate rates for web analytics - conversion rates, open rates, etc. - in `pandas` you can't use the traditional group by then apply a built in numpy function or a custom aggregation.

The `apply` function is incredibly versatile and is probably the best way to handle this.

First to create some basic data:

    > N = 1000
    > data = {'medium' = np.random.choice(['Organic', 'Direct'], size=N),
              'visits' = np.random.poisson(1000, size=N),
              'conversions' = np.random.poisson(10, size=N})

    > df = pd.DataFrame(data)
    > by_medium = df.groupby('medium')

##Naive Way

There is a way this can be done without `apply`, but it gets very old very quickly because it isn't versatile beyond the calculation you're doing.

    > visits = by_medium['visits'].sum()
    > conversions = by_medium['conversions'].sum()

    > conversions/visits

This certainly works, but again, it's a lot of typing and you're doing independent functions then joining the `DataFrames` on the indexes.

##The `apply` Way

Apply is generic and flexible, but isn't as easy as using `.sum()` on a metric.  It is better suited for this problem.

To use `apply` you first create a function that will be (surprise, surprise) applied to the groups.

    > def rates(group):
          conversions = group['conversions'].sum()
          visits = groups['visits'].sum()
          return conversions/visits

    > by_medium.apply(rates)

This feels better to me, though maybe it's not that much better, but the order feels right.

It's also easy to generalize this.

    > def rates(group, numerator, denominator):
         num = group[numerator].sum()
         den = group[denominator].sum()
         return num/den

    #assuming you had opens and sends as well
    > by_medium.apply(rates, 'opens', 'sends')
