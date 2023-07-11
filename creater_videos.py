from classes.helpers.create_folder_structure import create_folder_structure
from classes.helpers.convert_img_and_video_files import img_to_video
from pathlib import Path

sequence_names,fr_list, _ = create_folder_structure()

for i in range (0,17):
    print(sequence_names[i],fr_list[i])

    