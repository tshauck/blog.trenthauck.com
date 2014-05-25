title: Testing Static Sites with PlanOut
slug: pelican-plus-planout
date: 2014-05-18
Summary: And other cool shit along the way.
Category: Data Science, Code
Tags: Testing, Statistics
draft: yes
testpost: yes

# Introduction

The code referred to in the post is available [here][planoutapi], though it may
not match exactly.

[PlanOut][planout] has been out for a little while now. The first open source
commit happened in late January, with the lion's share happening in mid-March.
Since it's been out, I've wanted to play with it, but haven't found the time.
However, as I was walking home from work this weekend and saw  tweet...

<blockquote class="twitter-tweet" lang="en"><p>Tutorial in running online field
experiments from <a href="https://twitter.com/eytan">@eytan</a> and <a
href="https://twitter.com/seanjtaylor">@seanjtaylor</a> <a
href="http://t.co/JJHbCHvy7Y">http://t.co/JJHbCHvy7Y</a> Yes, it uses
PlanOut.</p>&mdash; Dean Eckles (@deaneckles) <a
href="https://twitter.com/deaneckles/statuses/469980676494594049">May 23,
2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

... that got my brain going.  First I thought, man I'd love to attend (and still
would), but since that's unlikely I thought I should run my own field
experiment.  And with that I decided to make the time and a Memorial Day Weekend
hack was born.

## AB Testing With Static Sites

Dynamic stuff on static sites is not easy, and it's not supposed to be.  The
whole idea is to trade off the dynamism for easy content generation.  That
said, there's no reason why SOA concepts don't apply.

So the idea is pretty simple, put PlanOut behind an API, use client side JS to call
the API and serve the treatment, and then use GA to store the response.  Oh,
also, use some other cool shit along the way.

# Plan of Action

Some more detail on how this will work:

1. The Experiment: Setup a PlanOut Experiment with treatments, overwrite PlanOut's
   logging to log the exposures to postgres.  The experiment will be a 3x2
   factorial design with three variants of a message used and two styles.  The
   unit with be a cookie\_id, which I'll talk more about in a bit.
2. The Glue: Have [Tornado][tornado] listen for incoming requests then serve the
   treatments as set by PlanOut.  Really this could be any thing that can import
   Python code and respond to `GET` requests.  Also, let's have some fun, so
   Docker will be used to put PlanOut plus the API in their own container and
   postgres in its own container.
3. Client side stuff: Just enough JQuery will be used to make the request to the
   API and modify the content with the appropriate treatment.  We'll also need
   to keep track of the response to the experiment so I'll use GA here, but,
   again, something else could be used (like a `POST` back to the API).

# PlanOut

I'll defer to [PlanOut's documentation][planout] for an introduction to PlanOut,
but there are some specifics with relation to what I'm trying to accomplish worth
noting.

## Experimental Setup

As mentioned, I'm running a pretty simple experiment.  First, I'll show one of
three text options:

```
a = ""
b = "Welcome to the blog of Trent Hauck, have a look around."
c = "Welcome to the blog of Trent Hauck"
```

And the text can be styled in one of two ways:

```
true: class="alert alert-info"
false: class=""
```

The CSS is from [Bootstrap][bootstrap].  In the event text a is chosen, no text
will be stylized.

This leads to the 3x2 factorial design I mentioned earlier.  Factor A the text,
has three options, factor B the style has two options - leading to 6 different
treatments.

There is something extra to consider here, since style will have no effect on
empty text the design is inherently unbalanced. 1/3 of subjects will receive the
no text treatment, while 2/3 of the rest of the subjects will receive the four
other outcomes.  Hopefully after some time, I'll report the findings of this
experiment and can go into the details of some benefits and challenges this
produces.

The goal of the test is to test how the welcome message and
style affect the engagement with the page, which can be measured several ways,
but here time-on-site, is the main metric of interest.  Text Greeting B has a
call-to-action that invites the subject to look around.

One final note in this section, the unit is cookie\_id.  That's a bit of a
misnomer, it's actually a random variable stored in Local Storage that is
conditionally set if the user doesn't have one yet.  The reason for this, is
PlanOut will maintain the exposed treatment across subjects based on a hash of
the unit.  It would be better to have a user id, since a user id persists across
platforms, browsers, etc.  My cookie\_id exists at the browser level (and only as
long as the user doesn't clear local storage).

## Overwriting PlanOut's Logging

From a code perspective, one thing the PlanOut documentation mentions, but
doesn't provide many details on is logging through means other than the `logging`
module.  I prefer to use postgres to make it easier to work with the data later,
so in this section I'll demonstrate how to make that happen.

First, PlanOut has a `SimpleExperiment` class which is sub-classed to add the
details of the given experiment.  It's fairly simple then to add a class between
`SimpleExperiment` and `MyExperiment`, which overwrites `SimpleExperiment`'s
logging.

```{python}
from planout.experiment import SimpleExperiment

import os

import psycopg2 as pg
from psycopg2.extras import Json as pJson

class PostgresLoggedExperiment(SimpleExperiment):

    def configure_logger(self):
        CONN_PARAMS = {'database': 'experiments',
                       'user': os.getenv('DB_ENV_USER'),
                       'password': os.getenv('DB_ENV_PASS'),
                       'host': os.getenv('DB_PORT_5432_TCP_ADDR'),
                       'port': os.getenv('DB_PORT_5432_TCP_PORT')}

        self.conn = pg.connect(**CONN_PARAMS)

    def log(self, data):
        cursor = self.conn.cursor()

        columns = ['inputs', 'name', 'checksum', 'params', 'time', 'salt',
                   'event']

        names = ','.join(columns)
        placeholders = ','.join(['%s']*len(columns))
        ins_statement = ("insert into experiments ({}) values ({})"
                         .format(names, placeholders))

        row = []
        for column in columns:
            value = data[column]
            row.append(pJson(value) if isinstance(value, dict) else value)

        with self.conn.cursor() as curr:
            curr.execute(ins_statement, row)

        self.conn.commit()
```

The code isn't that pretty (is any database code?), but after simply overwriting the
`configure_logger` method, and the `log` method storing data in postgres is now possible.
Since the data that is passed to `log` is json, any of `data`'s  values that are json
will be stored as json so I can have a row per exposure.

Now to define the experiment,

```{python}
class MyExp(PostgresLoggedExperiment)
```

is used instead of

```{python}
class MyExp(SimpleExperiment)
```

PlanOut seems to be a great tool.  It was designed by the top notch Engineers
and Data Scientists at Facebook specifically for this kind of work, so a lot of the tedious,
but important aspects of online testing are handle.  Testing is really
easy to mess up, so having a repeatable system is important.

# The Glue (The API)

This is a simple, but crucial, part of the setup.  Again, due to the limitations
of the static site PlanOut needs to be hosted elsewhere and have some mechanism
to serve the treatments.  Tornado will do that job here.

## Tornado To Serve Requests

Tornado is a fast web server for python.  I won't go into the details since it
gets the job done.  But it's worth saying a few things: 

* I did have to overwrite the standard `RequestHandler` to serve jsonp due to
  [Same Origin Policy][sop].  I don't like web development.
* The server accepts requests that match the regex `/hpexp/(\+d)`, that is
  /hpexp/(digits).  Where digits are the cookie_id, i.e. the unit of the
  experiment.

```{python}
import tornado.ioloop
import tornado.web
import json
from tornado.escape import json_encode

from experiments.example import ExampleExperiment

class ExampleExp(tornado.web.RequestHandler):
    def get(self, cookie_id):
        exp = ExampleExperiment(cookie_id=cookie_id)

        return_json = {'inputs': exp.inputs,
                       'greeting_text': exp.get('greeting_text'),
                       'style': exp.get('style')}

        self.write(json_encode(return_json))

    def write(self, data):
        super(ExampleExp, self).write("localcallback(" + json.dumps(data) + ")")
        self.set_header('Content-Type', 'application/javascript')

application = tornado.web.Application([
    (r"/hpexp/(\d+)", ExampleExp),
])

if __name__ == '__main__':
    application.listen(8999)
    tornado.ioloop.IOLoop.instance().start()
```

## Docker

I've been using Docker quite a bit lately, and while not strictly required for
this, it is really nice to be able to automatically start the API service and
leave it is its own container.  There are a few cool things I learned or did
along the way. This isn't relevant to the PlanOut testing in general so it
doesn't hurt to skip ahead.

### Automatic Service Starting

Through the use of [phusion/basebox][basebox] it's quite easy to have Docker
start the service.  Basebox replaces Ubuntu's Upstart with runit.  To take
advantage of this, I simply created the directory `/etc/service/planout`.  And
copied an executable run.sh there under the name run.

```
# in run.sh

#!/bin/sh

exec python /planoutapi/api.py
```

Then to start the container, I call `make run`.

```
# Makefile

PORT:=0.0.0.0:8999

run:
    docker run -d -p $(PORT):8999 --link postgresql:db thauck/planoutapi
```

The critical part is `-d` which starts the container in the background and
prints the container's hash.

See my Dockerfile for more info.

###Linking

I've taken advantage of linking containers twice so far in this post without
mentioning it.  First, in the `CONFIG` variable of my `PostgresLoggedExperiment`
and just above in `make run`.

Linking allows you to create a parent-child relationship between two containers
in Docker.  This is essential to keep services isolated, but building up apps
that take advantage of several containers.  The parent-child relationship allow
for facile communication of the environments, for example, my setup of postgres
only available to localhost, but with the link the parent (the API) can talk to
the child (this is more secure too).  Along these lines the parent has access
to the child's environment variables, so `$DB_ENV_USER` is the user created on
in the postgres container, but I don't have to remember the user, just the
variable.

###Postgres

I'm using the [this][postgres] container setup.  It allow for the stuff
mentioned above, but that's not was this section is about.  IMO, what's
interesting here is json in postgres.  At this point there's no point in using a
different relational database than postgres (and maybe event document store) for
that matter.

I wanted to keep a line per exposure, but I also wanted a general schema where I
could store multiple experiments.  This is tricky when you consider an
experiment could have several factors.  It's not straight forward how to design
a table that can handle many experiment types.  Therefore, storing json in json
fields allows for the flat design to be maintained.

Here's how the table was created:

```{sql}
CREATE TABLE experiments (
    id serial primary key,
    inputs json,
    name varchar(300),
    checksum varchar(50),
    params json,
    time bigint,
    salt varchar(300),
    event varchar(300)
)
```

This matches with the top level values PlanOut logs per exposure so we can
maintain the sample table for multiple experiments.

# Client Side

Time to end with my least favorite part, web stuff... (read, I'm gonna keep this brief.)

##Just enough JQuery (which is probably too much)

See github[planoutapi] (under scripts/) for more, but when the page loads JQuery makes a AJAX call to
the endpoint, and updates the content with the appropriate treatment.

##The Response Variable

Google analytics can easily track time on site, therefore, I'll have GA set a
custom dimension as the value of the unit.  The subject tracked in GA can then
be matched with the subject's exposure, and it's then possible to see if our
experiment had the desired effect.

# Conclusion

This was a pretty fun hack to put together, and I'll probably be using it more
in the future.  Testing is hard to get right, and PlanOut goes a long way in
helping get the small stuff right.

<div id=twitter></div>

# Resources

* [PlanOut][planout]
* [PlanOut Paper][planoutpaper]

[planout]: https://github.com/facebook/planout
[bootstrap]: http://getbootstrap.com/components/#alerts
[planoutapi]: https://github.com/tshauck/planoutapi
[sop]: http://en.wikipedia.org/wiki/Same-origin_policy
[basebox]: https://github.com/phusion/baseimage-docker
[postgres]: https://github.com/Painted-Fox/docker-postgresql
[twitter]: https://twitter.com/trent_hauck
[planoutpaper]: http://www-personal.umich.edu/~ebakshy/planout.pdf
[tornado]: http://www.tornadoweb.org/en/stable/
