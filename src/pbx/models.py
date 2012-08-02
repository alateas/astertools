from django.db import models

class Users(models.Model):
    extension = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    @classmethod
    def get_phones(cls, excluded=[]):
        return Users.objects.using('asterisk').exclude(extension__in = excluded)
        #.exclude(extension=251)

    class Meta:
        ordering = ('extension', )
        db_table = 'users'