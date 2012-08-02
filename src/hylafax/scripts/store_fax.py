# -*- coding: utf-8 -*-

import logging
import traceback
import datetime
from sys import argv,exit,path
from django.core.mail import EmailMessage

now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

logging.basicConfig(filename='/home/astertools/logs/fax.log', level=logging.INFO)
logging.debug(now + '|executed!')
logging.debug('args: %s' % argv)

try:
    from django.core.management import setup_environ
    path.append('/home/astertools/src')
    import settings
    setup_environ(settings)

    from hylafax.models import Fax, FaxDev
    import shutil

    if len(argv) < 4:
        exit('Arguments count should be > 2')

    tmp_pdf_file = settings.PROTECTED_MEDIA_ROOT + '/faxes/temp.pdf'
    shutil.copy(argv[1], tmp_pdf_file)

    fax = Fax(pdf_file=tmp_pdf_file, sender_number=argv[2].strip())
    fax_dev = FaxDev.objects.get(dev_name=argv[3].strip())
    fax.fax_dev = fax_dev
    fax.save()

    fax_name = '%d.pdf' % fax.id
    pdf_file = settings.PROTECTED_MEDIA_ROOT + '/faxes/' + fax_name
    shutil.move(tmp_pdf_file, pdf_file)

    if fax_dev.email.strip():
        email = EmailMessage(u'Факс %s' % fax_dev, u'Номер отправителя : %s ' % fax.sender_number, '6004791@lenmontag.ru', fax_dev.get_emails())
        email.attach_file(pdf_file)
        email.send()

    fax.pdf_file = settings.PROTECTED_MEDIA_URL + 'faxes/' + fax_name
    fax.save()
    logging.info('%s | fax %s successfully saved' % (now, pdf_file))
except Exception, e:
    logging.error(now + ' | ' + traceback.format_exc())