import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, recipient_name: str, email_body: str):
    try:
        print(f"📧 Connecting to Gmail...")
        
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = to_email
        msg["Subject"] = f"Quick idea for {recipient_name}"
        
        msg.attach(MIMEText(email_body, "plain"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        print(f"🔑 Logging in...")
        server.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD")
        )
        
        print(f"📤 Sending email...")
        server.sendmail(
            os.getenv("EMAIL_ADDRESS"),
            to_email,
            msg.as_string()
        )
        
        server.quit()
        
        print(f"✅ Email sent successfully to: {recipient_name} | {to_email}")
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    print(f"📧 Email loaded: {email}")
    print(f"🔑 Password loaded: {'✅ Yes' if password else '❌ No'}")
    
    send_email(
        to_email=email,
        recipient_name="Test",
        email_body="Hi,\n\nThis is a test email.\n\nBest,\nAlex"
    )