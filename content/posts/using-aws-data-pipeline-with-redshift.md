title: Using AWS Data Pipeline with Redshift
slug: using-aws-data-pipeline-with-redshift
date: 2013-05-26
summary: How to use two of AWS's nicest data products together.
category: Code
tags: Data Science, Intrastructure, Code

_Update_: This is now built in functionality - no hacks required.

AWS Redshift has hit the scene with lots of press... and deservedly so, it's a
pretty impressive tool that feels about right for 2013 data management.  AWS
Data Pipeline on the the other hand is a pretty unheralded tool on AWS.  For the
uninitiated, it allows users to chain together data nodes and activities into
work flows similar to [SSIS][SSIS_LINK].

For example, say you want to take data from an S3 bucket on a nightly basis, run
it through an EMR job, and spit it back into S3 - no problem.  Right now AWS
Data Pipeline supports DynamoDB, RDS, and S3 endpoints.  You'll notice that
Redshift isn't currently supported... hence the post.  That said, I can't
imagine a world in which Amazon doesn't support Redshift as an endpoint.  It's
surely coming, just not fast enough for me.

##The Basic Idea

For demonstration purposes I'll be creating a very simple task, that takes in a
file from S3 then copies the output to Redshift.  In Data Pipeline I'll utilize a
`ShellCommandActivity` and an S3 `DataNode`.  Basically, we'll copy the script
to the machine that runs the activity from the `DataNode` and have it take a
command line argument that will be S3 Bucket plus Prefix that a [`COPY`][CP]
command will be run against.  The basic flow looks like this:

![Pipeline Diagram](/img/redshift-datapipeline.png "Pipeline Diagram")

##The Script

For this script I'll be using Clojure.  There were a couple reasons behind that
choice, the main reason is that I want to be able to package the whole file into
a single run-able file (an uberjar)... and it's a fairly simple project to write
with Clojure.  

Writing the script is left as an exercise to the reader (Who does this guy think
he is?).  The import part of the code, the the `COPY` command.  Essentially, it
should be able to construct required string.  With Redshift it is important to avoid
single inserts and `INSERT INTO A SELECT * FROM B` when possible.

The function to create the copy command:

    (defn copy-cmd
      "Takes a S3 Bucket and AWS credential string and produces the COPY
      command"
      [file-name cred-str]
      (str "COPY mytable FROM"
           " '" file-name "'"
           " " creds-str
           " " "DELIMITER '\t'"
           " " "IGNOREHEADER 1"))

Run `lein uberjar` once you're done to get a standalone jar if you're using
leiningen.  This is really nice because we don't have to worry about any outside
dependencies.  For example, had I written this in Python I would've had to somehow
import a Postgres library, but here it's all ready to go... albeit in a large
file.

Once it's in a `jar` the execution should be as simple as:

    java -jar redshift-copy.jar -f s3://my-s3-location

##Setting Up the Activity

This part took me the longest - mostly because I sometimes don't like to look
before I leap, but also Data Pipeline isn't very mature so some behavior isn't
totally expected or implemented.  But that's the fun part right?

Like the image above, put the jar in an S3 bucket ([s3cmd][s3cmd]).  That in 
conjunction with setting the `stage` property of the activity to `true` will 
allow us to run the script on the activity machine - that whole stage file took
me largest to realize.

The command will then look like:

    java -jar ${INPUT1_STAGING_DIR}/redshift-copy.jar -f s3://my-s3-location/

One feature I'd like to see in Data Pipeline is the ability to combine staged
`Data Nodes` (copied to the activity machine) and non-staged `Data Nodes`.  The
reason for this, is that Redshift is designed to pull data from S3 into it's
tables, but if we copy the data locally then Copy that plan is for not.

##Conclusion

Clearly this is a 30K foot view, but the I tried to put this down 'on paper' to
help the person who was in my position a week or so ago but doesn't want to
experience the same learning curve that I did.

[SSIS_LINK]: http://en.wikipedia.org/wiki/SQL_Server_Integration_Services
[s3cmd]: http://s3tools.org/s3cmd
[CP]: http://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html
