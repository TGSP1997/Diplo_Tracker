import cv2
import csv
from pathlib import Path
import time
import numpy as np
#variables
sequence_name = 'Car'
track_name = 'track_deep'
fps=20
#read images and save as list
img_folder = Path("./Sequences/test", sequence_name, "img1")
list_of_imgs = []



#read track file and save as list
track_file = Path("./Sequences/test", sequence_name, "track",f'{track_name}.txt')
#track_file = Path("./Sequences/test", sequence_name, "det",'det.txt')
with open(track_file.as_posix()) as csv_file:
    csv_list = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        csv_list.append(row)

#get the max number of ids
max_id = 0
for arr_element in csv_list:
    if int(arr_element[1])> max_id:
        max_id = int(arr_element[1])

#create list of images read into cv2



#create random colours to choose for each id
color_list = []
for i in range(1,max_id+5):
    color_list.append(list(np.random.random(size=3) * 256))

video =cv2.VideoWriter(
    Path("./Sequences/test", sequence_name, "video").joinpath(f'{sequence_name}_{track_name}.mp4').as_posix(),
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps=fps,
    frameSize= (
        cv2.imread(Path("./Sequences/test", sequence_name, "img1/000001.jpg").as_posix()).shape[1],
        cv2.imread(Path("./Sequences/test", sequence_name, "img1/000001.jpg").as_posix()).shape[0]
    )
)
#draw boxes on imag and save as list inclusive id and total id
drawn_list_cv2_image = []
img_number = 1

for file in img_folder.glob('*.jpg'):

    add_to_list=False
    image_rect = None
    cv2_image = cv2.imread(file.as_posix())
    write = False
    for element in csv_list:
        img_to_write = None
        if int(element[0]) == img_number:
            x = float(element[2])
            y = float(element[3])
            w = float(element[4])
            h = float(element[5])

            x_start = int(x)
            y_start = int(y)

            x_end = int(x+w)
            y_end = int(y+h)

            image_rect = cv2.rectangle(cv2_image,(x_start, y_start), (x_end, y_end), color_list[int(1)],2)
            image_text = cv2.putText(image_rect, f'{element[1]}', (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_list[int(1)], 2)
            image_text2 = cv2.putText(image_text, f'Total-ID`s: {max_id}', (int(image_rect.shape[1]/8), image_rect.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            img_to_writ = image_text2
            write=True

    if write:
        #print(img_to_writ)
        #print(file.as_posix())
        #cv2.imshow('figure',img_to_writ)
        #cv2.waitKey(20)
        video.write(img_to_writ)
            


    img_number+=1






