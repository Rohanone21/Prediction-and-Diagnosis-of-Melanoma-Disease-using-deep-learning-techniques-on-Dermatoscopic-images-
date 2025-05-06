import cv2
import numpy as np
import urllib.request

URL = "http://192.0.0.4:8080/shot.jpg"  # Add '/shot.jpg' for image capture from IP Webcam app
while True:
    try:
        # Fetch data from the IP webcam
        response = urllib.request.urlopen(URL)
        img_arr = np.array(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)

        # Check if the image was decoded properly
        if img is None:
            print("Failed to decode the image. Retrying...")
            continue

        # Display the image
        cv2.imshow('IPWebcam', img)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"Error: {e}")
        break

cv2.destroyAllWindows()
