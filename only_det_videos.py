from classes.helpers.convert_ot_files import write_txt_from_otdet
from classes.helpers.create_videos import create_videos
from classes.helpers.create_folder_structure import create_folder_structure
from pathlib import Path

sequence_names, fr_list, _ = create_folder_structure()

for i in range (0,len(sequence_names)):
    write_txt_from_otdet(
                Path("./Sequences/test", sequence_names[i], "otc", f"{sequence_names[i]}.otdet"),
                Path("./Sequences/test", sequence_names[i],"det")
            )
    create_videos(sequence_name=sequence_names[i], fps=fr_list[i], track_names=['det'])