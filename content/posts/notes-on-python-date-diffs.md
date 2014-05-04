title: Notes On Python Date Diffs
slug: notes-on-python-date-diffs
summary: Handles date differences in Numpy and regular Python
date: 2013-08-17
tags: Python, PyData
category: Code

How do we handle differences in dates in regular `python` and then in `numpy`.

Python
------

```python
> from dateutil.parser import parse

> a = parse('2013-01-01')
> b = parse('2013-01-31')

> a - b
datetime.timedelta(-30)
```

Given two date objects the difference is a `timedelta` object which is part of the `datetime` module.  That object has a `.days` attribute which has gives an integer value which is easier to work with.  After that it's up to the user to up or down sample it to a different time scale... eg `(a-b).days/7` would be the difference in weeks.

Numpy
-----

Numpy as a timedelta64 object that contains meta data for the time period and the actual difference represented.

```python
> import numpy as np

> diff = np.datetime64('2013-01-01') - np.datetime64('2013-01-31')
> diff
numpy.timedelta64(-30,'D')
```

Re-sampling can then by done by "dividing" by another `timedelta64` object that is at the level of interest... eg `diff / np.timedelta64(1, 'W')` is `-4.28`.  Also, to get to a real number to work with `diff.astype(int)`.

General
-------

In both cases an object that represents a time delta can be added to a date object to reconstruct the time that would be there.
