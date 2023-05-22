import json
import bz2
import csv
 
with bz2.open('./Sequences/test/Car/otc/Car_iou.ottrk','r') as track_file2:
    read_file = json.loads(track_file2.readlines()[0])
txt_lines=''
for detection in read_file['data']['detections']:
    bb_left = float(detection["x"]) - (float(detection["w"])/2)
    bb_top = float(detection["y"]) - (float(detection["h"])/2)
    txt_lines+=(f'{detection["frame"]},{detection["track-id"]},{bb_left},{bb_top},{detection["w"]},{detection["h"]},1,-1,-1,-1\n')

with open(
    './Sequences/test/Car/track/track_iou.txt',
    'w',
    encoding = 'utf-8'
) as text_file:
    text_file.write(txt_lines)