"""
Helper to write a csv with all runtime infos
"""


import csv
from typing import Dict


def create_runtime_score(tracker_class_dict: Dict, sequence_names: list[str]) -> None:
    """write a csv with all runtime infos

    Args:
        tracker_class_dict (Dict): Dict which contains all tracker class objects
        sequence_names (list[str]): List of the sequence names
    """
    to_write = []
    to_write.append(['Tracker'] + sequence_names)

    deep1_v = ['DeepSort \\nwo Feature']
    deep2_v = ['Deepsort \\nw Feature']
    iou_v = ['IOU']
    viou_v = ['VIOU']
    ctkal_v= ['Centroid \\nw Kalman']
    for _, trackers in tracker_class_dict.items():
        for tracker in trackers:
            if tracker.__class__.__name__ == 'DeepSortTracker':
                print(tracker.__class__.__name__, tracker.runtime_1, tracker.sequence_name)
                print(tracker.__class__.__name__, tracker.runtime_2, tracker.sequence_name)
                deep1_v.append(tracker.runtime_1)
                deep2_v.append(tracker.runtime_2)
            if tracker.__class__.__name__ == 'VIOUTracker':
                print(tracker.__class__.__name__, tracker.runtime, tracker.sequence_name)
                viou_v.append(tracker.runtime)
            if tracker.__class__.__name__ == 'IOUTracker':
                print(tracker.__class__.__name__, tracker.runtime, tracker.sequence_name)
                iou_v.append(tracker.runtime)
            if tracker.__class__.__name__ == 'CentroidTracker':
                ctkal_v.append(tracker.runtime)
                print(tracker.__class__.__name__, tracker.runtime, tracker.sequence_name)

    to_write.append(deep1_v)
    to_write.append(iou_v)
    to_write.append(viou_v)
    to_write.append(ctkal_v)
    to_write.append(deep2_v)

    with open(r'./Sequences/Runtime_Scores.csv', 'w', encoding = 'utf-8',newline = '') as outfile:
        csv.excel.delimiter = ';'
        writer = csv.writer(outfile, dialect = csv.excel)
        for line in to_write:
            writer.writerow(line)
