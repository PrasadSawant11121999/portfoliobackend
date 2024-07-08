# main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://portfolio-r8o9.onrender.com/",
    "https://portfolio-r8o9.onrender.com",
    # Add your frontend URL if it's deployed elsewhere
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_email(name: str, email: str, message: str):
    sender_email = "prasad.sawant.1199@gmail.com"
    receiver_email = "prasad11121999@gmail.com"
    password = "ihal xdxe jtsq dqbi"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "New Contact Form Submission"

    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your email provider's SMTP server
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.post("/send-email/")
async def send_email_endpoint(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    if send_email(name, email, message):
        return {"message": "Email sent successfully!"}
    else:
        return {"message": "Failed to send email."}
