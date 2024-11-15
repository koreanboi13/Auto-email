import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import openpyxl
import sys
import os
from pathlib import Path

def prepare_args(list_of_beats):
    with open("path.txt", 'r') as f:
        folder_path = f.readline().strip()
    
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path) and os.path.getsize(full_path) < 25 * 1024 * 1024:
            list_of_beats.append(full_path)

def send_email_bcc(recipients, sender_email, sender_password, subject,body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message["To"] = ""  

    message.attach(MIMEText(body, "plain"))

    files = []
    prepare_args(files)
    for file_path in files:
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path)}",
            )
            message.attach(part)
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
            print("Письмо успешно отправлено всем получателям!")
    except Exception as e:
        print(f"Ошибка: {e}")


with open('sender.txt', 'r') as f:
    sender_email = f.readline().strip()
    sender_password = f.readline().strip()


wb_obj = openpyxl.load_workbook("artists.xlsx")
sheet_obj = wb_obj.active

argv = sys.argv[1]

bcc_recipients = []

if argv == "1":
    status_search = "ждет"
    
    with open("text_first", 'r') as f:
        subject = f.readline()
        body = f.readline()

    i = 1
    while True:
        status = sheet_obj[f"H{i}"].value
        if status == status_search:
            recipient_email = sheet_obj[f"F{i}"].value
            bcc_recipients.append(recipient_email)
            sheet_obj[f"H{i}"] = "Отправил биты" 
        if sheet_obj[f"H{i}"].value is None:
            break
        i += 1

elif argv == "2":
    status_search = "отправил биты"
    
    with open("text_multiple", 'r') as f:
        subject = f.readline()
        body = f.readline()

    i = 1
    while True:
        status = sheet_obj[f"H{i}"].value
        if status == status_search:
            recipient_email = sheet_obj[f"F{i}"].value
            bcc_recipients.append(recipient_email)
        if sheet_obj[f"H{i}"].value is None:
            break
        i += 1

if bcc_recipients:
    send_email_bcc(bcc_recipients, sender_email, sender_password, body)

wb_obj.save("artists.xlsx")

