#!/bin/bash

tempfile=$(mktemp)
youtube_dl_log=$(mktemp)

#youtube-dl -j "ytsearch5:$*" > $tempfile
youtube-dl -j "ytsearchdate20:$*" > $tempfile

# workaround for lack of mapfile in bash < 4
# https://stackoverflow.com/a/41475317/6598435
while IFS= read -r line
do
    youtube_urls+=("$line")
    #echo sqlite3 example.db "insert into video (url,status) values ("$line",0);"
    cmd="select * from video WHERE url = \"$line\";"
    val=`sqlite3 example.db "$cmd"|wc -l`
    # if val is anything other than 0, then we already have it in the db
    if [ $val == 0 ]
    then
	    echo "insert $line"
        sqlite3 example.db "insert into video (url) values (\"$line\");"
    fi

done < <(cat $tempfile | jq '.webpage_url' | tr -d '"' )
# # for bash >= 4
# mapfile -t youtube_urls < <(cat $tempfile | jq '.webpage_url' | tr -d '"' i)

cat $tempfile | jq '.fulltitle'

