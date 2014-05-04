title: Kicking Visualization
slug: kicking-visualization
date:2013-12-02
Summary: Looking a kicking accuracy by yardline.
tags: Visualization, Tableau
Category: Code


Needing to get my analytical fix outside of work now-a-days (I spend most my time building stuff, which is good and bad) I have to look to other areas to strech my skills.  Sports Analysis, which has undergone an explosion in interest over the last several years seems like a natural fit - lots of data, personal interest, external value in doing it well, etc.

#Are You Ready for Some Football
The next question is where in that realm to first dip my toe... the answer is obviously the one of the most crankerous subjects I've come across - field goal kicking percentages.  The gist of the argument for those who don't think that analysts (read ex-player color men) do a good job is the probability to make a field goal is highly dependent of accuracy and distance.  So saying a kicker has a 85% probability of making a field goal isn't very valuable.  The other thing people seem to have issue with is "field goal range" the idea that there is a line in the sand where if a team reaches that yardline the kick is as good as made.  If you watch football you've certainly seen the red line that goes across the screen.

#A Better Visualiztion
I hope to explore the probability question in more detail later, but for now, let's explore the visualization aspect.  The question is, is there a better way to incorperate the probabilistic nature of a field goal kick that makes sense to the fans? I'd argue there is, and it's simple as all good things are.

#First Things First
I should point out now that the data is from infochimps and is [play by play for 2002-2009][1].  In another future post I hope to walk through the data munging in more detail, but basically it was [csvkit][2] to get only the kicking plays then load that into postgres.

#The Improvement
This is probably very obvious, but why not combine the probabilty changes by yardline and a football field-esque visualization to create something easy to understand.  And with that, I give you...

<script type='text/javascript' src='http://public.tableausoftware.com/javascripts/api/viz_v1.js'></script><div class='tableauPlaceholder' style='width: 544px; height: 609px;'><noscript><a href='#'><img alt='Kicking Viz ' src='http:&#47;&#47;public.tableausoftware.com&#47;static&#47;images&#47;Ki&#47;KickingViz&#47;KickingViz&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz' width='544' height='609' style='display:none;'><param name='host_url' value='http%3A%2F%2Fpublic.tableausoftware.com%2F' /> <param name='site_root' value='' /><param name='name' value='KickingViz&#47;KickingViz' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='http:&#47;&#47;public.tableausoftware.com&#47;static&#47;images&#47;Ki&#47;KickingViz&#47;KickingViz&#47;1.png' / > <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div><div style='width:544px;height:22px;padding:0px 10px 0px 0px;color:black;font:normal 8pt verdana,helvetica,arial,sans-serif;'><div style='float:right; padding-right:8px;'><a href='http://www.tableausoftware.com/public/about-tableau-products?ref=http://public.tableausoftware.com/views/KickingViz/KickingViz' target='_blank'>Learn About Tableau</a></div></div>

I know this isn't fancy d3 stuff, but it's quick and easy and gets the point
across.  For the default view we're looking at Adam Vinatieri, one of the
greatest kickers all time.  And it's pretty obvious you want to get him closer
than the 35 yardline - though he is very clutch so he probably would be good if
the game was on the line.

I hope to continue this foray, so please stay tuned.

[1]: http://www.infochimps.com/datasets/2002-2009-nfl-play-by-play
[2]: http://csvkit.readthedocs.org/en/latest/
