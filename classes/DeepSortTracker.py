from deep_sort.tools.generate_detections import generate_detections, create_box_encoder
from deep_sort.deep_sort_app import run
from pathlib import Path
import time
from functools import wraps
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
        args[0].create_npy()
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

def timeit_fnc_only(func):
    """
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    Decorator to calculate runtime of specific class function
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f'Function {func.__name__}{args} Took {total_time:.4f} seconds')
        
        return result
    return timeit_wrapper


class DeepSortTracker:
    """
    Represents already implemented DeepSortTracker as for better use in OOP    
    """
    def __init__(
        self,
        sequence_name: str,
        min_confidence: float,
        nms_max_overlap: float,
        min_detection_height: int,
        max_cosine_distance: float,
        nn_budget: int,
        modelpath: str = './resources/mars-small128.pb',
        display: bool = False
    ) -> None:
        """
        Creates Class with needed parameters needed for DeepSort Tracker
        Definition copied from deep_sort_app
        Args:
            Run multi-target tracker on a particular sequence.

            Parameters
            ----------
            modelpath : str
                Path to .pb model
            min_confidence : float
                Detection confidence threshold. Disregard all detections that have
                a confidence lower than this value.
            nms_max_overlap: float
                Maximum detection overlap (non-maxima suppression threshold).
            min_detection_height : int
                Detection height threshold. Disregard all detections that have
                a height lower than this value.
            max_cosine_distance : float
                Gating threshold for cosine distance metric (object appearance).
            nn_budget : Optional[int]
                Maximum size of the appearance descriptor gallery. If None, no budget
                is enforced.
            display : bool
                If True, show visualization of intermediate tracking results. Default: False

        """
        self.otdet_path = Path("./Sequences/test", sequence_name, "otc", f"{sequence_name}.otdet")
        self.sequence_name = sequence_name
        self.modelpath = Path(modelpath)
        self.sequence_dir = Path("./Sequences/test", sequence_name)
        self.detection_file = Path("./Sequences/test", sequence_name, "det", f"{sequence_name}.npy")
        self.output_file = Path("./Sequences/test", sequence_name, "track/track_deep.txt")
        self.min_confidence = min_confidence
        self.nms_max_overlap = nms_max_overlap
        self.min_detection_height = min_detection_height
        self.max_cosine_distance = max_cosine_distance
        self.nn_budget = nn_budget
        self.display = display

    @timeit
    def run(self):
        run(
            sequence_dir=self.sequence_dir,
            detection_file=self.detection_file,
            output_file=self.output_file,
            min_confidence=self.min_confidence,
            nms_max_overlap=self.nms_max_overlap,
            min_detection_height=self.min_detection_height,
            max_cosine_distance=self.max_cosine_distance,
            nn_budget= self.nn_budget,
            display = self.display
        )

    @timeit_fnc_only
    def create_npy(
        self
    ):
        encoder = create_box_encoder(
            self.modelpath,
            batch_size=32
        )
        generate_detections(
            encoder,
            mot_dir=Path("./Sequences/test",self.sequence_name).as_posix(),
            output_dir=Path("./Sequences/test", self.sequence_name, "det"),
        )

if __name__ == "__main__":
    obj= DeepSortTracker(
        sequence_name="Car",
        modelpath = './resources/mars-small128.pb',
        min_confidence = 0.3,
        nms_max_overlap = 1.0,
        min_detection_height = 0,
        max_cosine_distance = 0.2,
        nn_budget = 100,
        display = False
    )
    obj.run()
