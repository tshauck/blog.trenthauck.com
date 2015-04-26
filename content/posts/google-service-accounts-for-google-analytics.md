title: Google Service Accounts for Google Analytics
date: 2013-10-27
slug: google-service-accounts-for-google-analytics
Summary: How to use Google's new service accounts.
tags: Python, APIs
Category: Code

##Ways to Connect
There are a few different ways one can connect to the API.

1. Installed Application, if there's a legit use case for this let me know.
2. Client/Web Application, say you want to connect to someone else's information,
   they need to step in when the data is consumed and authorize this.  This is
   useful in many ways, but it's not what this post is about.
3. Service Account, say you really want to do some data work on your data
   or you're working for somebody else and they want you to analyze their web
   data.  And to do that you need to collect the data on some server without
   ever connecting to a browser.

##Service Accounts
The way this works, is ahead of time the Service Account user gets access to
the GA account and procures a key (not unlike an SSH key) and a "fake" (more
on this later) user.  With that information then the consumer of the API can
make repeated calls to the API.

#Making it Work
This code is actually very, very simple... thanks to the Python Client Library.
Highlevel, we'll make a build a service client with an authenticated request,
then once that service client is "ok" we'll make queries to the GA API.

##Building the Authentication Request

    import httplib2

    # make sure you have pyopenssl
    # because SignedJwtAssertionCredentials requires
    # it under the hood
    from oauth2client.client import SignedJwtAssertionCredentials

    # I realized after the fact that this import is missing
    # put another way, I didn't test this :)
    from apiclient.discovery import build

    f = file('pk.p12', 'rb') #you get this from api console
    key = f.read()
    f.close()

    # this is the email for the impersonated account
    # mentioned earlier, this MUST be added as a user in GA, you can specify
    # the profile if you make it a user or give it access to everything by 
    # making it an admin
    account = 'MYACCOUNT'

    # this is the scope of the api request, we'll set it to readonly (frankly
    # I'm not sure if you can write... I don't see why you'd be able to
    scope = 'https://www.googleapis.com/auth/analytics.readonly'

    # create the credentials object with our info, we still haven't authorized
    creds = SignedJwtAssertionCredentials(account, key, scope)

    # here authorize is overriding a normal http request that comes along with
    # httplib2 and applying the required headers
    request = creds.authorize(httplib2.Http())

    # this actually builds the service object which'll give us access to GA data
    service_account = build("analytics", "v3", request)

    ##Querying the Data

    # Once we have the account built it's easy to grab that info from GA

    service_account.data().ga().get(ids=profile_id,
                                    start_date = start_date
                                    end_date = end_date
                                    metrics = metrics,
                                    dimensions = dimensions).execute()

    # returns a dict for you to play with... probably just want to dump it to
    # json so you can move it to a db, but really it's easy to do anything

#WrapUp
So it really isn't a difficult thing to do, but you just need to know what's
going on.  Also, make sure you place the email you get from the API console as
a user... it _will_ not work without that.  See below for useful links.

[Scopes](https://developers.google.com/gdata/faq#AuthScopes)  
[Metics and
Dimensions](https://developers.google.com/analytics/devguides/reporting/core/dimsmets)  
[Google API Client Documentation](http://google-api-python-client.googlecode.com/hg/docs/epy/oauth2client-module.html)  

[news]: http://googledevelopers.blogspot.com/2012/09/python-client-library-for-google-apis.html
[docs]: https://developers.google.com/api-client-library/python/start/get_started
