from pathlib import Path
import json

def create_folder_structure():
    with open("./Sequence_list.json",'r', encoding='utf-8') as json_file:
        structure=json.load(json_file)

    for sequence in structure["Sequences"]:
        Path("./Sequences/test", f"{sequence}",'det').mkdir(parents=True, exist_ok=True)
        Path("./Sequences/test", f"{sequence}",'img1').mkdir(parents=True, exist_ok=True)
        Path("./Sequences/test", f"{sequence}",'otc').mkdir(parents=True, exist_ok=True)
        Path("./Sequences/test", f"{sequence}",'track').mkdir(parents=True, exist_ok=True)
        Path("./Sequences/test", f"{sequence}",'video').mkdir(parents=True, exist_ok=True)