

- [**Diplo\_Tracker**](#diplo_tracker)
- [**Installation**](#installation)
- [**Folder Structure of Metadata**](#folder-structure-of-metadata)
- [**Usage**](#usage)
  - [| GNN    | TODO |](#-gnn-----todo-)
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
| GNN    | TODO |
---
# **References**

| Repro | Link |
|-------|------|
| OTVision    |  [OTVision](https://github.com/OpenTrafficCam/OTVision)  |
| DeepSORT   | [DeepSORT](https://github.com/nwojke/deep_sort) modified to run again and forked in [Modified DeepSORT](https://github.com/TGSP1997/deep_sort)   |
| StoneSoup    | [StoneSoup](https://stonesoup.readthedocs.io/en/latest/index.html)   |