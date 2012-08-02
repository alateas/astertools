# -*- coding: utf-8 -*-

from django.test import TestCase
from hylafax.models import Fax, FaxDev

class FaxTest(TestCase):

    def setUp(self):
        FaxDev(dev_name='ttyIAX1', title='fax 1').save()
        FaxDev(dev_name='ttyIAX2', title='fax 2').save()
        self.fax = Fax(pdf_file='atata', sender_number='666')
        self.fax.fax_dev = FaxDev.objects.get(dev_name='ttyIAX1')

    def test_utf(self):
