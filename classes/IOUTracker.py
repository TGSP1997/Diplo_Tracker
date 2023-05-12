from OTVision.track.track import main as tracker
from pathlib import Path
import time
from functools import wraps
import os

def timeit(func):
    """
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    Decorator to calculate runtime of specific class function
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        try:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            # first item in the args, ie `args[0]` is `self`
            print(f'Function {func.__name__}{args} Took {total_time:.4f} seconds')
        finally:
            args[0].rename()
        return result
    return timeit_wrapper


class IOUTracker:
    """
    Represents already implemented IOUTracker as for better use in OOP    
    """
    def __init__(
        self,
        sequence_name:str,
        sigma_l: float,
        sigma_h: float,
        sigma_iou: float,
        t_min: int,
        t_miss_max: int,
        overwrite: bool = True,
    ) -> None:
        """
        Creates Class with needed parameters needed for IOU Tracker
        Definition copied from OTVision
        Args:
            sequence_name (str): Name of Sequence0X 
            sigma_l (float): Lower confidence threshold. Detections with
                confidences below sigma_l are not even considered for tracking.
            sigma_h (float): Upper confidence threshold. Tracks are only
                considered as valid if they contain at least one detection with a confidence
                above sigma_h.
            sigma_iou (float): Intersection-Over-Union threshold. Two detections
                in subsequent frames are considered to belong to the same track if their IOU
                value exceeds sigma_iou and this is the highest IOU of all possible
                combination of detections.
            t_min (int): Minimum number of detections to count as a valid track.
                All tracks with less detections will be dissmissed.
            t_miss_max (int): Maximum number of missed detections before
                continuing a track. If more detections are missing, the track will not be
                continued.
            overwrite (bool): Whether or not to overwrite existing tracks files. Default: true
        """
        self.otdet_path = Path("./Sequences/test", sequence_name, "otc", f"{sequence_name}.otdet")
        self.sequence_name = sequence_name
        self.sigma_l = sigma_l
        self.sigma_h = sigma_h
        self.sigma_iou = sigma_iou
        self.t_min = t_min
        self.t_miss_max = t_miss_max
        self.overwrite = overwrite

    @timeit
    def run(self):
        tracker([self.otdet_path])

    def rename(self):
        time.sleep(1)
        new_name = self.otdet_path.parent / f"{self.otdet_path.stem}_iou.ittrk"
        new_path = self.otdet_path.parent / (self.otdet_path.stem + '.ottrk')
        if new_name.is_file():
            os.remove(new_name)
        new_path.rename(new_name)

if __name__ == "__main__":
    obj= IOUTracker(
        sequence_name="Car",
        sigma_l=0.27,
        sigma_h=0.42,
        sigma_iou=0.38,
        t_min=5,
        t_miss_max=51,
    )
    obj.run()
