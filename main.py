from PIL import Image, ImageDraw, ImageFont
import math
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time


# Real gen se pehle timer on kar dena pls

data_location = ""
cert_location = ""
mail = False
timer = False
print("Started")
sender = 'jainnimansh@gmail.com'
password = '***'

session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(sender, password)


def sendMail(receiver1, sample_pdf_path, name):
    receiver = receiver1

    Body = MIMEMultipart()
    Body['From'] = sender
    Body['To'] = receiver
    Body['Subject'] = 'Certificate-TS'

    html_txt = """\
    <html>
        <body>
            <h1>Hi {name},</h1>
            Thank you for participating in <a href="https://techsyndicate.us/robo" target="_blank">Robotronics '22</a> - the 10th edition of Tech Syndicate's annual tech event.
            This year we had more than 500+ registrations and received 150+ submissions. We hope you enjoyed participating in this competition as much as we enjoyed organising it. 
            <br><br>
            Congratulations and best of luck for the future. Stay tuned for Robotronics '23.
            <br><br>
            Please find your certificates attached and feel free to DM any moderator in case of issues. 
            <br><br>
            Revolutionize<br>
            Aayan Agarwal, President (<a href="tel:+91 9650573555">+91 9650573555</a>)<br>
            Aayush Garg, Vice President (<a href="tel:+91 9717966964">+91 9717966964</a>)<br>
        </body>
    </html>  
    """.format(name=name)
    html_at = MIMEText(html_txt, "html")
    Body.attach(html_at)

    pdf = sample_pdf_path
    binary_pdf = open(pdf, 'rb')

    msg = MIMEBase('application', 'octate-stream', Name="Cert.png")
    msg.set_payload((binary_pdf).read())

    encoders.encode_base64(msg)

    msg.add_header('Content-Decomposition', 'attachment', filename=pdf)
    Body.attach(msg)

    text = Body.as_string()
    session.sendmail(sender, receiver, text)
    print('Mail Sent')


def makePart(per):
    img = Image.open(
        cert_location, mode='r')
    draw = ImageDraw.Draw(img)

    name = per["name"]
    font = ImageFont.truetype(
        "font.woff2",
        80
    )
    txtSize = font.getlength(name)
    nameX = (4960-txtSize)/2
    draw.text(
        (nameX, 1001),
        name,
        fill='#1b1b1b',
        font=font)

    schooltxtsize = font.getlength(per["school"])
    font = ImageFont.truetype(
        "font.woff2",
        80
    )
    schoolX = (5100-schooltxtsize)/2
    draw.text(
        (schoolX, 1170),
        per["school"],
        fill="#1b1b1b",
        font=font
    )

    eventtxtsize = font.getlength(per["field"])
    font = ImageFont.truetype(
        "font.woff2",
        80
    )
    EventX = (5650-eventtxtsize)/2
    draw.text(
        (EventX, 1323),
        per["field"],
        fill="#1b1b1b",
        font=font
    )

    img.save("Partake.png")


def conversion(flag):
    i1 = Image.open(
        'Partake.png')
    im1 = i1.convert('RGB')
    im1.save("Certificate.pdf")
    os.remove("D:/nimansh/python/practice questions - TS/Fonts/Partake.png")


def generator():
    f = open(data_location)
    res = json.load(f)
    dt = res["data"]

    for i in dt:
        begin = time.time()
        try:
            makePart(i)
        except Exception as e:
            print(e)
            print("Error making Participation Certificate for:", i["name"])
        end = time.time()
        print("gen time", int(end-begin))
        if mail:
            begin = time.time()
            try:
                sendMail(i["mail"], "Partake.png", i["name"])
            except Exception as e:
                print(e)
                print("Error Sending Mail to:", i["name"])
            end = time.time()
            print("send mail time", int(end-begin))
            os.remove("Partake.png")
        if timer:
            time.sleep(30)
    f.close()
    session.quit()
    print("Finished")


if __name__ == "__main__":
    generator()
