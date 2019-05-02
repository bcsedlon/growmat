#!/bin/sh

echo "growmat"

cp /home/pi/growmat/db.sqlite3 /home/pi/growmat/growmat/ramdisk/db.sqlite3

nohup python2 /home/pi/growmat/growmat/manage.py modbus &
nohup python2 /home/pi/growmat/growmat/manage.py archive &
nohup python2 /home/pi/growmat/growmat/manage.py runserver 0.0.0.0:8000 > /dev/null &

#nohup fswebcam -c /etc/fswebcam.conf &
