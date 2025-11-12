# tracking_lk.py
import cv2 as cv
import numpy as np

I0 = cv.imread("MotoGP0.png")
I1 = cv.imread("MotoGP1.png")
assert I0 is not None and I1 is not None
g0 = cv.cvtColor(I0, cv.COLOR_BGR2GRAY); g1 = cv.cvtColor(I1, cv.COLOR_BGR2GRAY)

# Pick seed points to track (Shi–Tomasi corners)
p0 = cv.goodFeaturesToTrack(g0, maxCorners=800, qualityLevel=0.01, minDistance=7)

# Forward optical flow
p1, st, err = cv.calcOpticalFlowPyrLK(
    g0, g1, p0, None,
    winSize=(21,21), maxLevel=3,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 30, 0.01)
)
p0f = p0[st[:,0]==1]; p1f = p1[st[:,0]==1]

# Forward–backward check
p0b, stb, _ = cv.calcOpticalFlowPyrLK(g1, g0, p1f, None, winSize=(21,21), maxLevel=3)
good = (stb[:,0]==1) & (np.linalg.norm(p0f - p0b, axis=2).ravel() < 1.0)
p0g, p1g = p0f[good], p1f[good]

# Draw arrows
vis = I1.copy()
for (x0,y0),(x1,y1) in zip(p0g.reshape(-1,2), p1g.reshape(-1,2)):
    cv.arrowedLine(vis, (int(x0),int(y0)), (int(x1),int(y1)), (0,255,0), 1, tipLength=0.3)
cv.imwrite("out_tracking_lk.png", vis)
print(f"LK tracked (after FB check): {len(p0g)}")
