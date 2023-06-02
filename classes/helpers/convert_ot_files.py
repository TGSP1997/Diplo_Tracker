import argparse
from pathlib import Path
from OTVision.helpers.files import read_json


def write_txt_from_otdet(
    otdtet_file: Path,
    output_path: Path
) -> None:
    '''
    Converts "otdet" to MOTChallenge "txt" file.
    Layout:frame, id(-1), bb_left, bb_top, bb_width, bb_height, conf, x(-1) ,y(-1) ,z(-1)
    '''
    if not otdtet_file.is_file:
        raise ValueError('NO OTDET FILE FOUND')
    allowed_classes = ["car","motorcycle","bus","train","truck"]
    ot_dict = read_json(otdtet_file)
    txt_lines = ''
    for frame, detections in ot_dict['data'].items():
        for detection in detections['detections']:
            if detection['class'] not in allowed_classes:
                continue
            bb_left = float(detection["x"]) - (float(detection["w"])/2)
            bb_top = float(detection["y"]) - (float(detection["h"])/2)
            txt_lines += (
                f'{frame},-1,{bb_left},{bb_top},'
                f'{detection["w"]},{detection["h"]},'
                f'{detection["confidence"]},-1,-1,-1\n'
            )

    with open(
        #output_path.joinpath(ot_dict['metadata']['video']['filename']+'.txt'),
        output_path.joinpath('det.txt'),
        'w',
        encoding = 'utf-8'
    ) as text_file:
        text_file.write(txt_lines)

def write_ottrk_from_txt(

) -> None:
    print('neu hier')
    # stamped_detections = add_timestamps(detections_video, video_file)
    #         write_json(
    #             stamped_detections,
    #             file=detections_file,
    #             filetype=CONFIG[DEFAULT_FILETYPE][DETECT],
    #             overwrite=overwrite,
    #         )


def parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Converts "otdet" to MOTChallenge "txt" file')
    parser.add_argument(
        "--otdet_file",
        nargs="+",
        type=str,
        help="Path to otdet-file",
        required=False
    )
    parser.add_argument(
        "--output_path",
        nargs="+",
        type=str,
        help="Outputpath to write txt-file",
        required=False
    )
    parser.add_argument(
        "--write_txt_from_otdet",
        nargs="+",
        type=bool,
        help="Bool to choose function",
        required=False,
        default=False
    )
    parser.add_argument(
        "--write_ottrk_from_txt",
        nargs="+",
        type=bool,
        help="Bool to choose function",
        required=False,
        default=False
    )
    return parser.parse_args(argv)

def main(argv: list[str] | None = None):
    args = parse(argv)
    if args.write_ottrk_from_txt == args.write_txt_from_otdet:
        raise ValueError('You need to choose one function. See --help')
    if args.write_txt_from_otdet:
        if not args.otdet_file and not args.output_path:
            raise ValueError('Need to define --otdet_file and --output_path')
        write_txt_from_otdet(
            Path(args.otdet_file[0]),
            Path(args.output_path[0])
        )
    if args.write_ottrk_from_txt:
        write_ottrk_from_txt(

        )


if __name__ == "__main__":
    main()
