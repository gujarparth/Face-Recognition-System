import smtplib
from email.message import EmailMessage
import os
from datetime import datetime
from dotenv import load_dotenv

# Load the hidden variables from the .env file
load_dotenv() 

def send_attendance_email():
    print("[INFO] Preparing to send end-of-day report...")

    # --- 1. YOUR SECURE CREDENTIALS ---
    # The script now securely grabs ALL emails and passwords from the .env file!
    sender_email = os.getenv("SENDER_EMAIL")         
    app_password = os.getenv("APP_PASSWORD")  
    receiver_email = os.getenv("RECEIVER_EMAIL") # <-- Now perfectly dynamic!
    
    # Check if variables loaded correctly to prevent confusing errors
    if not all([sender_email, app_password, receiver_email]):
        print("[CRITICAL ERROR] Missing credentials! Check your .env file.")
        return

    # --- 2. EMAIL CONTENT ---
    today_date = datetime.now().strftime('%d-%m-%Y')
    subject = f"Automated Smart Attendance Log - {today_date}"
    
    body = f"""Respected Sir/Madam,

Please find attached the automated face-recognition attendance report for {today_date}. 

The attached CSV file contains the timestamped entry logs for all recognized individuals.

Best regards,
Parth Gujar
25BAI11507
"""
    
    # Create the email structure
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)
    
    # --- 3. ATTACH THE CSV FILE ---
    file_name = "Attendance.csv"
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            file_data = f.read()
        # Add the attachment
        msg.add_attachment(file_data, maintype='text', subtype='csv', filename=file_name)
        print(f"[SUCCESS] Found and attached {file_name}")
    else:
        print("[CRITICAL ERROR] Attendance.csv not found! Run the main scanner first.")
        return
        
    # --- 4. SEND THE EMAIL ---
    print(f"[INFO] Connecting to Google SMTP server to send to {receiver_email}...")
    try:
        # Connect securely to Gmail's port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            
        print("[SUCCESS] BOOM! Email sent successfully.")
        
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        print("Tip: Check if your App Password is correct and has no spaces.")

if __name__ == "__main__":
    send_attendance_email()