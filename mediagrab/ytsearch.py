#!/bin/env python3
# ytsearch.py - look for videos with a keyword, add the record to the database 
# 20-may-2021 rca initial commit to git. 
# still need command line options

import youtube_dl
from youtube_dl.utils import DateRange
import sqlite3
import os
import json
import sys
import getopt

DEBUG = 0;

settings = 'settings.json'
batch = 5

# assess the command line options
helptext =  'ytsearch.py [-k <keyword string> -d <database name> -b <batch size>] [-s <settings file>]'
argv = sys.argv[1:]
try:
   opts, args = getopt.getopt(argv,"hb:s:d:k:",["batch=","settings=","dbname=","keywords="])
except getopt.GetoptError:
   print (helptext)
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print (helptext)
      sys.exit()
   elif opt in ("-s", "--settings"):
      settings = arg
      continue
   elif opt in ("-b", "--batch"):
      batch = arg
   elif opt in ("-d", "--dbname"):
      dbname = arg
   elif opt in ("-k", "--keywords"):
      keywords = arg

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), settings)

with open(SETTINGS_PATH) as json_file:
    data = json.load(json_file)

if DEBUG:
	print(data['settings'])


try:
    keywords
except NameError:
    keywords = data['settings']['keywords']

try:
    batch
except NameError:
    batch = data['settings']['batch']

try:
    dbname
except NameError:
    dbname = data['settings']['dbname']


def get_yesterday():
	# Import date and timdelta class
    # from datetime module
    from datetime import date
    from datetime import timedelta
    # Get today's date
    today = date.today()
    # Yesterday date
    yesterday = today - timedelta(days = 2)

    #return it as yyyymmdd
    return yesterday.strftime('%Y%m%d')
    

# here is a list of the possible options
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'forcetitle': True,
    'forceurl': False,
    'forceid': True,
    'daterange' : DateRange(get_yesterday()),
#    'forceurl': True,
}
# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), dbname)


print ("keywords",keywords)
print ("dbname",dbname)

##########################################
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

##########################################
def save_ytinfo(con,ytid,url,description):
	sql = """
	INSERT INTO VIDEO (ytid, url,description,download) 
	VALUES (?, ?, ?, 0)"""
	cur = con.cursor()
	cur.execute(sql, (ytid, url, description))
	return cur.lastrowid

##########################################
def check_if_ytid_exists(con,ytid):
	sql = "SELECT ytid FROM video WHERE ytid=?"
	cur = con.cursor()
	cur.execute(sql, (ytid,))
	results = cur.fetchall()
	if len(results) == 0: 
		return False
	else:
		return True


################################################################################################
def check_if_table_exists(con,table_name):
	sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
#	sql = "SELECT ytid FROM video WHERE ytid=?"
	cur = con.cursor()
	cur.execute(sql, (table_name,))
	results = cur.fetchall()
	if len(results) == 0: 
		return False
	else:
		return True



table_create_sql = """
CREATE TABLE video(
    description text, 
    url text not null, 
    ytid text not null, 
    download int )""";


################################################################################################
# Extracts information using the "ytsearch:string" method
def search_yt_(con,searchstring):
    resultnum = batch 

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    	# build the search string
    	# ytsearch is another waay, we want to look at recent results. 

        sstring = "ytsearchdate" + str(resultnum) + ":" + searchstring

        try:
            infoSearched = ydl.extract_info(sstring)
        except youtube_dl.utils.DownloadError as e: 

            print ("error error? that one")
            self.error = e
            return False
            print ("can't do that one")
            pass


    mynum = len(infoSearched['entries'])
    # Output the information that has potential to be what I am looking for
    # iterate over the results wiht J
    print ("### My loop")
    for j in range(mynum):
        ytid = infoSearched['entries'][j]['id']
        if (check_if_ytid_exists(con,ytid) == False):
            print ('saving {} "{}"'.format(infoSearched['entries'][j]['id'], infoSearched['entries'][j]['title'].encode('ascii', 'xmlcharrefreplace')))
            save_ytinfo(con,ytid, infoSearched['entries'][j]['webpage_url'], infoSearched['entries'][j]['title'].encode('ascii', 'xmlcharrefreplace'))

#        for key in infoSearched['entries'][j]:
#
#            if key in [ 'id', 'webpage_url', 'title','channel_url','uploader','upload_date']: 
#                    print(' {}    {}' .format(infoSearched['entries'][j][key], key))
#        print("--")

################################################################################################
def printkeys():
    # Print the available keys
    print('\n keys available: \n')
    for i in infoSearched:
        print(i)
    for i in infoSearched['entries'][0]:
        print(i)
################################################################################################
# Extracts information using the actual URL method
def get_yt_info_single(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    infoUrlGiven = ydl.extract_info(url)

    print ("xxxx",infoUrlGiven)
    # Outputs the correct information I am looking for
    for i in infoUrlGiven:
        print ("--")
        if i == 'webpage_url' or i == 'title' or i == 'duration':
            print('\n {}    {}' .format(infoUrlGiven[str(i)], i))

################################################################################################
def create_video_table(connect):    
	print("create table")
	table_create_sql = """
	CREATE TABLE video(
	    description text, 
	    url text not null, 
	    ytid text not null, 
	    download int )""";
	connect.execute(table_create_sql, ())

################################################################################################
def db_disconnect(con):
	con.commit()
	con.close()
################################################################################################

if __name__ == "__main__": 
    connect = db_connect();

    if (check_if_table_exists(connect,'video') == False):
        create_video_table(connect);

    search_yt_(connect,keywords)

    db_disconnect(connect)


    # getting a channel needs some work
    url ="https://www.youtube.com/watch?v=Yf9A7eiRPJg"
    url ="https://www.youtube.com/channel/UC8BxSGcBKriJvoeyKOnJ6tA"
    #get_yt_info_single(url)



