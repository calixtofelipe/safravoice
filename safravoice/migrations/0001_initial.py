# Generated by Django 2.2.4 on 2020-09-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReqBuilder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(blank=True, max_length=30, verbose_name='client_id')),
                ('secret', models.TextField(blank=True, verbose_name='secret')),
                ('url', models.TextField(verbose_name='url')),
                ('description', models.TextField(verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(blank=True, verbose_name='valor')),
                ('intention', models.CharField(max_length=200, verbose_name='intention')),
            ],
        ),
    ]
