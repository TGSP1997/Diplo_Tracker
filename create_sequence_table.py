from pathlib import Path
from pymediainfo import MediaInfo # type: ignore[import]
import csv

cutted_folder = Path(r'C:\Users\Sandro\Desktop\too_watch\cutted')
to_write = []
to_write.append(['Ordner','Name','Dauer in Sekunden','Maße','Framerate', 'Total Frames', 'Dauer Eigenschaft', 'Eigenschaft'])
for file in cutted_folder.glob('**/*.mp4'):
    media_info =  MediaInfo.parse(file.as_posix())
    for track in media_info.tracks:
        if track.track_type == "Video":
            fps = track.frame_rate
            length = track.duration/1000
            width = track.width
            height = track.height
            to_write.append([f'{file.parent.parts[-1]}',f'{file.name}', f'{length}', f'{width}x{height}', f'{fps}',  f'{int(float(fps)*length)}','',''])

with open(r'./cutted_sequence_table.csv', 'w', encoding='latin-1',newline='') as outfile:
    csv.excel.delimiter=';'
    writer = csv.writer(outfile, dialect=csv.excel)
    for line in to_write:
        writer.writerow(line)