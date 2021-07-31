#!/bin/env python3
# save_video.py work through database table, downloading the videos as we go. 
# 
# 26-may-2021 rca initial commit to git. 

import youtube_dl
from youtube_dl.utils import DateRange
import os
import json
import sys
import getopt
import db_util

DEBUG = 0;
data = {}

settings = 'settings_sv.json'
data = db_util.load_settings(settings)

batch = 5

# assess the command line options
helptext =  'ytsearch.py -k <keyword string> -d <database name> -b <batch size> -s <settings file>'
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
        data = db_util.load_settings(arg)
    elif opt in ("-b", "--batch"):
        batch = arg
    elif opt in ("-d", "--dbname"):
        dbname = arg

try:
    batch
except NameError:
    batch = data['settings']['batch']

try:
    dbname
except NameError:
    dbname = data['settings']['dbname']

# here is a list of the possible options
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
# enable downloading and full logging for downloads. 

ydl_opts = {
    'quiet': False,
    'skip_download': False,
    'forcetitle': True,
    'forceurl': False,
    'forceid': True,
#    'forceurl': True,
}
# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), dbname)

print ("dbname",dbname)

connect = db_util.db_connect(DEFAULT_PATH);

#search_yt_(connect,keywords)
db_util.get_new_videos(connect,ydl_opts)
db_util.db_disconnect(connect)

# getting a channel needs some work
url ="https://www.youtube.com/watch?v=Yf9A7eiRPJg"
url ="https://www.youtube.com/channel/UC8BxSGcBKriJvoeyKOnJ6tA"