# type: ignore
# pylint: skip-file
#edited but source is: https://github.com/TGSP1997/MOT16_Annotator/https://github.com/khalidw/MOT16_Annotator
import cv2

# Click on one corner of the image,
# then, click on the other corner on the image.
# The coordinates will be saved in gt/gt.txt
from pathlib import Path
# Press 'esc' to quit
# Press 'n' for next frame


sequence_name = 'Sequence05_2020-01-01_00-00-00'
img_folder = Path(f'./Sequences/test/{sequence_name}/img1')
# Create a folder "det" for the detections in the same location as input video:
path_to_detection_folder = Path(f'./Sequences/test/{sequence_name}/gt')
new_path = path_to_detection_folder.joinpath('gt.txt')

if not path_to_detection_folder.is_dir():
  raise ValueError('no such folder exists')

list_of_imgs = []
for file in img_folder.glob(f'*.jpeg'):
    list_of_imgs.append(file)
len_list_of_images = len(list_of_imgs)
#mouse callback function
global click_list
global positions
positions, click_list = [], []

def callback(event, x, y, flags, param):
    if event == 1: click_list.append((x,y))
    if event == 2: click_list.clear()
    positions.append((x,y))    
    
cv2.namedWindow('img')
cv2.setMouseCallback('img', callback)
image_number = 0

frame_number = 1
object_id = 1 # cannot be 0 or negative

#read first image
img_p = cv2.imread(list_of_imgs[0].as_posix())

# get width and height of the original frame
h, w, _ = img_p.shape

# calculate resize factor, this will be used to correct the bounding boxes
# as we are drawing them on a resized scale
rf_w = w/1280 # original fame width / rescaled width
rf_h = h/720 # original fame height / rescaled height

img_p = cv2.resize(img_p, (1280,720))
index = 0
print(f'Bild: {index+1}/{len_list_of_images}')
with open(new_path.as_posix(),'w') as out_file:

  while True:
    img = img_p.copy()
    if len(positions)>1:
      movement = positions[-1]
      cv2.line(img, (movement[0]-w,movement[1]), (movement[0]+w,movement[1]), (102,102,255), 1)
      cv2.line(img, (movement[0],movement[1]-h), (movement[0],movement[1]+h), (102,102,255), 1)
    if len(click_list)>0:

      mouse_position = positions[-1]
      #horizontal high left to right
      a = click_list[-1][0], click_list[-1][1]
      b = mouse_position[0], click_list[-1][1]
      cv2.line(img, a, b, (123,234,123), 3)
      #horizontal low left to right
      a = click_list[-1][0], mouse_position[1]
      b = mouse_position[0], mouse_position[1]
      cv2.line(img, a, b, (123,234,123), 3)
      #vertical right high to low
      a = mouse_position[0], click_list[-1][1]
      b = mouse_position[0], mouse_position[1]
      cv2.line(img, a, b, (123,234,123), 3)
      #vertical left high to low
      a = click_list[-1][0], mouse_position[1]
      b = click_list[-1][0], click_list[-1][1]
      cv2.line(img, a, b, (123,234,123), 3)


    # If there are four points in the click list, save the image
    if len(click_list) == 2:

      #get the top left and bottom right
      a,b  = click_list

      #with open('%s/det.txt'%(new_path),'w') as out_file:
      # MOT 16 det,tx format
      # frame id, -1, xmin, ymin, width, height, confidence, -1, -1, -1
      # as our detections are manual, we will set confidence score as 1
      xmin = min(a[0],b[0])*rf_w
      ymin = min(a[1],b[1])*rf_h
      xmax = max(a[0],b[0])*rf_w
      ymax = max(a[1],b[1])*rf_h
      width = xmax-xmin
      height = ymax-ymin
      print('%d,%d,%.2f,%.2f,%.2f,%.2f,1,1,-1,-1'%(frame_number,object_id,xmin,ymin,width,height),file=out_file)
      print(f"{frame_number}, {object_id}, {xmin}, {ymin}, {width}, {height}, 1, 1, -1, -1")

      #reset the click list
      click_list = []

    # show the image and wait
    cv2.imshow('img', img)
    k = cv2.waitKey(1)
    # escape if 'esc' is pressed
    # 27 is the ascii code for 'esc'
    if k == 27: break

    # read next image if 'n' is pressed
    # 110 is the ascii code for 'n'
    if k == 110:
      index+=1
      frame_number += 1
      try:
        img = cv2.imread(list_of_imgs[index].as_posix())
      except IndexError:
        print('Error: lade letztes Bild aus Array')
        img = cv2.imread(list_of_imgs[-1].as_posix())
        index = len_list_of_images-1
        frame_number= len_list_of_images
      img_p = cv2.resize(img, (1280,720))
      print(f'Bild: {index+1}/{len_list_of_images}')
    
    if k == 118: #ascii for v
      index -=1
      frame_number -= 1
      try:
        if index<0:
           raise IndexError
        img = cv2.imread(list_of_imgs[index].as_posix())
      except IndexError:
        print('Error: lade erstes bild aus Array')
        img = cv2.imread(list_of_imgs[0].as_posix())
        index = 0
        frame_number= 1
      img_p = cv2.resize(img, (1280,720))
      print(f'Bild: {index+1}/{len_list_of_images}')
    # code to increment object id
    # press 'i' to increment object ID
    # 105 is ascii code for 'i'
    if k == 105:
          object_id += 1
          print("object_id incremented to %d" %(object_id))
      
    # code to increment object id
    # press 'd' to increment object ID
    # 100 is ascii code for 'd'
    if k == 100:
          object_id -= 1
          print("object_id decremented to %d" %(object_id))


cv2.destroyAllWindows()
