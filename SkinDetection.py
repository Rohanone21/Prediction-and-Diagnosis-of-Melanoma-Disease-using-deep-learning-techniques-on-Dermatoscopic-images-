import cv2
import numpy as np
import time

# Correct video source URL
stream_url = "http://192.0.0.4:8080/shot.jpg"

def get_frame_from_stream():
    retries = 5
    while retries > 0:
        try:
            cap = cv2.VideoCapture(stream_url)
            if not cap.isOpened():
                print(f"Unable to open stream. Retrying... ({5 - retries}/5)")
                retries -= 1
                time.sleep(1)
                continue

            ret, frame = cap.read()
            cap.release()

            if ret:
                print("Frame captured successfully!")
                return frame
            else:
                print(f"Failed to capture frame. Retrying... ({5 - retries}/5)")
                retries -= 1
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}. Retrying... ({5 - retries}/5)")
            retries -= 1
            time.sleep(1)

    print("Failed to connect to the video stream.")
    return None

# Create full screen window
cv2.namedWindow('Skin Detection with Bounding Boxes', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Skin Detection with Bounding Boxes', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    frame = get_frame_from_stream()
    if frame is None:
        print("Exiting as no frame is available.")
        break

    frame = cv2.resize(frame, (640, 480))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Skin color range
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)

    skin = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 0.5 < aspect_ratio < 1.5:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Skin Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

    # Display the result in fullscreen
    cv2.imshow('Skin Detection with Bounding Boxes', frame)
    # You can choose to hide the mask window or resize it as needed
    cv2.imshow('Skin Masking', skin)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        print("ESC pressed. Exiting program.")
        break
    elif key == 32:  # SPACE key
        filename = f"captured_frame_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Frame saved as {filename}")

cv2.destroyAllWindows()
