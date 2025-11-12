# MV-SLAM-Exploration

Repository of short OpenCV demo scripts for feature detection, matching, and tracking.

Files
- `SIFT.py` — SIFT keypoint detection, descriptor matching, and visualization.
- `FAST.py` — FAST keypoint detection, ORB descriptor computation, matching.
- `ORB.py` — ORB feature detection + matching demo plus an optical-flow example.
- `LK.py` — Lucas–Kanade optical flow tracking demo.
- `SIFTFAST.py`, `FAST.py`, `ORB.py`, `SIFT.py` — helper/demo variants.
- `MotoGP0.png`, `MotoGP1.png` — example input images (included in the workspace).

Requirements

The scripts require Python 3.8+ and OpenCV. See `requirements.txt` for a minimal set of packages.

Quick start

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run a demo (example):

```bash
python3 SIFT.py
```