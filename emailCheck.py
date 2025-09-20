import smtplib

 # Receiver's email
subject = "Test Email from Python"
body = "Hi, this is a test email sent using Python SMTP."

# Formatting the email
message = f"Subject: {subject}\n\n{body}"

try:
    # Set up SMTP connection
    obj = smtplib.SMTP("smtp.gmail.com", 587)
    obj.starttls()  # Secure connection
    obj.login(email, password)  # Login with credentials

    # Send the email
    obj.sendmail(email, recipient, message)
    print("Email sent successfully!")

except smtplib.SMTPAuthenticationError:
    print("Authentication failed! Double-check your email and App Password.")
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
finally:
    obj.quit()  # Close the connection




