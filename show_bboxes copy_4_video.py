import cv2
import csv
from pathlib import Path
from typing import List
import numpy as np


def get_track_data_and_id(sequence_name: str, track_names: List[str]):
    track_data_dict = {}
    max_id_dict = {}
    #load trackfiles into dict
    for track_name in track_names:
        track_file = Path(f'./Sequences/test/{sequence_name}/track/{track_name}.txt')
        if track_name == 'det':
            track_file = Path(f'./Sequences/test/{sequence_name}/det/{track_name}.txt')
        if not track_file.is_file():
            raise ValueError(f'{track_name}.txt no found')
        with open(track_file.as_posix()) as csv_file:
            csv_list = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row)>0:
                    csv_list.append(row)
            track_data_dict.update({f'{track_name}': csv_list})
    
        #get the max number of ids
        max_id = 0
        for arr_element in csv_list:
            if track_name == 'det':
                max_id_dict.update({f'{track_name}': 0})
                break
            if int(arr_element[1])> max_id:
                max_id = int(arr_element[1])
        max_id_dict.update({f'{track_name}': max_id})

    return track_data_dict, max_id_dict

def _create_video_writers(sequence_name: str, track_names: List[str], output_path: Path):
    #get width and height to initialize videowriter
    fps=20
    video_writer_dict = {}
    width = cv2.imread(Path("./Sequences/test", sequence_name, "img1/000001.jpg").as_posix()).shape[1]
    height = cv2.imread(Path("./Sequences/test", sequence_name, "img1/000001.jpg").as_posix()).shape[0]
    check_length_for_4by4 = [x for x in track_names if x != "det"]
    if len(check_length_for_4by4) == 4:
        video_writer_dict = {
            'all': cv2.VideoWriter(
                output_path.joinpath(f'{sequence_name}_all.mp4').as_posix(),
                cv2.VideoWriter_fourcc(*'mp4v'),
                fps=fps,
                frameSize= (
                    width*2,
                    height*2
                )
            )
        }
    for track_name in track_names:
        video_writer_dict.update(
            {
                f'{track_name}': cv2.VideoWriter(
                    output_path.joinpath(f'{sequence_name}_{track_name}.mp4').as_posix(),
                    cv2.VideoWriter_fourcc(*'mp4v'),
                    fps=fps,
                    frameSize= (
                        width,
                        height
                    )
                )
            }
        )
    return video_writer_dict

def create_videos(sequence_name:str):
    track_names = ['track_deep', 'track_ctkal', 'track_viou', 'track_iou', 'det']
    track_data_dict, max_id_dict = get_track_data_and_id(
        sequence_name = sequence_name,
        track_names = track_names
    )
    output_path = Path(f'./Sequences/test/{sequence_name}/video')

    video_writer_dict = _create_video_writers(
        sequence_name=sequence_name,
        track_names=track_names,
        output_path=output_path
    )

    img_folder = Path(f'./Sequences/test/{sequence_name}/img1')

    #draw boxes on imag and save as list inclusive id and total id
    img_number = 1
    #color_selected = np.random.random(size=3) * 256
    color_selected =[]
    color_selected.append([0, 255, 255][::-1])#reversed for rgb color
    color_selected.append([0, 0, 255][::-1]) # different color for trackers
    color_selected.append([0, 255, 0][::-1])
    color_selected.append([255, 0, 0][::-1])
    color_selected.append([0, 255, 255][::-1]) #and for det.txt
    for file in img_folder.glob('*.jpg'):
        img_deep = img_ctkal = img_iou = img_viou = []
        color_count = 0
        for track_name, csv_list in track_data_dict.items():
            image_rect = None
            cv2_image = cv2.imread(file.as_posix())
            for element in csv_list:
                final_drawn_img = None
                if int(element[0]) == img_number:
                    x = float(element[2])
                    y = float(element[3])
                    w = float(element[4])
                    h = float(element[5])

                    x_start = int(x)
                    y_start = int(y)
                    x_end = int(x+w)
                    y_end = int(y+h)
                    max_id = 0
                    for key, value in max_id_dict.items():
                        if key == track_name:
                            max_id = value
                            if track_name == 'track_ctkal': # because it starts at 0
                                max_id+=1
                    
                    image_rect = cv2.rectangle(cv2_image,(x_start, y_start), (x_end, y_end), color_selected[color_count],2)
                    if track_name == 'det':
                        image_text = cv2.putText(image_rect, f'{"{:1.2f}".format(float(element[6]))}', (int(x_start), int(y_start)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_selected[color_count], 2)
                    else:
                        image_text = cv2.putText(image_rect, f'{element[1]}', (int(x_start), int(y_start)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_selected[color_count], 2)
                    image_text2 = cv2.putText(image_text, f'Total-ID`s: {max_id}: {track_name}', (int(image_rect.shape[1]/8), image_rect.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_selected[color_count], 2)
                    final_drawn_img = image_text2
                    
                    match track_name:
                        case 'track_deep':
                            img_deep = final_drawn_img
                        case 'track_ctkal':
                            img_ctkal = final_drawn_img
                        case 'track_viou':
                            img_viou= final_drawn_img
                        case 'track_iou':
                            img_iou = final_drawn_img
                        case 'det':
                            img_det = final_drawn_img

            if final_drawn_img is None:
                match track_name:
                    case 'track_deep':
                        img_deep = cv2_image
                    case 'track_ctkal':
                        img_ctkal = cv2_image
                    case 'track_viou':
                        img_viou= cv2_image
                    case 'track_iou':
                        img_iou = cv2_image
                    case 'det':
                        img_det = cv2_image
            color_count+=1

        
        for tracker_name, writer in video_writer_dict.items():
            match tracker_name:
                case 'track_deep':
                    writer.write(img_deep)
                case 'track_ctkal':
                    writer.write(img_ctkal)
                case 'track_viou':
                    writer.write(img_viou)
                case 'track_iou':
                    writer.write(img_iou)
                case 'det':
                    writer.write(img_det)
                case 'all':
                    img_to_writ_obere_reihe = np.concatenate((img_deep, img_ctkal), axis=1)
                    img_to_writ_untere_reihe = np.concatenate((img_iou, img_viou), axis=1)
                    img_all = np.concatenate((img_to_writ_obere_reihe, img_to_writ_untere_reihe), axis=0)
                    writer.write(img_all)
            


        img_number+=1

if __name__ == '__main__':
    #create_videos('Car')
    create_videos('Car02')