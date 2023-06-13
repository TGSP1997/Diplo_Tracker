import argparse
from pathlib import Path
import cv2


def video_to_img(
    video_file: Path,
    output_path: Path,
    name: str,
    frame_rate: int,
    format_type: str
) -> None:
    '''
    Converts a video to img-sequence
    '''
    save_img_folder = output_path.joinpath(name)
    if not save_img_folder.is_dir():
        save_img_folder.mkdir(parents=True)
    vidcap = cv2.VideoCapture(video_file.as_posix())
    def get_frame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        has_frames,image = vidcap.read()
        if has_frames:
            cv2.imwrite(save_img_folder.joinpath(f'{count:06d}.{format_type}').as_posix(), image)
        return has_frames
    sec = 0
    count=1
    success = get_frame(sec)
    while success:
        count = count + 1
        sec = sec + float(1/frame_rate)
        sec = round(sec, 2)
        success = get_frame(sec)


def img_to_video(
    img_folder: Path,
    output_path: Path,
    name: str,
    frame_rate: int,
    format_type: str
) -> None:
    '''
    Converts a img-sequence to video
    '''
    if not img_folder.is_dir():
        raise ValueError('NO FOULDER FOUND')
    list_of_imgs = []
    for file in img_folder.glob(f'*.{format_type}'):
        list_of_imgs.append(file)
    if len(list_of_imgs) == 0:
        raise ValueError(f'NO PICTURES WITH FORMAT {format_type.upper()} FOUND INSIDE IMG-FOLDER')
    frame = cv2.imread(list_of_imgs[0].as_posix())
    video =cv2.VideoWriter(
        output_path.joinpath(f'{name}.mp4').as_posix(),
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps=frame_rate,
        frameSize= (
            frame.shape[1],
            frame.shape[0]
        )
    )
    for image in list_of_imgs:
        video.write(cv2.imread(image.as_posix()))

    cv2.destroyAllWindows()
    video.release()


def parse(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Converts video to img-sequence or img-sequence to video file'
    )
    parser.add_argument(
        "--img_folder",
        nargs="+",
        type=str,
        help="Path to img_folder",
        required=False,
        default=False
    )
    parser.add_argument(
        "--video_file",
        nargs="+",
        type=str,
        help="Path to video file",
        required=False,
        default=False
    )
    parser.add_argument(
        "--output_path",
        nargs="+",
        type=str,
        help="Outputpath to write imgages or video",
        required=True
    )
    parser.add_argument(
        "--fps",
        nargs="+",
        type=str,
        help="Framerate of video or  img-sequence",
        required=False,
        default = ['20']
    )
    parser.add_argument(
        "--name",
        nargs="+",
        type=str,
        help="Name for video or img-folder to save",
        required=True
    )
    parser.add_argument(
        "--format_type",
        nargs="+",
        type=str,
        help="Format type of img",
        required=False,
        default=['jpg']
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse(argv)
    if args.video_file == args.img_folder:
        raise ValueError('You need to choose one input. Either --video_file or --img_folder')
    if args.video_file:
        video_to_img(
            Path(args.video_file[0]),
            Path(args.output_path[0]),
            str(args.name[0]),
            int(args.fps[0]),
            str(args.format_type[0])
        )
    if args.img_folder:
        img_to_video(
            Path(args.img_folder[0]),
            Path(args.output_path[0]),
            str(args.name[0]),
            int(args.fps[0]),
            str(args.format_type[0])
        )


if __name__ == "__main__":
    main()
