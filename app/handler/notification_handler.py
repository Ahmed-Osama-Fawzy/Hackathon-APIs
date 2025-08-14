import smtplib
from email.message import EmailMessage
import secrets
import string

def SendOTPEmail(message, title, email):
    try:
        email_user = 'elkhayalsoftwarecompany@gmail.com'
        email_pass = 'qonozbkxlzjgldzp'
        to_email = email
        msg = EmailMessage()
        msg['Subject'] = f"{title} Email"
        msg['From'] = email_user
        msg['To'] = to_email
        msg.set_content(f"{message}")

        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(email_user, email_pass)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
    
def generate_numeric_otp(length: int = 6) -> str:
    """Cryptographically secure numeric OTP."""
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(length))
