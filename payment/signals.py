from django.dispatch import Signal
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail as django_send_mail

import ghasedakpack
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


order_paid = (
    Signal()
)  # این جا تعریف کردم. تو ویوز ازش استفاده کردم و در جای لازم سیگنال فرستادم
# و اینجا دوباره گفتم هر وقت پیغام گرفتی این کار رو انجام بده.


def get_client_ip(request):
    """
    Extract client IP address from request considering various headers.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Get the first IP in the chain
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    return ip


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if not user or not request:
        return
    email = user.email
    if not email:
        return
    try:
        ip = get_client_ip(request)
    except Exception as e:
        ip = "Unknown"
    subject = "ورود به سایت"
    message = f"ورود جدید از آی‌پی {ip} به drdjango.ir"
    try:
        send_mail(
            send_from="Motamed Confectionary",
            send_to=[email],
            subject=subject,
            message=message,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
        )
        # django_send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[email],
        #     fail_silently=False,
        # )
        print("email sent!")
    except:
        print("something went wrong about email")


@receiver(order_paid)
def handle_order_paid(sender, **kwargs):
    order = kwargs["order"]
    receiver_email = kwargs["email"]
    message = "%s %s عزیز! سفارش شما با موفقیت ثبت شد. کد پیگیری: %s" % (
        order.first_name,
        order.last_name,
        order.madval_tracking_code,
    )
    sms = ghasedakpack.Ghasedak(settings.GHASEDAK_API_KEY)
    # try:
    #     sms.send({'message': message, 'receptor' : order.phone_number, 'linenumber': settings.MY_LINE_NUMBER_ON_GHASEDAK_1})
    #     print('sms sent by line 1!')
    # except:
    #     try:
    #         sms.send({'message': message, 'receptor' : order.phone_number, 'linenumber': settings.MY_LINE_NUMBER_ON_GHASEDAK_2})
    #         print('sms sent by line 2!')
    #     except:
    #         print('something went wrong about sms')
    try:
        send_mail(
            send_from="Motamed Confectionary",
            send_to=[receiver_email],
            subject="سفارش موفق",
            message=message,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
        )
        # django_send_mail(
        #     subject="سفارش موفق",
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[receiver_email],
        #     fail_silently=False,
        # )
        print("email sent!")
    except:
        print("something went wrong about email")


def send_mail(
    send_from,
    send_to,
    subject,
    message,
    files=[],
    server="smtp.gmail.com",
    port=587,
    username="",
    password="",
    use_tls=True,
):
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
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename={}".format(Path(path).name)
        )
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
