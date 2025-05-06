# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 18:03:45 2025

@author: Rohan
"""

import cv2
import urllib.request
import numpy as np

# IP Webcam URL
URL = "http://192.0.0.4:8080/shot.jpg"
cv2.namedWindow("Python WebCam Screenshot App", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Python WebCam Screenshot App", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

img_counter = 0

while True:
    try:
        # Fetch video frame from IP Webcam
        cap = urllib.request.urlopen(URL)
        img_arr = np.array(bytearray(cap.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        if frame is None:
            print("Failed to grab frame. Retrying...")
            continue

        cv2.imshow("Python WebCam Screenshot App", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC key
            print("Hit ESC to close the application.")
            break
        elif k % 256 == 32:  # SPACE key
            img_name = f"opencv_frame_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print(f"Screenshot taken: {img_name}")
            img_counter += 1

    except Exception as e:
        print(f"Error: {e}")
        break

cv2.destroyAllWindows()
