#from classes.iou_tracker import IOUTracker
#from classes.viou_tracker import VIOUTracker
#from classes.centroid_tracker import CentroidTracker
#from classes.helpers.calculate_runtime_score import ScoreCalculator
#from classes.helpers.create_runtime_score import create_runtime_score
from classes.deep_sort_tracker import DeepSortTracker
from classes.helpers.create_folder_structure import create_folder_structure
from classes.helpers.create_videos import create_videos
from classes.helpers.check_empty_line import check_for_empty_lines
sequence_names,fr_list, total_frames_list = create_folder_structure()

tracker_class_dict = {}
# auswahl_nmb = 1
# sequence_names = [sequence_names[auswahl_nmb-1]]
# fr_list = [fr_list[auswahl_nmb-1]]
for sequence_name in sequence_names:
    obj_deep= DeepSortTracker(
        sequence_name=sequence_name,
        modelpath = './resources/mars-small128.pb',
        min_confidence = 0.25,
        nms_max_overlap = 1.0,
        min_detection_height = 0,
        max_cosine_distance = 600.2,
        nn_budget = 0,
        display = False,
        max_age=6000,
        max_iou_distance=9.9
    )
    # obj_voiu= VIOUTracker(
    #     sequence_name=sequence_name,
    #     sigma_l=0.3,
    #     sigma_h=0.5,
    #     sigma_iou=0.8,
    #     t_min=5,
    #     ttl=10,
    #     keep_upper_height_ratio=1.0,
    #     tracker_type='MIL'
    # )
    # obj_iou= IOUTracker(
    #     sequence_name=sequence_name,
    #     sigma_l=0.27,
    #     sigma_h=0.42,
    #     sigma_iou=0.38,
    #     t_min=5,
    #     t_miss_max=51,
    # )
    # obj_ctkal= CentroidTracker(
    #     sequence_name=sequence_name,
    #     max_lost=10,
    #     with_kalman=True
    # )
    tracker_class_dict.update({sequence_name:[obj_deep]})#obj_voiu,obj_iou,obj_ctkal

for sequence, trackers in tracker_class_dict.items():
    for tracker in trackers:
        tracker.run()
    #check_for_empty_lines(sequence_name)
for i in range (0,len(sequence_names)):        
    create_videos(sequence_name=sequence_names[i], fps=fr_list[i], track_names=['track_deep'])
# create_runtime_score(tracker_class_dict=tracker_class_dict, sequence_names=sequence_names)
# obj_score = ScoreCalculator()
# obj_score.calculate()