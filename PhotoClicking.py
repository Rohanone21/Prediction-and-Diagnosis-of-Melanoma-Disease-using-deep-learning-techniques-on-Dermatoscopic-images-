# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 18:03:45 2025

@author: Rohan
"""

import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Python WebCam Screenshot App", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Python WebCam Screenshot App", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

img_counter = 0

while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Python WebCam Screenshot App", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC key
        print("Hit ESC to close the application.")
        break
    elif k % 256 == 32:  # SPACE key
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("Screenshot Taken: {}".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
