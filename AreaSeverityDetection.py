import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Create a Tkinter window to prompt the file selection dialog
Tk().withdraw()  # Hides the root window
image_path = askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
)

# Check if the image path is valid
if not image_path:
    print("No file selected.")
    exit()

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
elif 324000 <= lesion_area < 500000:
    severity_message = "Moderate Severity"
else:
    severity_message = "High Severity"

# Prepare the text to display
text = f"Area: {int(lesion_area)}, Severity: {severity_message}"

# Set font size for larger text
font_scale = 1.5
thickness = 3

# Calculate text size and position
(font_width, font_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness)

# Set position at bottom of the lesion image
image_height, image_width = lesion_only.shape[:2]
box_margin = 20
box_height = font_height + 30
text_box_top_left = (10, image_height - box_height - box_margin)
text_box_bottom_right = (font_width + 30, image_height - box_margin)

# Draw a red box around the text
cv2.rectangle(
    lesion_only,
    text_box_top_left,
    text_box_bottom_right,
    (0, 0, 255),  # Red color
    thickness=cv2.FILLED
)

# Add white text inside the red box
cv2.putText(
    lesion_only,
    text,
    (text_box_top_left[0] + 10, text_box_bottom_right[1] - 10),
    cv2.FONT_HERSHEY_DUPLEX,
    font_scale,
    (255, 255, 255),  # White text
    thickness,
)

# Resize supporting images for display
screen_width = 800
screen_height = 600
lesion_mask_resized = cv2.resize(lesion_mask, (screen_width, screen_height))
thresh_image_resized = cv2.resize(thresh_image, (screen_width, screen_height))

# Create full screen window for lesion image
cv2.namedWindow("Lesion Region", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Lesion Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Display the lesion image in full screen and other windows normally
cv2.imshow("Lesion Region", lesion_only)
cv2.imshow("Lesion Mask", lesion_mask_resized)
cv2.imshow("Thresholded Image", thresh_image_resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
