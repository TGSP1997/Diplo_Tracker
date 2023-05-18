import re
START_DATE = "start_date"
FILE_NAME_PATTERN = r".*(?P<start_date>\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\..*"
name_list = [
    'Testvideo_Cars-Cyclist_FR20_2020-01-01_00-00-00.mp4',#correct
    'Cars.mp4',#false
    'Cars_2020-01-01.mp4',#false
    'Cars_2020-01-01_00-00-00.mp4'#correct
]
for video_file in name_list:
    match = re.search(
                FILE_NAME_PATTERN,
                video_file,
            )
    print(match)