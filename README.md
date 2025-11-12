# MV-SLAM-Exploration

General SLAM demo scripts using OpenCV and NumPy. The repository contains small, focused examples demonstrating common frontend techniques (feature detection, descriptor matching, and optical flow) that are useful when building SLAM pipelines.

## Repository layout
- `SIFT.py`, `FAST.py`, `ORB.py`, `LK.py` — demo scripts (detection, matching, tracking).
- `Images/` — place input images here (default demo names: `MotoGP0.png`, `MotoGP1.png`).
- `Outputs/` — demo outputs (visualizations) are written here by the scripts.
- `requirements.txt` — Python dependencies.

## Quick start

1. Create and activate a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Put your input images into the `Images/` directory (scripts look for `MotoGP0.png` and `MotoGP1.png` by default).

3. Run a demo — outputs will be written to `Outputs/` (the scripts create the folder if missing):

```bash
python3 SIFT.py
python3 ORB.py
python3 FAST.py
python3 LK.py
```

4. Inspect results:

```bash
ls -la Outputs/
```

Typical output names include `out_feat_*`, `out_matches*`, and `out_flow*` images.

## Troubleshooting
- If OpenCV is missing or SIFT is unavailable, install the contrib build:

```bash
pip install --upgrade opencv-contrib-python
```

- If your images are named differently, either rename them to `MotoGP0.png`/`MotoGP1.png` or I can add CLI options to the scripts to accept arbitrary paths.

## Next steps (optional)
- Add `argparse` to scripts for configurable input/output paths.
- Factor shared utilities (I/O, visualization) into a `utils.py` module.
- Add tests and CI that validate the demos (if desired).
