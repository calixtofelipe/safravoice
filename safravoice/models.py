from django.db import models
from django.db.models import Q


# Create your models here.
class ReqBuilder(models.Model):
    client_id = models.CharField('client_id', max_length=30, blank=True)
    secret = models.TextField('secret', blank=True)
    url = models.TextField('url')
    description = models.TextField('description')

    def __str__(self):
        return f'{self.id} - {self.description}'
