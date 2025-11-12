import os
import cv2 as cv
import numpy as np

# Inputs: read two images for comparison
INPUT_DIR = "Images"
OUTPUT_DIR = "Outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

I0 = cv.imread(os.path.join(INPUT_DIR, "MotoGP0.png"))
I1 = cv.imread(os.path.join(INPUT_DIR, "MotoGP1.png"))
assert I0 is not None and I1 is not None, "Failed to read input images"

# Convert to grayscale for feature detection / optical flow
g0 = cv.cvtColor(I0, cv.COLOR_BGR2GRAY)
g1 = cv.cvtColor(I1, cv.COLOR_BGR2GRAY)


# -----------------------------
# Camera intrinsics (optional)
# -----------------------------
# Some pipelines need a camera matrix K and distortion vector. This demo
# attempts to load `calib.npz` (created externally) and falls back to a
# simple pinhole approximation when not present. The fallback uses the image
# center for (cx,cy) and a focal length of ~800 px — good enough for demos.
try:
    # prefer a user-provided calibration file if available
    K = np.load("calib.npz")["K"]
except Exception:
    K = np.array([
        [800, 0, I0.shape[1] / 2],
        [0, 800, I0.shape[0] / 2],
        [0, 0, 1.0]
    ], dtype=np.float64)

# Distortion vector placeholder (zero assumes no distortion)
dist = np.zeros(5)


# ORB feature detection + descriptors
orb = cv.ORB_create(nfeatures=1200)
# detectAndCompute accepts a gray image and returns keypoints + descriptors
k0, d0 = orb.detectAndCompute(g0, None)
k1, d1 = orb.detectAndCompute(g1, None)

print(f"ORB: {len(k0)} / {len(k1)} keypoints")

# Draw keypoints on the original color images for visualization
I0_kp = cv.drawKeypoints(I0, k0, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
I1_kp = cv.drawKeypoints(I1, k1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imwrite(os.path.join(OUTPUT_DIR, "out_feat_I0.png"), I0_kp)
cv.imwrite(os.path.join(OUTPUT_DIR, "out_feat_I1.png"), I1_kp)


# Descriptor matching (Brute-force with Hamming)
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
raw = bf.knnMatch(d0, d1, k=2)

good = []
for m, n in raw:
    # Lowe ratio: accept match m only when it's significantly closer than n
    if m.distance < 0.75 * n.distance:
        good.append(m)

# Convert matched keypoint indices to point arrays (useful for later processing)
pts0 = np.float32([k0[m.queryIdx].pt for m in good]) if len(good) else np.empty((0, 2), dtype=np.float32)
pts1 = np.float32([k1[m.trainIdx].pt for m in good]) if len(good) else np.empty((0, 2), dtype=np.float32)


# Visualize matches
good_sorted = sorted(good, key=lambda m: m.distance)[:80]
match_img = cv.drawMatches(
    I0, k0, I1, k1, good_sorted, None,
    flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)
cv.imwrite(os.path.join(OUTPUT_DIR, "out_matches.png"), match_img)
print(f"good matches (ratio): {len(good)}")

# Optical-flow visualization (Lucas–Kanade)
p0 = cv.goodFeaturesToTrack(g0, maxCorners=600, qualityLevel=0.01, minDistance=7)
p1, st, err = cv.calcOpticalFlowPyrLK(
    g0, g1, p0, None,
    winSize=(21, 21), maxLevel=3,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 30, 0.01)
)

# Keep only successfully tracked points (status flag == 1)
p0t = p0[st[:, 0] == 1]
p1t = p1[st[:, 0] == 1]

# Draw flow lines on a copy of the second image
vis = I1.copy()
for (x0, y0), (x1, y1) in zip(p0t.reshape(-1, 2), p1t.reshape(-1, 2)):
    cv.line(vis, (int(x0), int(y0)), (int(x1), int(y1)), (0, 255, 0), 1)
cv.imwrite(os.path.join(OUTPUT_DIR, "out_flow.png"), vis)
