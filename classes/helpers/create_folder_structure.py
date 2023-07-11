"""
Helper to create the needed Folder Structure
"""


from pathlib import Path
from typing import Tuple
import json

def create_folder_structure() -> Tuple[list,list,list]:
    """Creates the needed folder structure from the Sequence_list.json
    return sequence_names, fr_list, total_frames_list
    """
    with open("./Sequence_list.json", 'r', encoding = 'utf-8') as json_file:
        structure = json.load(json_file)
    sequence_names = []
    fr_list = []
    total_frames_list = []
    #json_structure: name,frame_rate,total,frames
    for sequence_arr in structure["Sequences"]:
        sequence_names.append(sequence_arr[0])
        fr_list.append(sequence_arr[1])
        total_frames_list.append(sequence_arr[2])
        Path("./Sequences/test", f"{sequence_arr[0]}",'det').mkdir(parents = True, exist_ok = True)
        Path("./Sequences/test", f"{sequence_arr[0]}",'img1').mkdir(parents = True, exist_ok = True)
        Path("./Sequences/test", f"{sequence_arr[0]}",'otc').mkdir(parents = True, exist_ok = True)
        Path(
            "./Sequences/test", f"{sequence_arr[0]}",'track').mkdir(parents = True, exist_ok = True
        )
        Path(
            "./Sequences/test", f"{sequence_arr[0]}",'video').mkdir(parents = True, exist_ok = True
        )
        Path("./Sequences/test", f"{sequence_arr[0]}",'gt').mkdir(parents = True, exist_ok = True)

    return sequence_names, fr_list, total_frames_list
