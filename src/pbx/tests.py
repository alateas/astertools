# -*- coding: utf-8 -*-

from django.test import TestCase
from pbx.models import Users

class PbxTest(TestCase):
    multi_db = True
    fixtures = ['users.json', ]

    def test_get_phones_sorting(self):
        extensions = [i.extension for i in Users.get_phones()]
        for n,val in enumerate(extensions[:-1]):
            self.assertTrue(extensions[n+1] > val, "list not sorted")

    def test_get_phones_excluded(self):
        extensions = [i.extension for i in Users.get_phones()]
        self.assertIn(298, extensions)
        self.assertIn(251, extensions)

        extensions = [i.extension for i in Users.get_phones([298, ])]
        self.assertNotIn(298, extensions)
        self.assertIn(251, extensions)

        extensions = [i.extension for i in Users.get_phones([298,251])]
        self.assertNotIn(298, extensions)
        self.assertNotIn(251, extensions)