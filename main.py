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

timer = False
print("Started")
sender = 'jainnimansh@gmail.com'
password = 'wdfcrobslqkbkrsm'

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
            Thank you for participating in <a href="https://techsyndicate.us/intech" target="_blank">inTech '22</a> - the 4th edition of Tech Syndicate's annual intra school tech event.
            This year we had more than 200+ registrations and received 150+ submissions. We hope you enjoyed participating in this competition as much as we enjoyed organising it. 
            <br><br>
            Congratulations and best of luck for the future. Stay tuned for inTech '23.
            <br><br>
            Please find your certificates attached and feel free to DM any moderator in case of issues. 
            <br><br>
            Revolutionize<br>
            Aayan Agarwal, President <a href="tel:+91 9650573555">(+91 9650573555)</a><br>
            Aayush Garg, Vice President <a href="tel:+91 9717966964">(+91 9717966964)</a><br>
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
        "cert 6.png", mode='r')
    draw = ImageDraw.Draw(img)

    name = per["name"]
    font = ImageFont.truetype(
        "Outfit-Medium.ttf",
        100
    )
    txtSize = font.getsize(name)
    nameX = (4960-txtSize[0])/2
    draw.text(
        (nameX, 982),
        name,
        fill='#1b1b1b',
        font=font)

    schooltxtsize = font.getsize(per["school"])
    font = ImageFont.truetype(
        "Outfit-Medium.ttf",
        100
    )
    schoolX = (5050-schooltxtsize[0])/2
    draw.text(
        (schoolX, 1149),
        per["school"],
        fill="#1b1b1b",
        font=font
    )

    eventtxtsize = font.getsize(per["field"])
    font = ImageFont.truetype(
        "Outfit-Medium.ttf",
        100
    )
    EventX = (5650-eventtxtsize[0])/2
    draw.text(
        (EventX, 1304),
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
    f = open('data.json')
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
        print("gen time", end-begin)
        begin = time.time()
        try:
            sendMail(i["mail"], "Partake.png", i["name"])
        except Exception as e:
            print(e)
            print("Error Sending Mail to:", i["name"])

        end = time.time()
        print("send mail time", end-begin)
        os.remove("Partake.png")
        if timer:
            time.sleep(60)
    f.close()
    session.quit()
    print("Finished")


if __name__ == "__main__":
    generator()