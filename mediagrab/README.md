#MediaGrab

- download youtube videos based on keyword
- stash statuses in a mongodb and avoid downloading the same video multiple times



# 
# m h  dom mon dow   command
#10,20,30,40,50,00 5 * * 1 tar -zcf /var/backups/homei_`date '+%Y%m%d'`.tgz /home/rca/Projects
00,20,40 * * * * /usr/bin/python3 /home/pi/Running/mediagrab/ytsearch.py  -k 'covid' -d covid.sqlite3 -b 20 > /var/log/mediagrab/ytsearch_covid_` /bin/date '+\%Y\%m\%d-\%H\%M'`.log 2>&1
iagrab/ytsearch.py -k 'gaetz' -d gaetz.sqlite3  -b 20 > /var/log/mediagrab/ytsearch_gaetz_` /bin/date '+\%Y\%m\%d-\%H\%M'`.log 2>&1
#0 9 * * *  pip3 install --upgrade youtube-dl
