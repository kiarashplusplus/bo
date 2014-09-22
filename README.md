blockedonline.com
=================

Production code for various parts of BlockedOnline.com

Read www.blockedonline.com/getinvolved to make sense of these. 

Many parts of blockedonline.com are still not in this repo (i.e. proxy and mac clients, ad-hock data cleansing code, etc) . 
I will move them all here eventually.

All the code needs refactoring for readability and better performance. 

Servers
=================

There are two servers: "bo_front" is to serve the webpages and also includes APIs. 
All the data collection clients send their data to the other server: "bo_back". "bo_back" processes
the data and puts it in the common database with bo_front.

Windows Client
=================

Used by mac user volunteers to send us data. Written in PyQt4.

Mac Client
=================

Used by mac user volunteers to send us data. 
 
Chrome Plugin
=================

chrome extension to collect data.