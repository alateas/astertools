import logging
import traceback
import datetime
from sys import argv,exit,path

now = datetime.datetime.now().strftime("%d/%m/%Y %H:%m")

logging.basicConfig(filename='/opt/astertools/logs/email.log', level=logging.DEBUG)
try:
    from django.core.management import setup_environ
    path.append('/opt/astertools/src')
    import settings
    setup_environ(settings)

    from hylafax.models import Fax, FaxDev

    from django.core.mail import send_mail, EmailMessage

    # send_mail('Subject here', 'Here is the message.', 'fax@lenmontag.ru', ['dmitrymashkin@gmail.com'], fail_silently=False)

    email = EmailMessage('Subject here', 'Here is the message.', 'fax@lenmontag.ru', ['dmitrymashkin@gmail.com'])
    email.attach_file('/opt/astertools/src/urls.py')
    email.send()

    logging.info('email sended')
except Exception, e:
    logging.error(now + ' | ' + traceback.format_exc())
