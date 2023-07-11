"""
Helper to convert OpenTraffic Files from current state of the fork
"""


import bz2
import json
from pathlib import Path
from OTVision.helpers.files import read_json # type: ignore[import]


def write_txt_from_otdet(
    otdtet_file: Path,
    output_path: Path
) -> None:
    """Converts "otdet" to MOTChallenge "txt" file.
    Layout: frame, id(-1), bb_left, bb_top, bb_width, bb_height, conf, x(-1) ,y(-1) ,z(-1)

    Args:
        otdtet_file (Path):Path to otdet file
        output_path (Path):Path to save file

    """
    if not otdtet_file.is_file():
        raise ValueError('NO OTDET FILE FOUND')
    allowed_classes = ["car", "motorcycle", "bus", "train", "truck"]
    ot_dict = read_json(otdtet_file)
    txt_lines = ''
    for frame, detections in ot_dict['data'].items():
        for detection in detections['detections']:
            if detection['class'] not in allowed_classes:
                continue
            bb_left = float(detection["x"])
            bb_top = float(detection["y"])
            txt_lines += (
                f'{frame},-1,{bb_left},{bb_top},'
                f'{detection["w"]},{detection["h"]},'
                f'{detection["confidence"]},-1,-1,-1\n'
            )

    with open(
        output_path.joinpath('det.txt'),
        'w',
        encoding = 'utf-8'
    ) as text_file:
        text_file.write(txt_lines)


def write_txt_from_ottrk(
        ottrk_file: Path,
        txt_file: Path
) -> None:
    """Writes txt file from ottrk format

    Args:
        ottrk_file (Path): Path to ottrk file
        txt_file (Path): Path to write txt file
    """
    with bz2.open(ottrk_file.as_posix(),'r') as track_file2:
        read_file = json.loads(track_file2.readlines()[0])
    txt_lines = ''
    for detection in read_file['data']['detections']:
        bb_left = float(detection["x"])
        bb_top = float(detection["y"])
        txt_lines += (
            f'{detection["frame"]},{detection["track-id"]},{bb_left},{bb_top},{detection["w"]},'
            f'{detection["h"]},1,-1,-1,-1\n'
        )

    with open(
        txt_file.as_posix(),
        'w',
        encoding = 'utf-8'
    ) as text_file:
        text_file.write(txt_lines)


def write_ottrk_from_txt(

) -> None:
    """_summary_
    """
    print('neu hier')
    # stamped_detections = add_timestamps(detections_video, video_file)
    #         write_json(
    #             stamped_detections,
    #             file=detections_file,
    #             filetype=CONFIG[DEFAULT_FILETYPE][DETECT],
    #             overwrite=overwrite,
    #         )
