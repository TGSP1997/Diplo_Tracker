#oriented from https://github.com/TGSP1997/multi-object-tracker/blob/master/examples/example_notebooks/mot_YOLOv3.ipynb
import csv
import numpy as np
from pathlib import Path
import time
from functools import wraps
from typing import Optional
from motrackers import CentroidTracker as ct
from motrackers import CentroidKF_Tracker as ctkal
from .helpers.convert_ot_files import write_txt_from_otdet, write_ottrk_from_txt








def timeit(func):
    """
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    Decorator to calculate runtime of specific class function
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        write_txt_from_otdet(
            args[0].otdet_path,
            Path("./Sequences/test", args[0].sequence_name,"det")
        )
        time.sleep(1)
        try:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            # first item in the args, ie `args[0]` is `self`
            print(f'Function {func.__name__}{args} Took {total_time:.4f} seconds')
        finally:
            time.sleep(1)
            #TODO
            #write_ottrk_from_txt()
        return result
    return timeit_wrapper


class CentroidTracker:
    """
    Represents already implemented CentroidTracker as for better use in OOP    
    """
    def __init__(
        self,
        sequence_name:str,
        max_lost: int,
        with_kalman: bool = False,
        centroid_distance_threshold: Optional[int] = 30.,
        process_noise_scale: Optional[float] = 1.0,
        measurement_noise_scale: Optional[float] = 1.0,
        time_step: Optional[int] = 1

    ) -> None:
        """
        Creates Class with needed parameters needed for Centroid TRacker
        Definition copied from CentroidTRacker
        Args:
            sequence_name (str): Name of Sequence0X 
            max_lost (int): Maximum number of consecutive frames object was not detected.
            with_kalman (bool): Choose to use Centroid with Kalman Filter
        """
        self.otdet_path = Path("./Sequences/test", sequence_name, "otc", f"{sequence_name}.otdet")
        self.sequence_name = sequence_name
        self.tracker = ct(max_lost, tracker_output_format='mot_challenge')
        self.with_kalman = with_kalman
        if with_kalman:
            self.tracker = ctkal(
                max_lost = max_lost,
                tracker_output_format='mot_challenge',
                centroid_distance_threshold=centroid_distance_threshold,
                time_step=time_step,
                process_noise_scale=process_noise_scale,
                measurement_noise_scale=measurement_noise_scale
            )
        self.frame_count = len(list(Path("./Sequences/test", sequence_name, "img1").glob('*')))

    @timeit
    def run(self):
        tracker_type = "ct"
        if self.with_kalman:
            tracker_type = "ctkal"
        with open(
            Path("./Sequences/test/",self.sequence_name,"track",f"track_{tracker_type}.txt").as_posix(),
            'w',
            encoding='utf-8'
        ) as csv_output:
            writer = csv.writer(csv_output,delimiter=",")

            for frame_number in range(1,self.frame_count+1):
                bboxes, confidences, class_ids = self.get_elements(frame_number)
                tracks = self.tracker.update(bboxes, confidences, class_ids)
                for track in tracks:
                    writer.writerow(track)

    def get_elements(self, frame_number):
        with open(
            Path("./Sequences/test/",self.sequence_name,"det","det.txt").as_posix(),
            'r',
            encoding='utf-8'
        ) as csv_file:
            lister = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                lister.append(row)
        class_ids = []
        boxes = []
        scores = []
        for element in lister:
            if element[0]==str(frame_number):
                class_ids.append(2)
                scores.append(float(element[6]))
                boxes.append(
                    [float(element[2]),float(element[3]),float(element[4]),float(element[5])]
                )
                
        return np.array(boxes), scores,  class_ids



if __name__ == "__main__":
    obj= CentroidTracker(
        sequence_name="Car",
        max_lost=10
    )
    obj.run()
