from datetime import datetime as DateTime
import smtplib
import ssl
from email.message import EmailMessage

from prettyconf import config

AWS_SNS_SERVER = config('SMTP_SERVER')
AWS_SNS_PORT = config('SMTP_PORT', cast=int, default=587)
AWS_SNS_USERNAME = config('SMTP_USERNAME')
AWS_SNS_PASSWORD = config('SMTP_PASSWORD')

email_to = 'euribates@gmail.com'
# email_to = 'jrodleo@gobiernodecanarias.org'
# email_to = 'susi.suarez@gmail.com'
# email_to = 'misanram@gmail.com'


msg = EmailMessage()
msg['Subject'] = "Simple mail TEST - 1"
msg['From'] = 'info@pythoncanarias.es'
msg['To'] = email_to
now = DateTime.now()
msg.set_content(f'Ejemplo de envio usando AWS SNS a pelo. {now}')

context = ssl.create_default_context()
server = smtplib.SMTP(
    AWS_SNS_SERVER,
    port=AWS_SNS_PORT,
    )
server.ehlo()
server.starttls(context=context)
server.login(AWS_SNS_USERNAME, AWS_SNS_PASSWORD)
result = server.send_message(msg)
print('result =', result)
server.quit()
