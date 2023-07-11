"""
Checks all generated tracker txt for empty lines
as they cannot be interpreted by evaluation scripts
"""


from pathlib import Path



def check_for_empty_lines(sequence_name: str) -> None:
    """Opens and rewrite each tracker txt without empty lines

    Args:
        sequence_name (str): Sequence Name
    """
    for tracker in ['track_deep', 'track_ctkal', 'track_viou', 'track_iou']:
        with open(
            Path(f'./Sequences/test/{sequence_name}/track/{tracker}.txt').as_posix(),
            'r+',
            encoding = 'utf-8'
        ) as input_file:
            lines = input_file.readlines()
            # move file pointer to the beginning of a file
            input_file.seek(0)
            input_file.truncate()
            for line in lines:
                if line !='\n':
                    input_file.write(line)
