import cv2
import numpy as np
import skimage.feature as skf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import textwrap

# Create a Tkinter window to prompt file selection dialog
Tk().withdraw()
image_path = askopenfilename(title="Select an Image",
                             filetypes=[("Image Files", ".jpg;.jpeg;.png;.bmp;*.tiff")])

if not image_path:
    print("No file selected.")
    exit()

image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found.")
    exit()

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
_, thresh_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) == 0:
    print("No lesion detected.")
    exit()

largest_contour = max(contours, key=cv2.contourArea)
lesion_mask = np.zeros_like(gray_image)
cv2.drawContours(lesion_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
lesion_only = cv2.bitwise_and(image, image, mask=lesion_mask)

# Lesion Parameters
lesion_area = cv2.contourArea(largest_contour)
diameter = np.sqrt(4 * lesion_area / np.pi)
perimeter = cv2.arcLength(largest_contour, True)
border_irregularity = perimeter / np.sqrt(lesion_area)
melanin_distribution = np.mean(gray_image[lesion_mask == 255])

# Texture Analysis
glc_matrix = skf.graycomatrix(gray_image, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
contrast = skf.graycoprops(glc_matrix, prop='contrast')[0, 0]
energy = skf.graycoprops(glc_matrix, prop='energy')[0, 0]

# Dark Spots Detection
_, dark_spots = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)
dark_spots_ratio = np.sum(dark_spots == 255) / (image.shape[0] * image.shape[1])
dark_spots_present = "Yes" if dark_spots_ratio > 0.02 else "No"

# Skin Color Analysis (HSV)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
avg_hue = np.mean(hsv_image[:, :, 0])
skin_color = "Fair" if avg_hue < 15 else "Medium" if avg_hue < 30 else "Dark"

# Oily vs Dry Skin (Shininess Estimation)
specular_map = cv2.inRange(hsv_image[:, :, 2], 220, 255)
oiliness_ratio = np.sum(specular_map == 255) / (image.shape[0] * image.shape[1])
skin_type = "Oily" if oiliness_ratio > 0.05 else "Dry"

# Hair Detection (Black Strands Detection)
hair_mask = cv2.inRange(gray_image, 0, 40)
hair_ratio = np.sum(hair_mask == 255) / (image.shape[0] * image.shape[1])
skin_hair = "Hairy" if hair_ratio > 0.01 else "Clean"

# Severity Classification Based on Lesion Size and Melanin
if lesion_area < 300000 and melanin_distribution < 100:
    severity_message = "Low Severity"
elif lesion_area < 500000 or melanin_distribution < 150:
    severity_message = "Moderate Severity"
else:
    severity_message = "High Severity"

# Parameters Table
parameters = [
    ("Melanin", f"{round(melanin_distribution, 2)}"),
    ("Border Irregularity", f"{round(border_irregularity, 2)}"),
    ("Diameter", f"{round(diameter, 2)}"),
    ("Dark Spots", dark_spots_present),
    ("Skin Color", skin_color),
    ("Skin Type", skin_type),
    ("Hair", skin_hair),
    ("Severity", severity_message)
]

# Define Layout Sizes
screen_width, screen_height = 1280, 720
lesion_width, lesion_height = 500, 500  # Reduce lesion image size
table_width, table_height = 400, lesion_height

# Resize lesion image
lesion_only_resized = cv2.resize(lesion_only, (lesion_width, lesion_height))

# Create Table Background
table_bg = np.ones((table_height, table_width, 3), dtype=np.uint8) * 255  # White background

cell_height = 50
font_scale, font_thickness = 0.6, 1

def draw_text(img, text, pos):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)

# Draw Table
y_offset = 30
for param, value in parameters:
    cv2.rectangle(table_bg, (10, y_offset), (table_width - 10, y_offset + cell_height), (0, 0, 0), thickness=1)
    draw_text(table_bg, f"{param}: {value}", (20, y_offset + 30))
    y_offset += cell_height + 5

# Combine Table and Lesion Image
final_output = np.hstack((table_bg, lesion_only_resized))

# Display in Full Screen
cv2.namedWindow("Lesion Analysis", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Lesion Analysis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("Lesion Analysis", final_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
