import smtplib
from config import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image     import MIMEImage

def mail_send(msg): 
    smtp_server = smtplib.SMTP(host=os.getenv("MAIL_HOST"), port=587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(os.getenv("MAIL_ID"), os.getenv("MAIL_PASSWORD"))
    smtp_server.send_message(msg) 
    smtp_server.quit()

def mail_content(title, content, to):
    contents = MIMEText(
        """<html>
            <head></head>
            <body>
                Hi .<br>
                <img src="cid:my_image1"><br>
                This is a test message.
            </body>"""
        ,"html"
    )
    message = MIMEMultipart()
    message["Subject"] = "Allaw::구독하신 키워드 알림이 도착하였습니다."
    message["From"] = os.getenv("MAIL_ID")
    message["To"] = to
    message.attach(contents)
    # with open("C:/Users/user/Desktop/Gemini/image-1.jpeg", 'rb') as img_file:
    #     mime_img = MIMEImage(img_file.read())
    #     mime_img.add_header('Content-ID', '<' + "my_image1" + '>')
    # message.attach(mime_img)
    return message
