from classes.helpers.create_folder_structure import create_folder_structure
from classes.helpers.convert_img_and_video_files import img_to_video
from pathlib import Path

sequence_names,fr_list, _ = create_folder_structure()

for i in range (0,17):
    print(i)
    # img_folder = Path(f'./Sequences/test/{sequence_names[i]}/img1')
    # list_of_imgs = []
    # for file in img_folder.glob(f'*.jpeg'):
    #     list_of_imgs.append(file)
    # count = 1
    # for image in list_of_imgs:
    #     image.rename(f'./Sequences/test/{sequence_names[i]}/img1/{count:06d}.jpeg')
    #     count+=1
