# flash-hoarder

This is basically grabbing youtube videus during a crisis, or based on criteria.

Occasionally there is an event - a riot, a protest, a disaster, some kind of news event - during which a bunch of video is created and uploaded to the 
net, mostly youtube. That's how i'm scoping it anyways. 

The system will consist of one or more servers that will have attached storage,
all in the cloud. There will be a web/webapp front end that allows for review
of the library, maintenance of the keywords to scrape for, downloading the 
videos. 

Features:
- keyword manager
- submission page for specific URLs. 
- videos tracked by URL
- auto downloader: a cron job that will do a search for keywords and then 
download the videos that are new. 
- RSS feed of the video URLs for others who want to follow along at home
- spoofer to ensure that requests come from lots of different IP addresses 
to avoid getting blacklisted by youtube
- maintain the list of URLs in a database (mongodb?)
- daily cron job that makes a backup which is converted to a torrent of the 
downloaded videos for the day. 
