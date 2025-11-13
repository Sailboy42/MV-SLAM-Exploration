# Visual SLAM
This repo contains demos of a few different elements of SLAM (Simultaneous Localization and Mapping) along with slides that can be used for a teach-in on visual SLAM. The slides cover a high-level overview of the elements of SLAM, while the Visual Odometry and Feature Extraction folders each contain a demo covering a sub-topic of SLAM.

## Contents
- **SLAM overview teach-in slides** ```Visual_SLAM_Overview.pdf```: A presentation covering the major elements of SLAM, including strategies for feature extraction, feature tracking, camera pose estimation, local mapping, bundle adjustment, and loop closure.
- **Visual Odometry** (folder): A sub-repo containing a demo on how to implement visual odometry on a series of camera images using OpenCV. The demo creates a map of the path traveled as well as a live visualization of the visual features as they are detected.
- **Feature Extraction** (folder): A sub-repo containing demos on a couple of the sub-steps of visual odometry (feature detection, feature matching, and feature tracking).

## Division of Labor
Owen created the Feature Extraction demo, Zara created the Visual Odometry demo, and Bhargavi created the teach-in slides.
