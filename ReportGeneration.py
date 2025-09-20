import smtplib
import cv2
import numpy as np
import skimage.feature as skf
from tkinter import Tk, simpledialog, filedialog
from fpdf import FPDF
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Email credentials
sender_email = "rohanphadtare134@gmail.com"


# Create a Tkinter window for user input
Tk().withdraw()

# Get user details
name = simpledialog.askstring("Input", "Enter your name:")
gender = simpledialog.askstring("Input", "Enter your gender:")
age = simpledialog.askinteger("Input", "Enter your age:")
recipient_email = simpledialog.askstring("Input", "Enter your email address:")

# Select lesion image
image_path = filedialog.askopenfilename(title="Select an Image",
                                        filetypes=[("Image Files", ".jpg;.jpeg;.png;.bmp;*.tiff")])

if not image_path:
    print("No file selected.")
    exit()

# Read the image
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found.")
    exit()

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
_, thresh_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
    print("No lesion detected.")
    exit()

largest_contour = max(contours, key=cv2.contourArea)
lesion_mask = np.zeros_like(gray_image)
cv2.drawContours(lesion_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
lesion_only = cv2.bitwise_and(image, image, mask=lesion_mask)

# Calculate lesion parameters
lesion_area = cv2.contourArea(largest_contour)  # in pixels
diameter = np.sqrt(4 * lesion_area / np.pi)     # in pixels
perimeter = cv2.arcLength(largest_contour, True)  # in pixels
border_irregularity = perimeter / np.sqrt(lesion_area)
melanin_distribution = np.mean(gray_image[lesion_mask == 255])

# Extra parameters
circularity = (4 * np.pi * lesion_area) / (perimeter ** 2)
aspect_ratio = float(cv2.boundingRect(largest_contour)[2]) / cv2.boundingRect(largest_contour)[3]
solidity = lesion_area / cv2.contourArea(cv2.convexHull(largest_contour))
glcm = skf.graycomatrix(gray_image, distances=[1], angles=[0], symmetric=True, normed=True)
contrast = skf.graycoprops(glcm, 'contrast')[0, 0]
energy = skf.graycoprops(glcm, 'energy')[0, 0]

# Determine severity
severity = "High" if lesion_area > 500000 or melanin_distribution > 150 else "Moderate" if lesion_area > 300000 else "Low"

# Save lesion image
lesion_image_path = "lesion_output.jpg"
cv2.imwrite(lesion_image_path, lesion_only)

# Generate PDF report
pdf_filename = "Lesion_Report.pdf"
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Arial", style='B', size=16)
pdf.cell(200, 10, "Lesion Analysis Report", ln=True, align='C')
pdf.ln(10)

# User Details
pdf.set_font("Arial", size=12)
pdf.cell(100, 10, f"Name: {name}", ln=True)
pdf.cell(100, 10, f"Gender: {gender}", ln=True)
pdf.cell(100, 10, f"Age: {age}", ln=True)
pdf.ln(5)

# Add Lesion Image
pdf.image(lesion_image_path, x=130, y=30, w=60)

# Lesion Analysis Table
pdf.set_font("Arial", style='B', size=12)
pdf.cell(100, 10, "Lesion Analysis Results:", ln=True)
pdf.set_font("Arial", size=12)
pdf.ln(5)

pdf.cell(90, 10, "Parameter", 1, 0, 'C')
pdf.cell(90, 10, "Value (Units)", 1, 1, 'C')

pdf.cell(90, 10, "Lesion Area", 1, 0)
pdf.cell(90, 10, f"{lesion_area:.2f} pixels²", 1, 1)
pdf.cell(90, 10, "Diameter", 1, 0)
pdf.cell(90, 10, f"{diameter:.2f} pixels", 1, 1)
pdf.cell(90, 10, "Border Irregularity", 1, 0)
pdf.cell(90, 10, f"{border_irregularity:.2f} (ratio)", 1, 1)
pdf.cell(90, 10, "Melanin Distribution", 1, 0)
pdf.cell(90, 10, f"{melanin_distribution:.2f} (intensity)", 1, 1)
pdf.cell(90, 10, "Circularity (0-1)", 1, 0)
pdf.cell(90, 10, f"{circularity:.2f}", 1, 1)
pdf.cell(90, 10, "Aspect Ratio", 1, 0)
pdf.cell(90, 10, f"{aspect_ratio:.2f}", 1, 1)
pdf.cell(90, 10, "Solidity (0-1)", 1, 0)
pdf.cell(90, 10, f"{solidity:.2f}", 1, 1)
pdf.cell(90, 10, "Contrast", 1, 0)
pdf.cell(90, 10, f"{contrast:.2f}", 1, 1)
pdf.cell(90, 10, "Energy", 1, 0)
pdf.cell(90, 10, f"{energy:.2f}", 1, 1)
pdf.cell(90, 10, "Severity", 1, 0)
pdf.cell(90, 10, f"{severity}", 1, 1)

pdf.ln(10)

# Save the PDF
pdf.output(pdf_filename)
print(f"Report generated successfully: {pdf_filename}")

# Send the PDF report via email
def send_email(recipient, pdf_file):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = "Skin Lesion Analysis Report"

    body = "Please find your lesion analysis report attached."
    msg.attach(MIMEText(body, "plain"))

    with open(pdf_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_file)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print(f"Report sent successfully to {recipient}")

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

# Call the function to send the email
send_email(recipient_email, pdf_filename)


