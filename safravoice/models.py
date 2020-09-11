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


class ExtratoModel(models.Model):
    AccountId = models.TextField('AccountId', blank=True)
    Agency = models.TextField('Agency', blank=True)
    AccountNumber = models.TextField('AccountNumber', blank=True)
    Amount = models.TextField('Amount', blank=True)
    Currency = models.TextField('Currency', blank=True)
    Bank = models.TextField('Bank', blank=True)
    Agency = models.TextField('Agency', blank=True)
    Number = models.TextField('Number', blank=True)
    Cpf = models.TextField('Cpf', blank=True)
    Name = models.TextField('Name', blank=True)
    Goal = models.TextField('Goal', blank=True)
    Type = models.TextField('Type', blank=True)
    Status = models.TextField('Status', blank=True)
    BookingDateTime = models.TextField('BookingDateTime', blank=True)
    ValueDateTime = models.TextField('ValueDateTime', blank=True)
    TransactionInformation = models.TextField('TransactionInformation',
                                              blank=True)
