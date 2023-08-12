import smtplib, os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv('.env')

def send_email(to_email:str, subject:str, message:str):
    sender = os.environ.get('smtp_sender')
    password = os.environ.get('smtp_sender_password')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email
        msg.set_content(message)

        server.login(sender, password)
        server.send_message(msg) #Тут тоже надо поменять
        return "200 ok"
    except Exception as error:
        return f"Error: {error}"
    
# print(send_email('ktoktorov144@gmail.com', 'Geeks', 'Hello Geeks!'))
print(send_email('ktoktorov144@gmail.com', 'Сегодня у вас урок в 18:00', 'Здравствуйте сегодня у вас урок по Backend-разработке в 18:00. Приходите без опозданий!'))

emails = ['ktoktorov144@gmail.com', 'toktorovkurmanbek92@gmail.com', 'toktoroveldos15@gmail.com', 'emir@gmail.com', 'geeks@gmail.com']