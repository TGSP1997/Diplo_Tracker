import cv2
import csv
from pathlib import Path
import time
import numpy as np
#variables
sequence_name = 'Bus'
track_name = 'track_deep'
fps=20
#read images and save as list
img_folder = Path("./Sequences/test", sequence_name, "img1")
list_of_imgs = []
for file in img_folder.glob('*.jpg'):
    list_of_imgs.append(file)

#read track file and save as list
track_file = Path("./Sequences/test", sequence_name, "track",f'{track_name}.txt')
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
list_cv2_image = []
for image in list_of_imgs:
    cv2_image = cv2.imread(image.as_posix())
    list_cv2_image.append(cv2_image)

#create random colours to choose for each id
color_list = []
for i in range(0,max_id+1):
    color_list.append(list(np.random.random(size=3) * 256))

#draw boxes on imag and save as list inclusive id and total id
drawn_list_cv2_image = []
img_number = 1
for to_draw_image in list_cv2_image:
    add_to_list=False
    image_rect = None
    for element in csv_list:
        if int(element[0]) == img_number:
            x = float(element[2])
            y = float(element[3])
            w = float(element[4])
            h = float(element[5])

            x_start = int(x)
            y_start = int(y)

            x_end = int(x+w)
            y_end = int(y+h)

            image_rect = cv2.rectangle(to_draw_image,(x_start, y_start), (x_end, y_end), color_list[int(element[1])],2)
            image_text = cv2.putText(image_rect, f'{element[1]}', (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_list[int(element[1])], 2)
            image_text2 = cv2.putText(image_text, f'Total-ID`s: {max_id}', (int(image_rect.shape[1]/8), image_rect.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            add_to_list = True
    if add_to_list:
        drawn_list_cv2_image.append(image_text2)
    img_number+=1



#show video in loop until press q
loop=True
while loop:
    for img_cv2 in drawn_list_cv2_image:
        cv2.imshow('Frame',img_cv2)
        #time.sleep(0.01)
        key = cv2.waitKey(20) & 0xFF
        if key == ord('q'):
            loop = False
            break

video =cv2.VideoWriter(
    Path("./Sequences/test", sequence_name, "video").joinpath(f'{sequence_name}_{track_name}.mp4').as_posix(),
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps=fps,
    frameSize= (
        list_cv2_image[0].shape[1],
        list_cv2_image[0].shape[0]
    )
)
for to_write_img in drawn_list_cv2_image:
    video.write(to_write_img)
cv2.destroyAllWindows()
