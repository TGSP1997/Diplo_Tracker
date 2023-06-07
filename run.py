from classes.IOUTracker import IOUTracker
from classes.DeepSortTracker import DeepSortTracker
from classes.VIOUTracker import VIOUTracker
from classes.CentroidTracker import CentroidTracker
from classes.helpers.create_folder_structure import create_folder_structure
from classes.helpers.calculate_runtime_score import ScoreCalculator
from classes.helpers.create_runtime_score import create_runtime_score
sequence_names = create_folder_structure()
print(sequence_names)
sequence_names = ['Car','Car02']

tracker_class_dict = {}
for sequence_name in sequence_names:
    obj_deep= DeepSortTracker(
        sequence_name=sequence_name,
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
    obj_voiu= VIOUTracker(
        sequence_name=sequence_name,
        sigma_l=0.3,
        sigma_h=0.5,
        sigma_iou=0.8,
        t_min=5,
        ttl=10,
        keep_upper_height_ratio=1.0,
        tracker_type='MIL'
    )
    obj_iou= IOUTracker(
        sequence_name=sequence_name,
        sigma_l=0.27,
        sigma_h=0.42,
        sigma_iou=0.38,
        t_min=5,
        t_miss_max=51,
    )
    obj_ctkal= CentroidTracker(
        sequence_name=sequence_name,
        max_lost=10,
        with_kalman=True
    )
    tracker_class_dict.update({sequence_name:[obj_deep,obj_voiu,obj_iou,obj_ctkal]})

for sequence, trackers in tracker_class_dict.items():
    for tracker in trackers:
        tracker.run()

create_runtime_score(tracker_class_dict=tracker_class_dict, sequence_names=sequence_names)

obj_score = ScoreCalculator()
obj_score.calculate()