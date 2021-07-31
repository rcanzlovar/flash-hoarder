

import os
import json
import sys
import youtube_dl
from youtube_dl.utils import DateRange
import sqlite3

###################################################
def load_settings(file):
    """
    get the batch size, keywords, database name, etc from a settings file in json format
    :param file: name of the file, in the current directory as the script
    :return: dictionary with the settings.
    """
    SETTINGS_PATH = os.path.join(os.path.dirname(__file__), file )
    with open(SETTINGS_PATH) as json_file: 
        data = json.load(json_file)
    print(data, file=sys.stderr)
    return data
##########################################################################
def get_yesterday():
    """
    Import date and timdelta class from datetime module
    :return: yesterday's date
    """
    from datetime import date
    from datetime import timedelta
    # Get today's date
    today = date.today()
    # Yesterday date
    yesterday =  today - timedelta(days = 2)
    print ("yesterday = ",yesterday, file=sys.stderr)
    return yesterday.strftime('%Y%m%d')

##########################################
#def db_connect(db_path=DEFAULT_PATH):
def db_connect(db_path):
    """
    connect to the database
    :param db_path: path to the database file
    :return: database connection for further work
    """
    con = sqlite3.connect(db_path)
    return con

##########################################
def db_disconnect(con):
    """
    :param con: database connection for further work
    :return:
    """
    con.commit()
    con.close()

##########################################
def save_ytinfo(con,ytid,url,description):
    """
    Save fields from Youtube query into database
    :param con: database connect object
    :param ytid: the youtube id 
    :param url: the youtube url 
    :param description: the youtube description or title 
    :return:
    """
    sql = """
    INSERT INTO video (ytid, url,description,download) 
    VALUES (?, ?, ?,0)"""
    cur = con.cursor()
    cur.execute(sql, (ytid, url, description))
    return cur.lastrowid

##########################################
def check_if_ytid_exists(con,ytid):
    """
    Check if we have already seen this video on our database
    :param con: database connect object
    :param ytid: the youtube id 
    :return: True or False
    """
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
    """
    as the name suggests, this will check for the existence of a table
    :param con: database connect object
    :param table_name: the table we are checking for existence of 
    :return: True or False
    """
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    cur = con.cursor()
    cur.execute(sql, (table_name,))
    results = cur.fetchall()
    # if it doesn't exist, then the query returns no rows. 
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
def search_yt_(con,searchstring):
    """
    Extracts information using the "ytsearch:string" method
    :param con: database connection
    :param searchstring: search string to select videos
    :return:
    """
    resultnum = batch 

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    	# build the search string
    	# ytsearch is another waay, we want to look at recent results. 

        sstring = "ytsearchdate" + str(resultnum) + ":" + searchstring

        try:
            infoSearched = ydl.extract_info(sstring)
        except youtube_dl.utils.DownloadError: 
        	print ("can't do that one")
        	pass

    mynum = len(infoSearched['entries'])
    # Output the information that has potential to be what I am looking for
    # iterate over the results wiht J
    print ("### found ",mynum,"entries... ")
    for j in range(mynum):
        ytid = infoSearched['entries'][j]['id']
        if (check_if_ytid_exists(con,ytid) == False):
            print ('saving {} "{}"'.format(infoSearched['entries'][j]['id'], infoSearched['entries'][j]['title']))
            save_ytinfo(con,ytid, infoSearched['entries'][j]['webpage_url'], infoSearched['entries'][j]['title'])

################################################################################################
def get_yt_info_single(url):
    """
    Extracts information using the actual URL method
    """
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    infoUrlGiven = ydl.extract_info(url)

    print ("xxxx",infoUrlGiven)
    # Outputs the correct information I am looking for
    for i in infoUrlGiven:
        print ("--")
        if i == 'webpage_url' or i == 'title' or i == 'duration':
            print('\n {}    {}' .format(infoUrlGiven[str(i)], i))


################################################################################################
################################################################################################
def get_new_videos(con,ydl_opts):    
    """
    :param con: database connection
    :return"
    """
    sql = """
    SELECT * 
    FROM video
    WHERE download <> 1 
    """;
    cursor = con.cursor()
    cursor.execute(sql)


    rows = cursor.fetchall()
    print ("how many rows",len(rows),file=sys.stderr)
    for row in rows:
        download_video(con,row,ydl_opts)

###################################################/
def download_video(con,row,ydl_opts):
    """
    get a video into the media directoriy
    :param row: list from one row of a found video. 
    :param mediadir: Media directory to download
    """
    download_dir = "./media"
    if ( os.path.isdir(download_dir) == False):
        os.mkdir(download_dir)

    os.chdir("./media")
    title = row[0] # youtube title
    ytid = row[1] # youtube id
    url = row[2] # youtube url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    update_download(con,ytid)

    print(row)
    return True # we downloaded successfully 

##########################################
def update_download(con,ytid):
    """
    Set the download field to 1 to signify we've downloaded this. 
    :param con: database connect object
    :param ytid: the youtube id 
    :param url: the youtube url 
    :param description: the youtube description or title 
    :return:
    """
    sql = """
    UPDATE video 
    SET download = 1 
    WHERE ytid = ?"""
    print ("sql: ",sql)
    print ("ytid: ",ytid)
    cur = con.cursor()
    cur.execute(sql, (ytid,))
    con.commit()

################################################################################################
def create_video_table():    
    """
    If no video table exists, here is the SQL to create it. With this we can just 
    create a new database and just start stashign.
    """
    print("create table")
    table_create_sql = """
    CREATE TABLE video(
        description text, 
        url text not null, 
        ytid text not null, 
        download int )""";