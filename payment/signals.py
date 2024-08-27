from django.dispatch import Signal
from django.dispatch import receiver

import ghasedakpack
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from config.madval1369_secret import *

order_paid = Signal() # این جا تعریف کردم. تو ویوز ازش استفاده کردم و در جای لازم سیگنال فرستادم
# و اینجا دوباره گفتم هر وقت پیغام گرفتی این کار رو انجام بده.


@receiver(order_paid)
def handle_order_paid(sender, **kwargs):
    order = kwargs['order']
    receiver_email = kwargs['email']
    message = "%s %s عزیز! سفارش شما با موفقیت ثبت شد. کد پیگیری: %s" \
                %(order.first_name, order.last_name, order.madval_tracking_code)
    sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
    # try:
    #     sms.send({'message': message, 'receptor' : order.phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_1})
    #     print('sms sent by line 1!')
    # except:
    #     try:
    #         sms.send({'message': message, 'receptor' : order.phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
    #         print('sms sent by line 2!')
    #     except:
    #         print('something went wrong about sms')
    try:
        # send_mail(send_from="Motamed Confectionary", send_to=[receiver_email], subject='سفارش موفق',
        #       message=message, username=DJANGO_EMAIL_ADDRESS, password=DJANGO_EMAIL_APP_PASSWORD)
        print('email sent!')
    except:
        print('something went wrong about email')


def send_mail(send_from, send_to, subject, message, files=[],
              server="smtp.gmail.com", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
