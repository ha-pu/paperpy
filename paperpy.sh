#!/bin/sh

cd /home/pi/paperpy
rclone move --verbose --log-file=logs/rclone.log dropbox:Privat/PaperPyIn files_new
. paperpy/bin/activate
python3 paper.py >> logs/paperpy.log 2>&1
rclone move --verbose --log-file=logs/rclone.log files_old dropbox:Privat/PaperPyOut
