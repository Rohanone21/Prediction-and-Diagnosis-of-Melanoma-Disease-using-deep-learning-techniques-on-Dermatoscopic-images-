# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 19:12:33 2025

@author: Rohan
"""

import cv2
import numpy as np

# Correct file path with raw string
image_path = r"C:\Users\Rohan\Desktop\skin cancer Desktop 100% code\skin cancer Desktop 100% code (1)\skin cancer Desktop 100% code (1)\skin cancer Desktop 100% code\data\3melanoma\ISIC_0000161.jpg"

# Read the image
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Image not found at the specified path.")
    exit()

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Apply Otsu's thresholding to segment the lesion region
_, thresh_image = cv2.threshold(
    blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ensure at least one contour is found
if len(contours) == 0:
    print("No lesion detected.")
    exit()

# Filter to get the largest contour (assuming it's the lesion)
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask for the lesion region
lesion_mask = np.zeros_like(gray_image)
cv2.drawContours(lesion_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

# Mask the original image to focus only on the lesion region
lesion_only = cv2.bitwise_and(image, image, mask=lesion_mask)

# Calculate the area of the lesion
lesion_area = cv2.contourArea(largest_contour)

# Approximate the shape of the lesion
epsilon = 0.01 * cv2.arcLength(largest_contour, True)
approx = cv2.approxPolyDP(largest_contour, epsilon, True)

# Detect shape based on the number of edges
if len(approx) == 3:
    shape = "Triangle"
elif len(approx) == 4:
    shape = "Quadrilateral"
elif len(approx) == 5:
    shape = "Pentagon"
elif len(approx) == 6:
    shape = "Hexagon"
else:
    shape = "Irregular/Circle"

# Calculate the bounding box of the lesion
x, y, w, h = cv2.boundingRect(largest_contour)

# Add severity feedback based on area
if lesion_area < 300000:
    severity_message = "Low Severity"
elif 300000 <= lesion_area < 400000:
    severity_message = "Moderate Severity"
else:
    severity_message = "High Severity"

# Add red text for area and severity below the lesion
text = f"Area: {int(lesion_area)}, Severity: {severity_message}"
cv2.putText(
    lesion_only,
    text,
    (x, y + h + 20),  # Position below the bounding box
    cv2.FONT_HERSHEY_DUPLEX,
    0.8,
    (0, 0, 255),  # Red color
    2,
)

# Resize images to fit screen dimensions
screen_width = 800
screen_height = 600

# Resizing lesion region
lesion_only_resized = cv2.resize(lesion_only, (screen_width, screen_height))
lesion_mask_resized = cv2.resize(lesion_mask, (screen_width, screen_height))
thresh_image_resized = cv2.resize(thresh_image, (screen_width, screen_height))

# Display the lesion region with annotations
cv2.imshow("Lesion Region", lesion_only_resized)
cv2.imshow("Lesion Mask", lesion_mask_resized)
cv2.imshow("Thresholded Image", thresh_image_resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
