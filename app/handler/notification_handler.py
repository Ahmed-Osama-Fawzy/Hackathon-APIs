import smtplib
from email.message import EmailMessage

def SendOTPEmail(message, title):
    try:
        email_user = 'elkhayalsoftwarecompany@gmail.com'
        email_pass = 'qonozbkxlzjgldzp'
        to_email = 'elesraaforaluminiumproducts@gmail.com'
        msg = EmailMessage()
        msg['Subject'] = f"{title} Email"
        msg['From'] = email_user
        msg['To'] = to_email
        msg.set_content(f"Your Message is:\n{message}")

        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(email_user, email_pass)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False