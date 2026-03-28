import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(to_email: str, code: str):
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    
    if not smtp_user or not smtp_pass:
        print("\n" + "="*50)
        print(f"📧 MOCK EMAIL DISPATCH TO: {to_email}")
        print(f"🔑 YOUR LUXE LOGIN CODE IS: {code}")
        print("💡 To send real emails, set SMTP_USER and SMTP_PASS variables.")
        print("="*50 + "\n")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = "Your Luxe Fashion Login Code"
        
        body = f"<h2>Welcome to Luxe!</h2><p>Your 6-digit verification code is: <strong style='font-size:24px; color:#d6003c;'>{code}</strong></p><p>This code will expire in 10 minutes. Do not share it with anyone.</p>"
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
