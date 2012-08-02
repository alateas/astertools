import os
from sys import argv,exit,path

from django.core.management import setup_environ
path.append('/home/astertools/src')
import settings
setup_environ(settings)

from hylafax.models import FaxDev

ls = os.listdir('/etc/hylafax/etc')
devs = filter(lambda x:x.startswith('config.tty'), ls)
devs = map(lambda x:x.replace('config.', '', 1), devs)
for dev in devs:
    if not FaxDev.objects.filter(dev_name=dev):
        print 'new device: ' + dev
        FaxDev(dev_name=dev, title=dev).save()
