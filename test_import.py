from classes.DeepSortTracker import DeepSortTracker
from classes.IOUTracker import IOUTracker
from classes.VIOUTracker import VIOUTracker
from classes.CentroidTracker import CentroidTracker
from classes.helpers.create_folder_structure import create_folder_structure
create_folder_structure()
obj= DeepSortTracker(
    sequence_name="Car",
    modelpath = './resources/mars-small128.pb',
    min_confidence = 0.3,
    nms_max_overlap = 1.0,
    min_detection_height = 0,
    max_cosine_distance = 0.2,
    nn_budget = 100,
    display = False,
    max_age=200,
    max_iou_distance=0.9
)
obj.run()
obj= VIOUTracker(
    sequence_name="Car",
    sigma_l=0.3,
    sigma_h=0.5,
    sigma_iou=0.8,
    t_min=5,
    ttl=10,
    keep_upper_height_ratio=1.0,
    tracker_type='MIL'
)
obj.run()
obj= CentroidTracker(
    sequence_name="Car",
    max_lost=10,
    with_kalman=False
)
obj.run()
obj= CentroidTracker(
    sequence_name="Car",
    max_lost=10,
    with_kalman=True
)
obj.run()
obj= IOUTracker(
    sequence_name="Car",
    sigma_l=0.27,
    sigma_h=0.42,
    sigma_iou=0.38,
    t_min=5,
    t_miss_max=51,
)
obj.run()