# moviegrab.py - based on the content of a sqlite db, download youtube videoso

import sqlite3

import youtube_dl


def yt_getinfo():

	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

	with ydl:
	    result = ydl.extract_info(
	        'http://www.youtube.com/watch?v=BaW_jenozKc',
	        download=False # We just want to extract the info
	    )

	if 'entries' in result:
	    # Can be a playlist or a list of videos
	    video = result['entries'][0]
	else:
	    # Just a video
	    video = result

	print(video)
	video_url = video['url']
	print(video_url)












conn = sqlite3.connect('example.db')
c = conn.cursor()

#c.execute("""create table video(
#	description text, 
#	url text not null 
#	);
 #""")
c.execute("""SELECT * from video """)

#print(c.fetchall())




ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

with ydl:
    result = ydl.extract_info(
        'http://www.youtube.com/watch?v=BaW_jenozKc',
        download=False # We just want to extract the info
    )

if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

#print(video)
for key, value in video.items():
    print(key, ' : ', value)
video_url = video['webpage_url']
print(video_url)