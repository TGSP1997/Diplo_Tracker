from classes.DeepSortTracker import DeepSortTracker
from classes.IOUTracker import IOUTracker

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