# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import openpyxl
# import sys
# import os, os.path
# from pathlib import Path

# def prepare_args(list_of_beats):
#     f = open("path.txt",'r')
#     folder_path = f.readline()
#     f.close

#     for entry in os.listdir(folder_path):
#         full_path = os.path.join(folder_path, entry)
#         if os.path.isfile(full_path) and (os.path.getsize(full_path) < 25*1024*1024):  # Проверяем, что это файл
#            list_of_beats.append(full_path)

# def send_email(recipient_email,sender_email,sender_password,body):
#     subject = "Beat by aurora_melodicbeats"

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = recipient_email
#     message["Subject"] = subject


#     message.attach(MIMEText(body, "plain"))

#     files = []
#     prepare_args(files)
#     for file_path in files:
#         try:
#             with open(file_path, "rb") as attachment:
#                 part = MIMEBase("application", "octet-stream")
#                 part.set_payload(attachment.read())
            
#             encoders.encode_base64(part)
#             part.add_header(
#                 "Content-Disposition",
#                 f"attachment; filename={file_path.split('\\')[-1]}",
#             )
#             message.attach(part)
#         except FileNotFoundError:
#             print(f"Файл '{file_path}' не найден.")
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls() 
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, recipient_email, message.as_string())
#             print("Письмо успешно отправлено!")
#     except Exception as e:
#         print(f"Ошибка: {e}")


# f = open('sender.txt', 'r')
# sender_email  = f.readline()
# sender_password = f.readline()
# f.close()

# wb_obj = openpyxl.load_workbook("artists.xlsx")
# sheet_obj = wb_obj.active

# argv = sys.argv[1]
# print(argv)
# if(argv == "1"):
#     status_search = "ждет"
#     body = "Заменить"

#     i = 1
#     while True:
#         status = sheet_obj[f"H{i}"].value
#         if status == status_search:
#             index = f"f{i}"
#             recipient_email = sheet_obj[index].value
#             send_email(recipient_email, sender_email,sender_password,body)
#             sheet_obj[index] = "Отправил биты"
#         if(sheet_obj[f"H{i}"].value is None):
#             print("stop")
#             break
#         i+=1
# if(argv == "2"):
#     status_search = "отправил биты"
#     body = "заменить"


#     i = 1
#     while True:
#         status = sheet_obj[f"H{i}"].value
#         if status == status_search:
#             index = f"f{i}"
#             recipient_email = sheet_obj[index].value
#             send_email(recipient_email, sender_email,sender_password,body)
#         if(sheet_obj[f"H{i}"].value is None):
#             print("stop")
#             break
#         i+=1
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
    # Чтение пути из файла
    with open("path.txt", 'r') as f:
        folder_path = f.readline().strip()
    
    # Сбор всех файлов, подходящих по размеру
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path) and os.path.getsize(full_path) < 25 * 1024 * 1024:
            list_of_beats.append(full_path)

def send_email_bcc(recipients, sender_email, sender_password, body):
    subject = "Beat by aurora_melodicbeats"

    # Создание письма
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message["To"] = "Undisclosed recipients"  # Необязательно, можно оставить пустым

    message.attach(MIMEText(body, "plain"))

    # Добавление вложений
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

    # Отправка письма всем получателям
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
            print("Письмо успешно отправлено всем получателям!")
    except Exception as e:
        print(f"Ошибка: {e}")

# Чтение данных отправителя
with open('sender.txt', 'r') as f:
    sender_email = f.readline().strip()
    sender_password = f.readline().strip()

# Чтение Excel-файла
wb_obj = openpyxl.load_workbook("artists.xlsx")
sheet_obj = wb_obj.active

argv = sys.argv[1]
print(argv)

# Список всех получателей BCC
bcc_recipients = []

if argv == "1":
    status_search = "ждет"
    body = "Заменить"
    i = 1
    while True:
        status = sheet_obj[f"H{i}"].value
        if status == status_search:
            recipient_email = sheet_obj[f"F{i}"].value
            bcc_recipients.append(recipient_email)
            sheet_obj[f"H{i}"] = "Отправил биты"  # Обновление статуса
        if sheet_obj[f"H{i}"].value is None:
            print("stop")
            break
        i += 1
elif argv == "2":
    status_search = "отправил биты"
    body = "Заменить"
    i = 1
    while True:
        status = sheet_obj[f"H{i}"].value
        if status == status_search:
            recipient_email = sheet_obj[f"F{i}"].value
            bcc_recipients.append(recipient_email)
        if sheet_obj[f"H{i}"].value is None:
            print("stop")
            break
        i += 1

# Отправляем письма скрытой копией всем собранным адресатам
if bcc_recipients:
    send_email_bcc(bcc_recipients, sender_email, sender_password, body)

# Сохраняем изменения в Excel-файле
wb_obj.save("artists.xlsx")

