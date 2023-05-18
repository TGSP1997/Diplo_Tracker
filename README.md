
# **REWORK TO DO**
- [**REWORK TO DO**](#rework-to-do)
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
* GNN-Tracker
---
# **Installation**
TODO

---
# **Folder Structure of Metadata**
* Similar Structure as MOTChallenge
* Folders like det,track,gt,img1,otc,video are needed even if empty
```
    Sequences/
    ├─ test/
    │  ├─ Sequence01/
    │  │  ├─ det/
    │  │  │  ├─ det.txt
    │  │  │  ├─ [det.npy]
    │  │  ├─ track/
    │  │  │  ├─ track.txt
    │  │  ├─ gt/
    │  │  │  ├─ gt.txt
    │  │  ├─ img1/
    │  │  │  ├─ 000001.jpg
    │  │  │  ├─ ...
    │  │  ├─ otc/
    │  │  │  ├─ Sequence01.ottrk
    │  │  │  ├─ Sequence01.otdet
    │  │  ├─ video/
    │  │  │  ├─ Sequence01.mp4
    │  │  ├─ seqinfo.ini
    │  ├─ Sequence02/
    │  ├─ .../
    ├─ [train]
    
```

---
# **Usage**
Every Tracker needs its own files beforehand
| Tracker | Files needed |
|-------|------|
| IOU    | .otdet |
| DeepSORT    | img1 (Image Sequence) and .otdet |

---
# **References**

| Repro | Link |
|-------|------|
| OTVision    |  [OTVision](https://github.com/OpenTrafficCam/OTVision)  |
| DeepSORT   | [DeepSORT](https://github.com/nwojke/deep_sort) modified to run again and forked in [Modified DeepSORT](https://github.com/TGSP1997/deep_sort)   |
