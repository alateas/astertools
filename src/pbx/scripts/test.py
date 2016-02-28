import logging
import traceback
import datetime
from sys import argv,exit,path

now = datetime.datetime.now().strftime("%d/%m/%Y %H:%m")

logging.basicConfig(filename='/opt/astertools/logs/pbx_test.log', level=logging.DEBUG)
try:
    from django.core.management import setup_environ
    path.append('/opt/astertools/src')
    import settings
    setup_environ(settings)

    from pbx.models import Users

    for i in Users.objects.using('asterisk').all():
        print (i.extension, i.name)

    logging.info('%s pbx tested' % now)
except Exception, e:
    logging.error(now + ' | ' + traceback.format_exc())