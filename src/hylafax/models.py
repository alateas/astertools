from django.db import models
from django.core import urlresolvers
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User, Group
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
#from addons.ext_m2m import ExtManyToManyField, m2m_post_save

logging.basicConfig(filename='/home/astertools/logs/debug.log', level=logging.ERROR)

class FaxDev(models.Model):
    dev_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)

    def get_emails(self):
        return self.email.replace(' ', '').split(',')

    def __unicode__(self):
        return unicode(self.title)

    def has_access(self, user):
        for group in user.groups.all():
            try:
                perm = FaxDevPermission.objects.get(group=group)
                if self in perm.fax_devs.all():
                    return True
            except ObjecDoesNotExist:
                pass
        return False


class Fax(models.Model):
    pdf_file = models.CharField(max_length=255, editable=False)
    sender_number = models.CharField(verbose_name=_('sender_number'), max_length=255)
    sender_name = models.CharField(verbose_name=_('sender_name'), max_length=255, default='')
    description = models.TextField(verbose_name=_('description'), default='')
    date = models.DateTimeField(verbose_name=_('date'), auto_now_add=True, blank=True)  
    fax_dev = models.ForeignKey(FaxDev, verbose_name=_('fax_dev'), editable=False)

    class Meta:
        verbose_name=_('fax')
        verbose_name_plural=_('faxes')    

    def pdf_link(self):
        return '<a href="%s" target="_blank"><img width="20" height="20" src="/m/pdf_icon.png" /></a>' % self.pdf_file
    pdf_link.allow_tags = True
    pdf_link.short_description = _('pdf_file')

class FaxDevPermission(models.Model):
    group = models.ForeignKey(Group, primary_key=True)
    fax_devs = models.ManyToManyField('FaxDev')
