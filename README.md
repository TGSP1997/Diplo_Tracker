- [**Diplo\_Tracker**](#diplo_tracker)
- [**Installation**](#installation)
- [**Folder Structure of Metadata**](#folder-structure-of-metadata)
- [**Usage**](#usage)
- [**References**](#references)

---
# **Diplo_Tracker**
Following Tracker are implemented:
* IOU-Tracker
* DeepSort-Tracker
* Centroid-Tracker
* VIOU-Tracker
---
# **Installation**
Execute the install.sh<br />
It will create a venv-envirement and install the requierements


---
# **Folder Structure of Metadata**
* Similar structure as MOTChallenge
* Modify Sequence_list.json with the Sequence Names
* Empty structure is created at start
```
    Sequences/
    ├─ Runtime_Scores.csv
    ├─ Runtime_Comparison.pdf
    ├─ Runtime_Comparison.png
    ├─ test/
    │  ├─ Sequence01/
    │  │  ├─ det/
    │  │  │  ├─ det.txt
    │  │  │  ├─ det.npy
    │  │  ├─ track/
    │  │  │  ├─ track_tracker.txt
    │  │  ├─ gt/
    │  │  │  ├─ gt.txt
    │  │  ├─ img1/
    │  │  │  ├─ 000001.jpg
    │  │  │  ├─ ...
    │  │  ├─ otc/
    │  │  │  ├─ Sequence01_tracker.ottrk
    │  │  │  ├─ Sequence01.otdet
    │  │  ├─ video/
    │  │  │  ├─ Sequence01.mp4
    │  │  │  ├─ Sequence01_all.mp4
    │  │  │  ├─ Sequence01_det.mp4
    │  │  │  ├─ Sequence01_tracker_name.mp4
    │  ├─ Sequence02/
    │  ├─ .../
    ├─ [train]
    
```

---
# **Usage**
Every Tracker needs its own files beforehand<br />
In order to visualize the results the img1 (Image Sequence) is needed
| Tracker | Files needed |
|-------|------|
| IOU    | .otdet |
| VIOU    | img1 (Image Sequence) and .otdet |
| DeepSORT    | img1 (Image Sequence) and .otdet |
| Centroid    | .otdet |

To execute run the run.py

---
# **References**

| Repro | Link |
|-------|------|
| OTVision   | [OTVision](https://github.com/OpenTrafficCam/OTVision) modified to run again and forked in [Modified OTVision](https://github.com/TGSP1997/OTVision)   
| DeepSORT   | [DeepSORT](https://github.com/nwojke/deep_sort) modified to run again and forked in [Modified DeepSORT](https://github.com/TGSP1997/deep_sort)   |
| VIOU   | [VIOU](https://github.com/bochinski/iou-tracker) modified to run again and forked in [Modified VIOU](https://github.com/TGSP1997/iou-tracker)   
| Centroid  | [Centroid](https://github.com/adipandas/multi-object-tracker) modified to run again and forked in [Modified Centroid](https://github.com/TGSP1997/multi-object-tracker)   
| py-lapsolver  | [py-lapsolver](https://github.com/cbm755/py-lapsolver) modified to run again and forked in [Modified py-lapsolver](https://github.com/TGSP1997/py-lapsolver)   
