#!/bin/sh

echo "growmat"

cp ./db.sqlite3 ./ramdisk/db.sqlite3
 

nohup python ./growmat/manage.py modbus &
#nohup python ./growmat/manage.py archive &
nohup python ./growmat/manage.py runserver 0.0.0.0:80 > /dev/null &

#nohup fswebcam -c /etc/fswebcam.conf &
