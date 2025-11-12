import os
import cv2 as cv
import numpy as np

INPUT_DIR = "Images"
OUTPUT_DIR = "Outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

I0 = cv.imread(os.path.join(INPUT_DIR, "MotoGP0.png"))
I1 = cv.imread(os.path.join(INPUT_DIR, "MotoGP1.png"))

assert I0 is not None and I1 is not None
g0 = cv.cvtColor(I0, cv.COLOR_BGR2GRAY); g1 = cv.cvtColor(I1, cv.COLOR_BGR2GRAY)

# FAST
fast = cv.FastFeatureDetector_create(threshold=20, nonmaxSuppression=True)
k0 = fast.detect(g0, None)
k1 = fast.detect(g1, None)
# keep strongest N so it’s not too busy
k0 = sorted(k0, key=lambda k: -k.response)[:1200]
k1 = sorted(k1, key=lambda k: -k.response)[:1200]

cv.imwrite(os.path.join(OUTPUT_DIR, "out_detection_fast_f0.png"),
           cv.drawKeypoints(I0, k0, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
cv.imwrite(os.path.join(OUTPUT_DIR, "out_detection_fast_f1.png"),
           cv.drawKeypoints(I1, k1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))

# ORB
orb = cv.ORB_create()
k0, d0 = orb.compute(g0, k0)
k1, d1 = orb.compute(g1, k1)

bf = cv.BFMatcher(cv.NORM_HAMMING)
raw = bf.knnMatch(d0, d1, k=2)
good = [m for m,n in raw if m.distance < 0.75*n.distance]

# RANSAC cleanup
if len(good) >= 8:
    p0 = np.float32([k0[m.queryIdx].pt for m in good])
    p1 = np.float32([k1[m.trainIdx].pt for m in good])
    F, mask = cv.findFundamentalMat(p0, p1, cv.FM_RANSAC, 1.0, 0.999)
    keep = [gm for gm,ok in zip(good, mask.ravel()==1) if ok]
else:
    keep = good

match_img = cv.drawMatches(I0, k0, I1, k1, keep[:100], None,
                           flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imwrite(os.path.join(OUTPUT_DIR, "out_matches_fast_orb.png"), match_img)
print(f"FAST+ORB: kp0={len(k0)} kp1={len(k1)} good={len(good)} kept={len(keep)}")