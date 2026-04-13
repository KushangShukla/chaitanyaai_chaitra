import smtplib
import random
import os 

EMAIL=os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_otp_email(to_email):

    otp = str(random.randint(100000, 999999))

    message = f"Subject: Your OTP\n\nYour OTP is {otp}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, to_email, message)

    return otp