import cv2 as cv
import numpy as np

# Load two images of the same scene
I0 = cv.imread("MotoGP0.png")
I1 = cv.imread("MotoGP1.png")

assert I0 is not None and I1 is not None
g0 = cv.cvtColor(I0, cv.COLOR_BGR2GRAY); g1 = cv.cvtColor(I1, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create(nfeatures=1200)
k0,d0 = sift.detectAndCompute(g0, None)
k1,d1 = sift.detectAndCompute(g1, None)

cv.imwrite("out_detection_sift_f0.png", cv.drawKeypoints(I0, k0, None,
          flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
cv.imwrite("out_detection_sift_f1.png", cv.drawKeypoints(I1, k1, None,
          flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))

bf = cv.BFMatcher(cv.NORM_L2)
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
cv.imwrite("out_matches_sift.png", match_img)
print(f"SIFT: kp0={len(k0)} kp1={len(k1)} good={len(good)} kept={len(keep)}")
